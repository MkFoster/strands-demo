"""
Interactive Strands Agent Demo

A simple interactive demo that lets you chat with the agent and use API tools.
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
    Interactive chat with the Strands Agent.
    """
    print("🤖 Interactive Strands Agent Demo")
    print("=" * 40)
    print("This agent has access to JSONPlaceholder API tools:")
    print("- get_user_info(user_id): Get user details")
    print("- get_posts_by_user(user_id): Get user's posts") 
    print("- get_post_by_id(post_id): Get specific post")
    print("- get_user_todos(user_id): Get user's todos")
    print("- get_random_quote(): Get inspirational quote")
    print("- current_time(): Get current time")
    print("\nTry asking things like:")
    print("- 'Tell me about user 1'")
    print("- 'Get posts by user 2'")
    print("- 'Show me todos for user 3'")
    print("- 'Get me a random quote'")
    print("- 'What time is it?'")
    print("\nType 'quit' to exit")
    print("=" * 40)
    
    # Create the agent
    agent = Agent(
        tools=[
            current_time,
            get_user_info,
            get_posts_by_user,
            get_post_by_id,
            get_user_todos,
            get_random_quote
        ]
    )
    
    while True:
        try:
            user_input = input("\n🧑 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye!")
                break
                
            if not user_input:
                print("Please enter a message or 'quit' to exit.")
                continue
                
            print("\n🤖 Agent:")
            response = agent(user_input)
            print(response)
            
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("Make sure you have set up your model provider correctly.")


if __name__ == "__main__":
    main()