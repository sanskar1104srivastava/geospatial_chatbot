# --- FILE: creator.py (using a local Mistral model via Ollama) ---

import os
from langchain_community.chat_models import ChatOllama # MODIFIED: Imported ChatOllama
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_openai_tools_agent, AgentExecutor

# --- Step 1: Import your tools (No change here) ---
from tools.overpass_tool import find_amenities_in_city, find_amenities_near_point

# --- Configuration ---
# MODIFIED: No API key needed! We are running the model locally with Ollama.
# We have removed all the API key checks.


# --- Step 2: Define the agent's core instructions (No change here) ---
# This prompt works perfectly with a local Mistral model.
SYSTEM_PROMPT = """
You are Geo, a friendly and expert geography assistant. Your main goal is to help users find places and amenities.

You must follow these rules for every interaction:

1.  **Analyze the User's Intent:** First, determine if the user is asking a broad question about a whole city or a specific question about an amenity near a landmark.

2.  **Strategy for Broad City Queries:**
    - If a user asks a general question like "Tell me about Gorakhpur" or "What can I find in Gorakhpur?", DO NOT ask for more details immediately.
    - Your primary action is to call the `city_wide_amenity_search` tool using only the `city_or_district` argument. Leave `amenity_type` empty.
    - This provides a general overview first.

3.  **Strategy for Specific Amenity Queries:**
    - If the user asks for a specific amenity like "a general hospital in Gorakhpur", use the `city_wide_amenity_search` tool with both `city_or_district` and `amenity_type` filled.
    - If they ask for something near a landmark (e.g., "cafes near the Eiffel Tower"), use the `point_of_interest_amenity_search` tool.

4.  **Engage in a Helpful Conversation:**
    - After providing an initial list of results, always offer to help the user refine their search.
    - For example, after a general search, you can say: "I found several amenities including restaurants, parks, and hospitals. Are you interested in a particular category?"
    - Always present the information clearly and concisely.
"""


# --- Step 3: Initialize the Agent and its Components ---

def create_geo_agent() -> AgentExecutor:
    """
    Creates and configures the Geo agent to use a local Ollama model.
    """
    print("Initializing Geo agent with local Mistral model via Ollama...")

    # MODIFIED: Define the LLM to be the local Ollama instance.
    # The 'model' name must match the model you pulled with 'ollama run'.
    llm = ChatOllama(model="mistral", temperature=0)

    # The rest of the setup remains the same.
    tools = [find_amenities_in_city, find_amenities_near_point]
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])
    agent = create_openai_tools_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True
    )

    print("Agent initialized successfully.")
    return agent_executor


def run_agent_interaction(agent_executor: AgentExecutor, user_input: str) -> None:
    """
    Runs a single interaction with the agent and prints the output.
    """
    print(f"\n--- 💬 Query: '{user_input}' ---\n")
    try:
        response = agent_executor.invoke({"input": user_input})
        print("\n--- ✅ Final Answer ---")
        print(response.get("output", "No output generated."))
    except Exception as e:
        print(f"\n--- ❌ An error occurred ---")
        print(f"Error details: {e}")
    finally:
        print("\n" + "="*60)


# --- Step 4: Main Execution Block (No change here) ---

if __name__ == "__main__":
    # IMPORTANT: Make sure the Ollama application is running before you execute this script.
    geo_agent = create_geo_agent()
    
    # --- Interactive Session ---
    print("\n--- 🗣️ Interactive Session with Local Mistral (type 'exit' to quit) ---")
    while True:
        try:
            user_query = input("You: ")
            if user_query.lower() == 'exit':
                print("Geo: Goodbye!")
                break
            run_agent_interaction(geo_agent, user_query)
        except KeyboardInterrupt:
            print("\nGeo: Goodbye!")
            break