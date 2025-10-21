"""
Strands Agents Demo - API Tool Integration

This demo shows how to create a Strands Agent with custom tools that make API calls
to public JSON APIs. The agent can fetch user data, posts, todos, and quotes.
"""

from strands import Agent
from strands_tools import current_time
from api_tools import (
    get_user_info, 
    get_posts_by_user, 
    get_post_by_id, 
    get_user_todos, 
    get_random_quote
)


def main():
    """
    Main function to demonstrate the Strands Agent with API tools.
    """
    print("🤖 Strands Agents Demo - API Tools Integration")
    print("=" * 50)
    
    # Create an agent with our custom API tools plus a built-in tool
    agent = Agent(
        tools=[
            current_time,      # Built-in tool from strands-agents-tools
            get_user_info,     # Our custom API tools
            get_posts_by_user,
            get_post_by_id,
            get_user_todos,
            get_random_quote
        ]
    )
    
    # Demo message that will exercise multiple tools
    demo_message = """
    Hello! I'd like you to help me explore some data using your API tools. 
    
    Please do the following:
    1. First, tell me what time it is right now
    2. Get information about user #3 from the JSONPlaceholder API
    3. Fetch all posts by that user
    4. Get the todos for user #5 
    5. Fetch a random inspirational quote
    6. Summarize what you learned about the users and their activity
    
    Please use your tools to gather this information and provide a nice summary!
    """
    
    print("🔄 Sending request to agent...")
    print(f"Request: {demo_message}")
    print("\n" + "=" * 50)
    print("🤖 Agent Response:")
    print("=" * 50)
    
    # Send the message to the agent and get the response
    try:
        response = agent(demo_message)
        print(response)
    except Exception as e:
        print(f"❌ Error running agent: {e}")
        print("Make sure you have:")
        print("1. Installed all requirements: pip install -r requirements.txt")
        print("2. Set up your model provider (check Strands documentation)")
        print("3. Have internet connection for API calls")


if __name__ == "__main__":
    main()