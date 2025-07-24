# main.py
import sys
import os

# --- THIS IS THE CRITICAL FIX ---
# Add the project's root directory to the Python path.
# This ensures that all modules can be imported correctly, regardless of where the script is run from.
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)
# -----------------------------

from agent.creator import create_geospatial_agent

def chat_loop():
    """
    Initializes the agent and runs the main conversational loop.
    """
    # Create the agent once when the application starts
    try:
        agent = create_geospatial_agent()
    except Exception as e:
        print(f"❌ Could not create the agent. Please check your setup. Error: {e}", file=sys.stderr)
        sys.exit(1)

    print("\n--- 🗺️  Geo, the ReAct Geospatial Agent, is ready! ---")
    print("Ask me to find places. I will show you my thoughts as I work.")
    print("Example: 'Find 3 cafes near the Eiffel Tower in Paris'")
    print("Type 'exit' or 'quit' to end the chat.")

    while True:
        user_query = input("\nYou: ")
        if user_query.lower() in ['exit', 'quit']:
            print("\nBot: Goodbye!")
            break
        
        try:
            # Let the agent handle the entire process
            response = agent.invoke({"input": user_query})
            # Print only the final, clean answer from the agent's response
            print(f"\nGeo: {response['output']}")
        except Exception as e:
            # Catch potential errors during the agent's run for a better user experience
            print(f"\nAn unexpected error occurred: {e}")

if __name__ == "__main__":
    chat_loop()