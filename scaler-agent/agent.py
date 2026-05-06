from core.runtime import AgentRuntime

def run_agent(user_input: str):
    """
    Backward compatible wrapper for the new hardened runtime.
    """
    runtime = AgentRuntime()
    runtime.run(user_input)

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        run_agent(" ".join(sys.argv[1:]))
    else:
        run_agent("Build a high-fidelity Scaler Academy clone.")
