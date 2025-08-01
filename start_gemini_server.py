#!/usr/bin/env python3
"""
Start Agentic Mentor server with Gemini API key
"""

import os
import sys
from pathlib import Path

# Set environment variables BEFORE importing any modules
os.environ["GEMINI_API_KEY"] = "AIzaSyAlyO95cDTxdYivhmOtXGKLxXJWzKsYwrM"
os.environ["USE_GEMINI"] = "true"
os.environ["WEB_PORT"] = "3000"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def start_server():
    """Start the server with correct environment variables"""
    
    print("🤖" + "="*50 + "🤖")
    print("           AGENTIC MENTOR - Gemini Edition")
    print("🤖" + "="*50 + "🤖")
    print("🌐 Server will be available at: http://localhost:3000")
    print("📊 Web Interface: http://localhost:3000")
    print("🔧 API Endpoints: http://localhost:3000/api/")
    print("🧠 Using Google Gemini 1.5 Flash")
    print("=" * 60)
    print("✅ Environment variables set:")
    print(f"   GEMINI_API_KEY: {os.environ.get('GEMINI_API_KEY', 'Not set')[:20]}...")
    print(f"   USE_GEMINI: {os.environ.get('USE_GEMINI', 'Not set')}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        # Import and start the server
        from src.main import app
        import uvicorn
        
        # Start the server
        uvicorn.run(
            app.app,  # Use the FastAPI app instance
            host="0.0.0.0",
            port=3000,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 If you see a SentenceTransformer error, try:")
        print("   1. pip install --upgrade sentence-transformers")
        print("   2. Clear the model cache: rm -rf ~/.cache/huggingface")
        sys.exit(1)

if __name__ == "__main__":
    start_server() 