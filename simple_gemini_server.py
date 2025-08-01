#!/usr/bin/env python3
"""
Simple Agentic Mentor server with Gemini API - bypasses vector store loading
"""

import os
import sys
from pathlib import Path

# Set environment variables BEFORE importing any modules
os.environ["GEMINI_API_KEY"] = "AIzaSyAlyO95cDTxdYivhmOtXGKLxXJWzKsYwrM"
os.environ["USE_GEMINI"] = "true"
os.environ["WEB_PORT"] = "3001"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def start_simple_server():
    """Start a simplified server without vector store dependencies"""
    
    print("🤖" + "="*50 + "🤖")
    print("           AGENTIC MENTOR - Simple Gemini Edition")
    print("🤖" + "="*50 + "🤖")
    print("🌐 Server will be available at: http://localhost:3001")
    print("📊 Web Interface: http://localhost:3001")
    print("🔧 API Endpoints: http://localhost:3001/api/")
    print("🧠 Using Google Gemini 1.5 Flash")
    print("=" * 60)
    print("✅ Environment variables set:")
    print(f"   GEMINI_API_KEY: {os.environ.get('GEMINI_API_KEY', 'Not set')[:20]}...")
    print(f"   USE_GEMINI: {os.environ.get('USE_GEMINI', 'Not set')}")
    print("=" * 60)
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    try:
        from fastapi import FastAPI, HTTPException
        from fastapi.responses import HTMLResponse
        from fastapi.staticfiles import StaticFiles
        from fastapi.templating import Jinja2Templates
        from fastapi import Request
        import uvicorn
        from datetime import datetime
        import asyncio
        from typing import Dict, Any
        
        # Import LLM client
        from src.llm_client import LLMClient
        
        # Create FastAPI app
        app = FastAPI(
            title="Agentic Mentor - Simple",
            description="AI-Driven Internal Knowledge Explorer",
            version="1.0.0"
        )
        
        # Setup templates
        templates_dir = "templates"
        os.makedirs(templates_dir, exist_ok=True)
        templates = Jinja2Templates(directory=templates_dir)
        
        # Create static directory
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        
        # Initialize LLM client
        llm_client = LLMClient()
        
        @app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Landing page"""
            return templates.TemplateResponse("landing.html", {"request": request})
        
        @app.get("/chat", response_class=HTMLResponse)
        async def chat(request: Request):
            """Chat interface"""
            return templates.TemplateResponse("index.html", {"request": request})
        
        @app.post("/api/query")
        async def query(request: Request):
            """Handle a user query"""
            try:
                data = await request.json()
                query_text = data.get("query")
                user_id = data.get("user_id", "anonymous")
                
                if not query_text:
                    raise HTTPException(status_code=400, detail="Query text is required")
                
                # Simple response generation without vector store
                messages = [
                    {"role": "system", "content": "You are a helpful AI assistant. Answer questions clearly and concisely."},
                    {"role": "user", "content": query_text}
                ]
                
                response_text = await llm_client.call_llm(messages, temperature=0.3)
                
                return {
                    "success": True,
                    "query_id": f"query_{datetime.utcnow().timestamp()}",
                    "response": response_text,
                    "confidence": 0.8,
                    "sources": [],
                    "suggested_follow_up": "Is there anything else you'd like to know?"
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "response": "I apologize, but I encountered an error. Please try again."
                }
        
        @app.get("/api/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0-simple"
            }
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=3001,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_simple_server() 