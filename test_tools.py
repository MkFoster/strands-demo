"""
Test script to verify API tools work correctly.
Run this to test the tools independently before using with the agent.
"""

from api_tools import (
    get_user_info, 
    get_posts_by_user, 
    get_post_by_id, 
    get_user_todos, 
    get_random_quote
)
import json


def test_tools():
    """Test each API tool independently."""
    print("🧪 Testing API Tools")
    print("=" * 40)
    
    # Test user info
    print("\n1. Testing get_user_info(1)...")
    user = get_user_info(1)
    print(f"User name: {user.get('name', 'Error')}")
    print(f"Email: {user.get('email', 'Error')}")
    
    # Test posts by user
    print("\n2. Testing get_posts_by_user(1)...")
    posts = get_posts_by_user(1)
    if isinstance(posts, list) and len(posts) > 0:
        print(f"Found {len(posts)} posts")
        print(f"First post title: {posts[0].get('title', 'Error')}")
    else:
        print("Error fetching posts")
    
    # Test specific post
    print("\n3. Testing get_post_by_id(1)...")
    post = get_post_by_id(1)
    print(f"Post title: {post.get('title', 'Error')}")
    
    # Test user todos
    print("\n4. Testing get_user_todos(1)...")
    todos = get_user_todos(1)
    if isinstance(todos, list) and len(todos) > 0:
        print(f"Found {len(todos)} todos")
        completed = sum(1 for todo in todos if todo.get('completed'))
        print(f"Completed todos: {completed}/{len(todos)}")
    else:
        print("Error fetching todos")
    
    # Test random quote
    print("\n5. Testing get_random_quote()...")
    quote = get_random_quote()
    print(f"Quote: {quote.get('content', 'Error')}")
    print(f"Author: {quote.get('author', 'Unknown')}")
    
    print("\n✅ Tool testing complete!")


if __name__ == "__main__":
    test_tools()