#!/usr/bin/env python3
"""
Setup script for Agentic Mentor with Gemini API
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def setup_gemini():
    """Setup Gemini API configuration"""
    
    print("🤖" + "="*50 + "🤖")
    print("           AGENTIC MENTOR - Gemini Setup")
    print("🤖" + "="*50 + "🤖")
    
    # Check if Gemini API key is set
    gemini_key = os.getenv("GEMINI_API_KEY")
    
    if not gemini_key or gemini_key == "your_gemini_api_key_here":
        print("❌ GEMINI_API_KEY not found or not set properly")
        print("\n📋 To get a Gemini API key:")
        print("1. Go to: https://makersuite.google.com/app/apikey")
        print("2. Sign in with your Google account")
        print("3. Click 'Create API Key'")
        print("4. Copy the generated key")
        print("\n🔧 Set the environment variable:")
        print("   Windows: set GEMINI_API_KEY=your_key_here")
        print("   Linux/Mac: export GEMINI_API_KEY=your_key_here")
        print("\n💡 Or create a .env file with:")
        print("   USE_GEMINI=true")
        print("   GEMINI_API_KEY=your_key_here")
        return False
    
    print(f"✅ GEMINI_API_KEY found: {gemini_key[:10]}...")
    
    # Test the connection
    try:
        from src.llm_client import LLMClient
        
        # Set environment for Gemini
        os.environ["USE_GEMINI"] = "true"
        os.environ["GEMINI_API_KEY"] = gemini_key
        
        # Initialize client
        client = LLMClient()
        
        # Test with a simple query
        test_messages = [
            {"role": "user", "content": "Hello! Can you respond with 'Gemini is working!'?"}
        ]
        
        print("\n🧪 Testing Gemini connection...")
        import asyncio
        
        async def test_connection():
            response = await client.call_llm(test_messages)
            print(f"✅ Gemini Response: {response}")
            return True
        
        result = asyncio.run(test_connection())
        
        if result:
            print("\n🎉 Gemini API is working correctly!")
            print("\n🚀 You can now run the server with:")
            print("   python run_gemini.py")
            print("   or")
            print("   python run_server.py")
            return True
            
    except Exception as e:
        print(f"❌ Error testing Gemini: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure your API key is valid")
        print("2. Check if billing is set up in Google Cloud Console")
        print("3. Ensure Gemini API is enabled")
        return False

def create_env_file():
    """Create a .env file with Gemini configuration"""
    
    env_content = """# LLM Configuration
OPENAI_API_KEY=demo_key
OPENAI_MODEL=gpt-4-turbo-preview

# Gemini Configuration - Set this to true to use Gemini
USE_GEMINI=true
GEMINI_API_KEY=your_gemini_api_key_here

# Web Server Configuration
WEB_HOST=0.0.0.0
WEB_PORT=8000
WEB_DEBUG=false

# Security Configuration
SECRET_KEY=your-secret-key-here
ENCRYPTION_KEY=your-encryption-key-here

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=./logs/agentic_mentor.log

# Vector Store Configuration
VECTOR_STORE_TYPE=chroma
CHROMA_PERSIST_DIRECTORY=./data/chroma

# Database Configuration
DATABASE_URL=sqlite:///./data/agentic_mentor.db
REDIS_URL=redis://localhost:6379

# Agent Configuration
AGENT_MEMORY_SIZE=1000
AGENT_REFLECTION_ENABLED=true
AGENT_LEARNING_RATE=0.1

# Search Configuration
SEARCH_MAX_RESULTS=10
SEARCH_SIMILARITY_THRESHOLD=0.7

# Crawler Configuration
CRAWLER_MAX_DEPTH=3
CRAWLER_DELAY=1.0
CRAWLER_TIMEOUT=30

# Rate Limiting
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=3600
"""
    
    try:
        with open(".env", "w") as f:
            f.write(env_content)
        print("✅ Created .env file with Gemini configuration")
        print("📝 Edit the .env file and replace 'your_gemini_api_key_here' with your actual API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Setup Agentic Mentor with Gemini API")
    parser.add_argument("--create-env", action="store_true", help="Create .env file")
    parser.add_argument("--test", action="store_true", help="Test Gemini connection")
    
    args = parser.parse_args()
    
    if args.create_env:
        create_env_file()
    elif args.test:
        setup_gemini()
    else:
        print("🔧 Gemini Setup Options:")
        print("1. Create .env file: python setup_gemini.py --create-env")
        print("2. Test connection: python setup_gemini.py --test")
        print("3. Run both: python setup_gemini.py --create-env --test") 