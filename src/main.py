"""
Main application for Agentic Mentor
"""

import asyncio
import os
from datetime import datetime
from typing import Dict, Any
from loguru import logger
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request
import uvicorn

from src.config import settings
from src.knowledge.vector_store import VectorStore
from src.knowledge.search import SemanticSearch
from src.agents.qa_agent import QAAgent
from src.agents.crawler_agent import CrawlerAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.reflection_agent import ReflectionAgent


class AgenticMentor:
    """Main application class for Agentic Mentor"""
    
    def __init__(self):
        # Initialize components
        self.vector_store = VectorStore()
        self.search_engine = SemanticSearch(self.vector_store)
        
        # Initialize agents
        self.qa_agent = QAAgent(self.vector_store, self.search_engine)
        self.crawler_agent = CrawlerAgent(self.vector_store)
        self.memory_agent = MemoryAgent(settings.agent_memory_size)
        self.reflection_agent = ReflectionAgent()
        
        # Setup templates
        templates_dir = "templates"
        os.makedirs(templates_dir, exist_ok=True)
        self.templates = Jinja2Templates(directory=templates_dir)
        
        # Create static directory
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        
        # Initialize FastAPI
        self.app = FastAPI(
            title="Agentic Mentor",
            description="AI-Driven Internal Knowledge Explorer",
            version="1.0.0"
        )
        
        # Setup routes
        self._setup_routes()
        
        # Setup logging
        logger.add(
            settings.log_file,
            rotation="1 day",
            retention="30 days",
            level=settings.log_level
        )
    
    def _setup_routes(self):
        """Setup FastAPI routes"""
        
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            """Landing page"""
            return self.templates.TemplateResponse("landing.html", {"request": request})
        
        @self.app.get("/chat", response_class=HTMLResponse)
        async def chat(request: Request):
            """Chat interface"""
            return self.templates.TemplateResponse("index.html", {"request": request})
        
        @self.app.post("/api/query")
        async def query(request: Request):
            """Handle a user query"""
            try:
                data = await request.json()
                query_text = data.get("query")
                user_id = data.get("user_id", "anonymous")
                context = data.get("context", {})
                
                if not query_text:
                    raise HTTPException(status_code=400, detail="Query text is required")
                
                # Process query with Q&A agent
                result = await self.qa_agent.process({
                    "query_text": query_text,
                    "user_id": user_id,
                    "context": context
                })
                
                # Store in memory for learning
                await self.memory_agent.process({
                    "operation": "store",
                    "query": result["query"],
                    "response": result["response"],
                    "user_id": user_id
                })
                
                return {
                    "success": True,
                    "query_id": result["query"].id,
                    "response": result["response"].response_text,
                    "confidence": result["response"].confidence_score,
                    "sources": [
                        {
                            "type": source.chunk.source_type.value,
                            "url": source.chunk.source_url,
                            "similarity": source.similarity_score
                        }
                        for source in result["response"].sources
                    ],
                    "suggested_follow_up": result["response"].suggested_follow_up
                }
                
            except Exception as e:
                logger.error(f"Error processing query: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/crawl")
        async def crawl_sources(request: Request, background_tasks: BackgroundTasks):
            """Crawl knowledge sources"""
            try:
                data = await request.json()
                source_type = data.get("source_type")
                config = data.get("config", {})
                
                if not source_type:
                    raise HTTPException(status_code=400, detail="Source type is required")
                
                # Run crawling in background
                background_tasks.add_task(self._crawl_source, source_type, config)
                
                return {
                    "success": True,
                    "message": f"Crawling started for {source_type}",
                    "source_type": source_type
                }
                
            except Exception as e:
                logger.error(f"Error starting crawl: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/improve")
        async def improve_response(request: Request):
            """Improve a response using reflection agent"""
            try:
                data = await request.json()
                query = data.get("query")
                response = data.get("response")
                search_results = data.get("search_results", [])
                
                if not query or not response:
                    raise HTTPException(status_code=400, detail="Query and response are required")
                
                # Analyze and improve response
                analysis = await self.reflection_agent.process({
                    "operation": "analyze",
                    "query": query,
                    "response": response,
                    "search_results": search_results
                })
                
                improved = await self.reflection_agent.process({
                    "operation": "improve",
                    "query": query,
                    "response": response,
                    "analysis": analysis,
                    "search_results": search_results
                })
                
                return {
                    "success": True,
                    "analysis": analysis,
                    "improved_response": improved["improved_response"],
                    "improvements": improved["improvements"]
                }
                
            except Exception as e:
                logger.error(f"Error improving response: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/stats")
        async def get_stats():
            """Get system statistics"""
            try:
                # Get vector store stats
                vector_stats = await self.vector_store.get_stats()
                
                # Get search stats
                search_stats = await self.search_engine.get_search_stats()
                
                # Get memory stats
                memory_stats = await self.memory_agent.get_memory_stats()
                
                # Get reflection stats
                reflection_stats = await self.reflection_agent.get_reflection_stats()
                
                return {
                    "success": True,
                    "vector_store": vector_stats,
                    "search": search_stats,
                    "memory": memory_stats,
                    "reflection": reflection_stats,
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error getting stats: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.get("/api/health")
        async def health_check():
            """Health check endpoint"""
            return {
                "status": "healthy",
                "timestamp": datetime.utcnow().isoformat(),
                "version": "1.0.0"
            }
    
    async def _crawl_source(self, source_type: str, config: Dict[str, Any]):
        """Crawl a knowledge source"""
        try:
            result = await self.crawler_agent.process({
                "source_type": source_type,
                "config": config
            })
            
            logger.info(f"Crawling completed for {source_type}: {result['chunks_processed']} chunks")
            
        except Exception as e:
            logger.error(f"Error crawling {source_type}: {e}")
    
    def run(self):
        """Run the application"""
        uvicorn.run(
            self.app,
            host=settings.web_host,
            port=settings.web_port,
            log_level=settings.log_level.lower()
        )


# Create main application instance
app = AgenticMentor()

if __name__ == "__main__":
    app.run() 