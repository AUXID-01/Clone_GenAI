import sys
from agent import run_agent

def main():
    """
    CLI entry point for the Scaler Agent.
    """
    banner = """
\033[93m╔══════════════════════════════════════╗
║       Scaler Agent — CLI Tool        ║
╚══════════════════════════════════════╝\033[0m
Type your instruction below. Type 'exit' or 'quit' to quit.
"""
    print(banner)

    while True:
        try:
            user_input = input("\n\033[92mYou:\033[0m ").strip()
            
            if not user_input:
                continue
                
            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break
                
            run_agent(user_input)
            
        except KeyboardInterrupt:
            print("\n\nExiting gracefully... Goodbye!")
            sys.exit(0)
        except Exception as e:
            print(f"\n[ERROR] An error occurred in main: {str(e)}")

if __name__ == "__main__":
    main()
