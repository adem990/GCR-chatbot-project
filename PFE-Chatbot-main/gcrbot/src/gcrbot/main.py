# src/gcrbot/main.py
import os
os.environ["GRPC_VERBOSITY"] = "NONE"
os.environ["GRPC_LOG_LEVEL"] = "ERROR"
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"

import warnings
warnings.filterwarnings("ignore")
from gcrbot.gemini_tool import ask_gemini

def run():
    print("PFE Chatbot (type 'quit' to exit)")
    while True:
        q = input("\nYou: ").strip()
        if q.lower() in ['quit', 'q', 'exit']:
            print("Goodbye!")
            break
        if q:
            print(f"\nAssistant: {ask_gemini(q)}")

# Needed by CrewAI command "crewai run"
if __name__ == "__main__":
    run()
