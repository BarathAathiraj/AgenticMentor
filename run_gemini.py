#!/usr/bin/env python3
"""
Run Agentic Mentor with Google Gemini API
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def run_with_gemini(port=8000):
    """Run the server with Gemini API configuration"""
    
    # Set environment variables for Gemini
    os.environ.update({
        "WEB_PORT": str(port),
        "OPENAI_API_KEY": "demo_key",
        "SECRET_KEY": "demo-secret-key",
        "ENCRYPTION_KEY": "demo-encryption-key",
        "WEB_HOST": "0.0.0.0",
        "WEB_DEBUG": "false",
        "LOG_LEVEL": "INFO",
        "LOG_FILE": "./logs/agentic_mentor.log",
        "VECTOR_STORE_TYPE": "chroma",
        "CHROMA_PERSIST_DIRECTORY": "./data/chroma",
        "DATABASE_URL": "sqlite:///./data/agentic_mentor.db",
        "REDIS_URL": "redis://localhost:6379",
        "AGENT_MEMORY_SIZE": "1000",
        "AGENT_REFLECTION_ENABLED": "true",
        "AGENT_LEARNING_RATE": "0.1",
        
        # Gemini Configuration
        "USE_GEMINI": "true",
        "GEMINI_API_KEY": os.getenv("GEMINI_API_KEY", "demo_key")
    })
    
    print("🤖" + "="*50 + "🤖")
    print("           AGENTIC MENTOR - Gemini Edition")
    print("🤖" + "="*50 + "🤖")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"📊 Web Interface: http://localhost:{port}")
    print(f"🔧 API Endpoints: http://localhost:{port}/api/")
    print("🧠 Using Google Gemini 1.5 Flash")
    print("=" * 60)
    print("Make sure you have set GEMINI_API_KEY in your environment!")
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Import and run the main application
        from src.main import AgenticMentor
        
        app = AgenticMentor()
        app.run()
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Agentic Mentor with Gemini API")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
    
    args = parser.parse_args()
    
    run_with_gemini(args.port) 