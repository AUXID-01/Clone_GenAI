import os
import json
import time
from typing import List, Dict, Any
from groq import Groq, RateLimitError as GroqRateLimitError
from openai import OpenAI, RateLimitError as OpenRouterRateLimitError
from dotenv import load_dotenv

from core.state import AgentState, Task, TaskStatus
from core.logger import logger
from tools.registry import registry
from logic.observer import Observer
from logic.recovery import RecoveryManager
from prompts.system_prompt import SYSTEM_PROMPT

load_dotenv()

class AgentRuntime:
    def __init__(self, model: str = None):
        self.openrouter_key = os.getenv("OPENROUTER_API_KEY")
        self.groq_key = os.getenv("GROQ_API_KEY")
        
        if self.openrouter_key:
            print("[\033[94mINFO\033[0m] Using OpenRouter as the reasoning engine.")
            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.openrouter_key,
            )
            self.model = model or "meta-llama/llama-3.3-70b-instruct"
            self.is_groq = False
        else:
            print("[\033[94mINFO\033[0m] Using Groq as the reasoning engine.")
            self.client = Groq(api_key=self.groq_key)
            self.model = model or "llama-3.3-70b-versatile"
            self.is_groq = True

        self.state = None
        self.observer = None
        self.recovery = None
        self.messages = []

    def _initialize(self, objective: str):
        self.state = AgentState(objective=objective)
        self.observer = Observer(self.state)
        self.recovery = RecoveryManager(self.state)
        self.messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"OBJECTIVE: {objective}"}
        ]

    def run(self, objective: str):
        self._initialize(objective)
        print(f"\n[INIT] Starting runtime for objective: {objective}")

        while True:
            # Add state summary to context
            state_summary = self.observer.get_summary()
            current_context = self.messages + [{"role": "system", "content": f"STATE SUMMARY:\n{state_summary}"}]

            try:
                print(f"[\033[90mDEBUG\033[0m] Requesting reasoning from {self.model}...")
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=current_context,
                    response_format={"type": "json_object"}
                )
                
                message = response.choices[0].message
                raw_content = message.content
                
                if raw_content is None:
                    finish_reason = response.choices[0].finish_reason
                    error_msg = f"Model returned empty content. Finish reason: {finish_reason}"
                    if finish_reason == "content_filter":
                        error_msg += " (Output was filtered by safety systems)"
                    raise ValueError(error_msg)

                try:
                    data = json.loads(raw_content)
                except json.JSONDecodeError as e:
                    print(f"[\033[91mERROR\033[0m] Failed to parse JSON: {str(e)}")
                    print(f"[\033[90mDEBUG\033[0m] Raw Content: {raw_content}")
                    raise ValueError(f"Invalid JSON response: {str(e)}")
                
                step = data.get("step")
                thinking = data.get("thinking", "")
                plan_data = data.get("plan", [])
                
                if not step:
                    raise ValueError("LLM response missing required 'step' field.")

                # Update Tasks from PLAN
                if plan_data:
                    self._sync_tasks(plan_data)

                # ALWAYS append the assistant's response to history so it doesn't repeat itself
                self.messages.append({"role": "assistant", "content": raw_content})

                logger.log_step(step, thinking)
                print(f"[\033[94mTHINK\033[0m] {thinking}")
                
                if step == "TOOL":
                    tool_name = data.get("tool_name")
                    tool_args = data.get("tool_args", {})
                    
                    if not tool_name:
                        print("[\033[91mERROR\033[0m] Step is TOOL but 'tool_name' is missing.")
                        self.messages.append({"role": "user", "content": "You specified step 'TOOL' but forgot to provide 'tool_name'. Please provide it."})
                        continue

                    print(f"[\033[93mTOOL\033[0m]  Executing {tool_name}...")
                    
                    result = registry.execute(tool_name, tool_args)
                    
                    # Process observation
                    self.observer.observe(tool_name, tool_args, result)
                    
                    logger.log_tool(tool_name, tool_args, result.success, str(result.data if result.success else result.error))
                    print(f"[\033[92mOBSERVE\033[0m] {'Success' if result.success else 'Error: ' + result.error}")
                    
                    # Update message history with observation
                    self.messages.append({
                        "role": "user", 
                        "content": json.dumps({
                            "observation": result.data if result.success else result.error,
                            "success": result.success
                        })
                    })
                    
                elif step == "OUTPUT":
                    print(f"\n[\033[95mOUTPUT\033[0m] {data.get('content', 'Objective complete.')}")
                    break
                
                elif step == "ERROR":
                    print(f"[\033[91mERROR\033[0m] {data.get('content', 'Unknown error reported by AI.')}")
                    break
                
                elif step == "PLAN":
                    print(f"[\033[94mPLAN\033[0m] Plan updated. Proceeding to execution...")
                    self.messages.append({
                        "role": "user",
                        "content": "Plan updated. Now execute the first tool to begin implementation."
                    })
                
                else:
                    print(f"[\033[91mWARNING\033[0m] Unknown step: {step}")
                    self.messages.append({
                        "role": "user",
                        "content": f"I don't recognize the step '{step}'. Please use PLAN, TOOL, OUTPUT, or ERROR."
                    })
                
                # Small delay
                time.sleep(1)

            except (GroqRateLimitError, OpenRouterRateLimitError):
                print("[\033[91mDEBUG\033[0m] Rate limit hit. Waiting 10s...")
                time.sleep(10)
            except Exception as e:
                print(f"[FATAL] Runtime crash: {str(e)}")
                # Self-correction attempt
                error_feedback = f"The last response caused a system error: {str(e)}. Please ensure your next response is valid JSON and follows the required schema."
                self.messages.append({"role": "user", "content": error_feedback})
                time.sleep(2)

    def _sync_tasks(self, plan_data: List[Dict[str, Any]]):
        """
        Synchronizes the agent's internal task list with the LLM's plan.
        """
        for t_data in plan_data:
            existing = self.state.get_task_by_id(t_data.get("id"))
            if not existing:
                self.state.tasks.append(Task(
                    id=t_data.get("id"),
                    title=t_data.get("title", "Untitled Task"),
                    description=t_data.get("description", ""),
                    status=TaskStatus(t_data.get("status", "pending"))
                ))
            else:
                existing.status = TaskStatus(t_data.get("status", "pending"))
