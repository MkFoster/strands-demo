#!/usr/bin/env python3
"""
Test script to check if your model provider is configured correctly.
Run this before starting the web application to verify setup.
"""

import sys
import os
from dotenv import load_dotenv
from strands import Agent
from strands_tools import current_time

def check_env_config():
    """Check if .env file is configured properly."""
    print("🔍 Checking .env configuration...")
    
    # Load .env file
    load_dotenv()
    
    has_aws = os.getenv('AWS_ACCESS_KEY_ID') and os.getenv('AWS_SECRET_ACCESS_KEY')
    has_openai = os.getenv('OPENAI_API_KEY')
    aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
    
    if has_aws:
        print(f"✅ AWS credentials found in environment")
        print(f"✅ AWS region: {aws_region}")
        return True
    elif has_openai:
        print(f"✅ OpenAI API key found in environment")
        return True
    else:
        print("❌ No credentials found in environment")
        print("\n🔧 Setup Instructions:")
        print("1. Copy .env.example to .env:")
        print("   cp .env.example .env")
        print("\n2. Edit .env file and add your credentials:")
        print("   AWS_ACCESS_KEY_ID=your_access_key_here")
        print("   AWS_SECRET_ACCESS_KEY=your_secret_key_here")
        print("   AWS_DEFAULT_REGION=us-east-1")
        print("\n   OR for OpenAI:")
        print("   OPENAI_API_KEY=your_openai_key_here")
        return False

def test_model_provider():
    """Test if the model provider is working correctly."""
    print("🧪 Testing Strands Agent Configuration")
    print("=" * 60)
    
    # Check environment first
    if not check_env_config():
        return False
        
    print("\n🤖 Testing agent creation...")
    
    try:
        # Create a simple agent with just one tool
        agent = Agent(tools=[current_time])
        print("✅ Agent created successfully")
        
        # Try a simple test message
        print("💬 Testing agent with a simple message...")
        response = agent("What time is it?")
        print(f"✅ Agent responded: {response}")
        print("\n🎉 SUCCESS: Your model provider is configured correctly!")
        print("🚀 You can now run the web application with:")
        print("   python -m uvicorn web_app:app --host 0.0.0.0 --port 8000")
        return True
        
    except Exception as e:
        error_str = str(e)
        print(f"❌ ERROR: {error_str}")
        
        if "Unable to locate credentials" in error_str or "NoCredentialsError" in error_str:
            print("\n🔧 AWS Bedrock Setup Required:")
            print("1. Make sure your .env file has valid AWS credentials")
            print("2. Verify you have Bedrock access in your AWS account")
            print("3. Check that your IAM user has Bedrock permissions")
            
        elif "InvalidRequestException" in error_str:
            print("\n🔧 Bedrock Access Issue:")
            print("1. Request access to Bedrock models in AWS Console")
            print("2. Go to: AWS Console → Amazon Bedrock → Model access")
            print("3. Request access to Claude or other models")
            
        else:
            print(f"\n❓ Unexpected error: {e}")
            print("Please check the Strands Agents documentation for troubleshooting.")
            
        return False

if __name__ == "__main__":
    success = test_model_provider()
    sys.exit(0 if success else 1)