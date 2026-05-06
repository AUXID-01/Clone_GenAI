import os
import json
import time
from groq import Groq, RateLimitError
from dotenv import load_dotenv
from tools import tool_map
from prompts.system_prompt import SYSTEM_PROMPT

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def run_agent(user_input: str):
    """
    Main agent reasoning loop: START -> THINK -> TOOL -> OBSERVE -> OUTPUT
    """
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_input}
    ]
    
    print(f"\n[START] User instruction received: {user_input}")
    
    max_retries = 3
    retry_delay = 2 # Groq is more stable, lower retry delay
    
    while True:
        try:
            print(f"[\033[90mDEBUG\033[0m] Sending request to Groq...")
            
            # Call Groq with retry logic
            response = None
            for attempt in range(max_retries):
                try:
                    response = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=messages,
                        response_format={"type": "json_object"} 
                    )
                    break # Success, exit retry loop
                except RateLimitError as e:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (2 ** attempt)
                        print(f"[\033[91mDEBUG\033[0m] Groq Rate limit hit. Retrying in {wait_time}s...")
                        time.sleep(wait_time)
                    else:
                        raise e 
            
            if not response:
                break

            raw_content = response.choices[0].message.content
            print(f"[\033[90mDEBUG\033[0m] Received response from AI.")
            
            try:
                data = json.loads(raw_content)
            except json.JSONDecodeError:
                print(f"[\033[91mDEBUG\033[0m] Groq returned invalid JSON: {raw_content[:100]}...")
                messages.append({"role": "assistant", "content": raw_content})
                continue

            step = data.get("step")
            content = data.get("content", "")
            
            # Log internal AI state for debugging
            print(f"[\033[90mDEBUG\033[0m] AI Step: {step}")
            
            # Print the current step
            if step == "THINK":
                print(f"[\033[94mTHINK\033[0m]   {content}")
            elif step == "TOOL":
                tool_name = data.get("tool_name")
                tool_args = data.get("tool_args", {})
                print(f"[\033[93mTOOL\033[0m]    Calling {tool_name} with {tool_args}")
                
                # Execute tool
                if tool_name in tool_map:
                    result = tool_map[tool_name](**tool_args)
                else:
                    result = f"Error: Tool '{tool_name}' not found."
                
                print(f"[\033[92mOBSERVE\033[0m] {result}")
                
                # Add assistant message and tool observation back to conversation
                messages.append({"role": "assistant", "content": raw_content})
                messages.append({"role": "user", "content": json.dumps({
                    "step": "OBSERVE",
                    "content": result
                })})
                continue # Next iteration
                
            elif step == "OUTPUT":
                print(f"[\033[95mOUTPUT\033[0m]  {content}")
                break 
            
            elif step == "START":
                print(f"[\033[96mSTART\033[0m]   {content}")
            
            else:
                print(f"[\033[91mDEBUG\033[0m] AI emitted unknown step: {step}. Content: {content[:50]}...")
            
            # For START, THINK or unknown steps, we just append and continue
            messages.append({"role": "assistant", "content": raw_content})
            
            # Small delay to keep the loop readable
            time.sleep(1)
            
        except Exception as e:
            print(f"[FATAL ERROR] An unexpected error occurred in the agent loop: {str(e)}")
            break
