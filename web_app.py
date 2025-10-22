"""
FastAPI backend for Strands Agents Chat Demo

This creates a web API that serves the Strands agent with a chat interface.
Includes endpoints for chat messages and static file serving.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import asyncio
from typing import Dict, Any
import traceback
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from strands import Agent
from strands_tools import current_time
from api_tools import (
    get_user_info, 
    get_posts_by_user, 
    get_post_by_id, 
    get_user_todos, 
    get_random_quote
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Strands Agents Chat Demo",
    description="A web interface for interacting with Strands Agents using API tools",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    error: str = None

# Initialize the Strands agent
try:
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
    logger.info("✅ Strands agent initialized successfully")
except Exception as e:
    logger.error(f"❌ Failed to initialize Strands agent: {e}")
    agent = None

@app.get("/", response_class=HTMLResponse)
async def root():
    """Serve the main chat interface"""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "agent_available": agent is not None,
        "tools_count": 6 if agent else 0  # We know we have 6 tools
    }

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """
    Process a chat message through the Strands agent
    """
    if not agent:
        raise HTTPException(
            status_code=500, 
            detail="Strands agent not available. Please check your model provider configuration."
        )
    
    try:
        logger.info(f"Processing message: {message.message[:100]}...")
        
        # Run the agent in a thread pool to avoid blocking
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, agent, message.message)
        
        logger.info("✅ Agent response generated successfully")
        return ChatResponse(response=str(response))
        
    except Exception as e:
        error_msg = f"Error processing message: {str(e)}"
        logger.error(f"❌ {error_msg}")
        logger.error(traceback.format_exc())
        
        # Provide specific guidance for common credential issues
        if "Unable to locate credentials" in str(e) or "NoCredentialsError" in str(e):
            helpful_message = """
🔧 **AWS Bedrock Setup Required**

To use this chat interface, you need to configure AWS Bedrock credentials:

**Quick Setup with .env file (Recommended):**
1. Copy `.env.example` to `.env`
2. Fill in your AWS credentials in the `.env` file:
   ```
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   AWS_DEFAULT_REGION=us-east-1
   ```
3. Restart the server

**Alternative: AWS CLI**
1. Install: `pip install awscli`
2. Configure: `aws configure`

**Alternative: OpenAI**
1. Add to `.env` file: `OPENAI_API_KEY=your_key_here`

**Get AWS Bedrock Access:**
- Sign up for AWS account
- Request access to Bedrock models in AWS console
- Create IAM user with Bedrock permissions
- Use those credentials in your `.env` file

Once configured, restart the server and try again!
            """.strip()
            
            return ChatResponse(
                response=helpful_message,
                error="AWS Bedrock credentials not configured"
            )
        
        return ChatResponse(
            response="I apologize, but I encountered an error processing your request. Please check the server logs for details.",
            error=error_msg
        )

@app.get("/tools")
async def list_tools():
    """List available tools"""
    if not agent:
        return {"tools": [], "error": "Agent not available"}
    
    # Since we can't access agent.tools directly, let's return the known tools
    tools_info = [
        {"name": "current_time", "doc": "Get the current time"},
        {"name": "get_user_info", "doc": "Fetch user information by user ID from JSONPlaceholder API"},
        {"name": "get_posts_by_user", "doc": "Fetch all posts by a specific user from JSONPlaceholder API"},
        {"name": "get_post_by_id", "doc": "Fetch a specific post by its ID from JSONPlaceholder API"},
        {"name": "get_user_todos", "doc": "Fetch all todos for a specific user from JSONPlaceholder API"},
        {"name": "get_random_quote", "doc": "Fetch a random quote from the quotable API"}
    ]
    
    return {"tools": tools_info}

@app.get("/demo")
async def demo_suggestions():
    """Get demo message suggestions"""
    return {
        "suggestions": [
            "What time is it right now?",
            "Tell me about user 3 from the API",
            "Get posts by user 1",
            "Show me todos for user 2", 
            "Get me an inspirational quote",
            "Fetch post #5 and summarize it",
            "Compare users 1 and 2 - who has more completed todos?",
            "Get the latest posts and give me the top 3 most interesting titles"
        ]
    }

# Mount static files (we'll create this directory)
app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting Strands Agents Chat Server...")
    print("📖 Available at: http://localhost:8000")
    print("🔧 API docs at: http://localhost:8000/docs")
    uvicorn.run("web_app:app", host="0.0.0.0", port=8000, reload=True)