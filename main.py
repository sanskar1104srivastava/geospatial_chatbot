# --- FILE: main.py (Corrected) ---
import sys
import os

# Add the project's root directory to the Python path to find the 'agent' module
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# MODIFICATION 1: Changed the imported function name to match creator.py
# This assumes your creator.py file is located at: ./agent/creator.py
from agent.creator import create_geo_agent

def chat_loop():
    """Initializes the agent and runs the main conversational loop."""
    
    # MODIFICATION 2: Called the correct function name here.
    agent = create_geo_agent()

    print("\n--- 🗺️  Geo, the Multi-Tool Agent, is ready! ---")
    print("I can search within a city ('hospitals in Gorakhpur') or near a landmark ('cafes near India Gate').")
    print("Type 'exit' or 'quit' to end the chat.")

    while True:
        try:
            user_query = input("\nYou: ")
            if user_query.lower() in ['exit', 'quit']:
                print("\nGeo: Goodbye!")
                break
            
            # The agent invocation is correct
            response = agent.invoke({"input": user_query})
            print(f"\nGeo: {response['output']}")

        except KeyboardInterrupt:
            print("\n\nGeo: Goodbye!")
            break
        except Exception as e:
            print(f"\nAn unexpected error occurred: {e}")
            print("Please try again.")


if __name__ == "__main__":
    chat_loop()