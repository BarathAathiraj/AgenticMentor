#!/usr/bin/env python3
"""
Simple script to start Agentic Mentor on any port
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def start_server(port=3000):
    """Start the server on specified port"""
    
    # Set environment variables
    os.environ["WEB_PORT"] = str(port)
    os.environ["OPENAI_API_KEY"] = "demo_key"
    os.environ["SECRET_KEY"] = "demo-secret-key"
    os.environ["ENCRYPTION_KEY"] = "demo-encryption-key"
    
    print("🤖" + "="*50 + "🤖")
    print("           AGENTIC MENTOR - Starting Server")
    print("🤖" + "="*50 + "🤖")
    print(f"🌐 Server will be available at: http://localhost:{port}")
    print(f"📊 Web Interface: http://localhost:{port}")
    print(f"🔧 API Endpoints: http://localhost:{port}/api/")
    print("=" * 60)
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

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Agentic Mentor server")
    parser.add_argument("--port", type=int, default=3000, help="Port to run the server on (default: 3000)")
    
    args = parser.parse_args()
    
    start_server(args.port) 