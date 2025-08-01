#!/usr/bin/env python3
"""
Enhanced Agentic Mentor server with comprehensive AI agents
"""

import os
import sys
from pathlib import Path

# Set environment variables BEFORE importing any modules
os.environ["GEMINI_API_KEY"] = "AIzaSyAlyO95cDTxdYivhmOtXGKLxXJWzKsYwrM"
os.environ["USE_GEMINI"] = "true"
os.environ["WEB_PORT"] = "3002"

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def start_enhanced_server():
    """Start the enhanced server with all agents"""
    
    print("🤖" + "="*50 + "🤖")
    print("           AGENTIC MENTOR - Enhanced Edition")
    print("🤖" + "="*50 + "🤖")
    print("🌐 Server will be available at: http://localhost:3002")
    print("📊 Web Interface: http://localhost:3002")
    print("🔧 API Endpoints: http://localhost:3002/api/")
    print("🧠 Using Google Gemini 1.5 Flash")
    print("🤖 Enhanced Agents: Q&A, Crawler, Synthesis, Memory")
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
        
        # Import all agents
        from src.llm_client import LLMClient
        from src.agents.qa_agent import QAAgent
        from src.agents.enhanced_crawler_agent import EnhancedCrawlerAgent
        from src.agents.knowledge_synthesis_agent import KnowledgeSynthesisAgent
        from src.agents.memory_agent import MemoryAgent
        from src.knowledge.vector_store import VectorStore
        from src.knowledge.search import SemanticSearch
        
        # Create FastAPI app
        app = FastAPI(
            title="Agentic Mentor - Enhanced",
            description="AI-Driven Internal Knowledge Explorer with Multi-Agent System",
            version="2.0.0"
        )
        
        # Setup templates
        templates_dir = "templates"
        os.makedirs(templates_dir, exist_ok=True)
        templates = Jinja2Templates(directory=templates_dir)
        
        # Create static directory
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        
        # Initialize components
        vector_store = VectorStore()
        search_engine = SemanticSearch(vector_store)
        llm_client = LLMClient()
        
        # Initialize all agents
        qa_agent = QAAgent(vector_store, search_engine)
        crawler_agent = EnhancedCrawlerAgent(vector_store)
        synthesis_agent = KnowledgeSynthesisAgent(vector_store, search_engine)
        memory_agent = MemoryAgent()
        
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
            """Handle a user query with enhanced agents"""
            try:
                data = await request.json()
                query_text = data.get("query")
                user_id = data.get("user_id", "anonymous")
                agent_type = data.get("agent_type", "qa")  # qa, synthesis, crawl
                
                if not query_text:
                    raise HTTPException(status_code=400, detail="Query text is required")
                
                # Route to appropriate agent
                if agent_type == "qa":
                    return await _handle_qa_query(qa_agent, query_text, user_id)
                elif agent_type == "synthesis":
                    return await _handle_synthesis_query(synthesis_agent, query_text, user_id)
                elif agent_type == "crawl":
                    return await _handle_crawl_query(crawler_agent, query_text, user_id)
                else:
                    # Default to Q&A with synthesis
                    return await _handle_enhanced_query(
                        qa_agent, synthesis_agent, memory_agent, 
                        query_text, user_id
                    )
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e),
                    "response": "I apologize, but I encountered an error. Please try again."
                }
        
        async def _handle_qa_query(qa_agent, query_text: str, user_id: str):
            """Handle Q&A query"""
            result = await qa_agent.process({
                "query_text": query_text,
                "user_id": user_id
            })
            
            return {
                "success": True,
                "agent_type": "qa",
                "query_id": result["query"].id,
                "response": result["response"].response_text,
                "confidence": result["response"].confidence_score,
                "sources": [s.chunk.source_type.value for s in result["search_results"]],
                "suggested_follow_up": result["response"].suggested_follow_up
            }
        
        async def _handle_synthesis_query(synthesis_agent, query_text: str, user_id: str):
            """Handle knowledge synthesis query"""
            result = await synthesis_agent.process({
                "operation": "synthesize",
                "query": query_text,
                "sources": ["github", "jira", "confluence"],
                "user_context": {"role": "developer"}
            })
            
            return {
                "success": True,
                "agent_type": "synthesis",
                "synthesis": result["synthesis"],
                "gaps": result["gaps"],
                "connections": result["connections"],
                "confidence": result["confidence"]
            }
        
        async def _handle_crawl_query(crawler_agent, query_text: str, user_id: str):
            """Handle crawling query"""
            result = await crawler_agent.process({
                "job_type": "github_enhanced",
                "config": {"repos": ["your-org/your-repo"]}
            })
            
            return {
                "success": True,
                "agent_type": "crawl",
                "job_result": result,
                "message": "Crawling completed successfully"
            }
        
        async def _handle_enhanced_query(qa_agent, synthesis_agent, memory_agent, 
                                       query_text: str, user_id: str):
            """Handle enhanced query with multiple agents"""
            
            # Get Q&A response
            qa_result = await qa_agent.process({
                "query_text": query_text,
                "user_id": user_id
            })
            
            # Get synthesis if multiple sources found
            synthesis_result = None
            if len(qa_result["search_results"]) > 1:
                synthesis_result = await synthesis_agent.process({
                    "operation": "synthesize",
                    "query": query_text,
                    "sources": list(set([s.chunk.source_type.value for s in qa_result["search_results"]])),
                    "user_context": {"role": "developer"}
                })
            
            # Store in memory
            await memory_agent.process({
                "operation": "store",
                "query": qa_result["query"],
                "response": qa_result["response"],
                "user_id": user_id
            })
            
            # Build enhanced response
            enhanced_response = {
                "success": True,
                "agent_type": "enhanced",
                "query_id": qa_result["query"].id,
                "response": qa_result["response"].response_text,
                "confidence": qa_result["response"].confidence_score,
                "sources": [s.chunk.source_type.value for s in qa_result["search_results"]],
                "suggested_follow_up": qa_result["response"].suggested_follow_up
            }
            
            if synthesis_result:
                enhanced_response["synthesis"] = synthesis_result["synthesis"]
                enhanced_response["gaps"] = synthesis_result["gaps"]
            
            return enhanced_response
        
        @app.post("/api/synthesis")
        async def synthesis(request: Request):
            """Knowledge synthesis endpoint"""
            try:
                data = await request.json()
                query_text = data.get("query")
                sources = data.get("sources", ["github", "jira", "confluence"])
                
                if not query_text:
                    raise HTTPException(status_code=400, detail="Query text is required")
                
                result = await synthesis_agent.process({
                    "operation": "synthesize",
                    "query": query_text,
                    "sources": sources,
                    "user_context": data.get("user_context", {})
                })
                
                return {
                    "success": True,
                    "synthesis": result["synthesis"],
                    "gaps": result["gaps"],
                    "connections": result["connections"],
                    "confidence": result["confidence"]
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        @app.post("/api/crawl")
        async def crawl(request: Request):
            """Enhanced crawling endpoint"""
            try:
                data = await request.json()
                job_type = data.get("job_type", "github_enhanced")
                config = data.get("config", {})
                
                result = await crawler_agent.process({
                    "job_type": job_type,
                    "config": config
                })
                
                return {
                    "success": True,
                    "job_result": result
                }
                
            except Exception as e:
                return {
                    "success": False,
                    "error": str(e)
                }
        
        @app.get("/api/agents")
        async def get_agents():
            """Get available agents"""
            return {
                "agents": [
                    {
                        "name": "Q&A Agent",
                        "description": "Answers questions using RAG",
                        "endpoint": "/api/query?agent_type=qa"
                    },
                    {
                        "name": "Knowledge Synthesis Agent",
                        "description": "Combines information from multiple sources",
                        "endpoint": "/api/synthesis"
                    },
                    {
                        "name": "Enhanced Crawler Agent",
                        "description": "Intelligent knowledge extraction",
                        "endpoint": "/api/crawl"
                    },
                    {
                        "name": "Memory Agent",
                        "description": "Learns from past interactions",
                        "endpoint": "internal"
                    }
                ]
            }
        
        @app.get("/api/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "2.0.0-enhanced",
                "agents": ["qa", "synthesis", "crawler", "memory"]
            }
        
        # Start the server
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=3002,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ Error starting enhanced server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    start_enhanced_server() 