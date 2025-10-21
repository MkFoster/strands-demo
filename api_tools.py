"""
Tools for making API calls to JSONPlaceholder API.
This demonstrates how to create custom tools for Strands Agents.
"""

import requests
import json
from typing import Dict, Any, List
from strands import tool


@tool
def get_user_info(user_id: int) -> Dict[str, Any]:
    """
    Fetch user information by user ID from JSONPlaceholder API.
    
    Args:
        user_id: The ID of the user to fetch (1-10)
        
    Returns:
        Dictionary containing user information including name, email, address, etc.
    """
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{user_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch user info: {str(e)}"}


@tool
def get_posts_by_user(user_id: int) -> List[Dict[str, Any]]:
    """
    Fetch all posts by a specific user from JSONPlaceholder API.
    
    Args:
        user_id: The ID of the user whose posts to fetch (1-10)
        
    Returns:
        List of dictionaries containing post information (title, body, etc.)
    """
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts?userId={user_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return [{"error": f"Failed to fetch posts: {str(e)}"}]


@tool
def get_post_by_id(post_id: int) -> Dict[str, Any]:
    """
    Fetch a specific post by its ID from JSONPlaceholder API.
    
    Args:
        post_id: The ID of the post to fetch (1-100)
        
    Returns:
        Dictionary containing post information (title, body, userId, etc.)
    """
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/posts/{post_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return {"error": f"Failed to fetch post: {str(e)}"}


@tool
def get_user_todos(user_id: int) -> List[Dict[str, Any]]:
    """
    Fetch all todos for a specific user from JSONPlaceholder API.
    
    Args:
        user_id: The ID of the user whose todos to fetch (1-10)
        
    Returns:
        List of dictionaries containing todo information (title, completed status, etc.)
    """
    try:
        response = requests.get(f"https://jsonplaceholder.typicode.com/todos?userId={user_id}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        return [{"error": f"Failed to fetch todos: {str(e)}"}]


@tool
def get_random_quote() -> Dict[str, Any]:
    """
    Fetch a random quote from the quotable API.
    
    Returns:
        Dictionary containing quote information.
    """
    try:
        response = requests.get("https://api.quotable.io/random")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        # Return a fallback quote if the API fails
        return {
            "content": "The best time to plant a tree was 20 years ago. The second best time is now.",
            "author": "Chinese Proverb",
            "error": f"API temporarily unavailable: {str(e)}"
        }