"""
Main application for Agentic Mentor
"""

import os
import json
import asyncio
import logging
from datetime import datetime
from typing import Dict, Any, List
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from loguru import logger
import uvicorn

from src.config import settings
from src.knowledge.vector_store import VectorStore
from src.knowledge.search import SemanticSearch
from src.agents.qa_agent import QAAgent
from src.agents.crawler_agent import CrawlerAgent
from src.agents.memory_agent import MemoryAgent
from src.agents.reflection_agent import ReflectionAgent
from src.models import Query


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
        
        # Mount static files
        self.app.mount("/static", StaticFiles(directory="static"), name="static")
        
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
                
                # Create proper Query object with all required fields
                import uuid
                
                query_obj = Query(
                    id=str(uuid.uuid4()),
                    user_id=user_id,
                    query_text=query_text,
                    context=context,
                    timestamp=datetime.now()
                )
                
                # Process query with Q&A agent
                result = await self.qa_agent.process(query_obj)
                
                # Store in memory for learning
                try:
                    await self.memory_agent.process({
                        "operation": "store",
                        "query": query_obj,
                        "response": {
                            "response_text": result.get("text", ""),
                            "confidence_score": result.get("confidence", 0.0),
                            "sources": result.get("sources", []),
                            "suggested_follow_up": result.get("follow_up", "")
                        },
                        "user_id": user_id
                    })
                except Exception as e:
                    logger.warning(f"Failed to store in memory: {e}")
                
                return {
                    "success": True,
                    "query_id": query_obj.id,
                    "response": result.get("text", ""),
                    "confidence": result.get("confidence", 0.0),
                    "sources": result.get("sources", []),
                    "suggested_follow_up": result.get("follow_up", "")
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
        
        @self.app.get("/api/crawl/github")
        async def crawl_github_get(background_tasks: BackgroundTasks):
            """Crawl GitHub repositories using default settings"""
            try:
                repos = settings.github_repos
                organization = settings.github_organization
                
                if not repos and not organization:
                    raise HTTPException(status_code=400, detail="No GitHub configuration found in settings")
                
                # Run GitHub crawling in background
                background_tasks.add_task(self._crawl_github, repos, organization)
                
                return {
                    "success": True,
                    "message": f"GitHub crawling started using default configuration",
                    "repos": repos,
                    "organization": organization
                }
                
            except Exception as e:
                logger.error(f"Error starting GitHub crawl: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/crawl/github")
        async def crawl_github(request: Request, background_tasks: BackgroundTasks):
            """Crawl GitHub repositories"""
            try:
                # Get request body
                body = await request.body()
                if not body:
                    # Use default configuration from settings
                    repos = settings.github_repos
                    organization = settings.github_organization
                else:
                    data = await request.json()
                    repos = data.get("repos", [])
                    organization = data.get("organization", settings.github_organization)
                
                if not repos and not organization:
                    raise HTTPException(status_code=400, detail="Either repos or organization is required")
                
                # Run GitHub crawling and wait for result
                result = await self._crawl_github(repos, organization)
                
                return {
                    "success": result["success"],
                    "chunks": result["chunks"],
                    "message": result["message"],
                    "repos": repos,
                    "organization": organization
                }
                
            except json.JSONDecodeError:
                # Handle empty or invalid JSON
                repos = settings.github_repos
                organization = settings.github_organization
                
                if not repos and not organization:
                    raise HTTPException(status_code=400, detail="No GitHub configuration found in settings")
                
                # Run GitHub crawling and wait for result
                result = await self._crawl_github(repos, organization)
                
                return {
                    "success": result["success"],
                    "chunks": result["chunks"],
                    "message": result["message"],
                    "repos": repos,
                    "organization": organization
                }
                
            except Exception as e:
                logger.error(f"Error starting GitHub crawl: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/crawl/jira")
        async def crawl_jira(request: Request, background_tasks: BackgroundTasks):
            """Crawl Jira projects"""
            try:
                data = await request.json()
                projects = data.get("projects", [])
                
                if not projects:
                    raise HTTPException(status_code=400, detail="Projects list is required")
                
                # Run Jira crawling in background
                background_tasks.add_task(self._crawl_jira, projects)
                
                return {
                    "success": True,
                    "message": f"Jira crawling started for {len(projects)} projects",
                    "projects": projects
                }
                
            except Exception as e:
                logger.error(f"Error starting Jira crawl: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/crawl/confluence")
        async def crawl_confluence(request: Request, background_tasks: BackgroundTasks):
            """Crawl Confluence spaces"""
            try:
                data = await request.json()
                spaces = data.get("spaces", [])
                
                if not spaces:
                    raise HTTPException(status_code=400, detail="Spaces list is required")
                
                # Run Confluence crawling in background
                background_tasks.add_task(self._crawl_confluence, spaces)
                
                return {
                    "success": True,
                    "message": f"Confluence crawling started for {len(spaces)} spaces",
                    "spaces": spaces
                }
                
            except Exception as e:
                logger.error(f"Error starting Confluence crawl: {e}")
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
                
                # Calculate unique sources from source type distribution
                source_distribution = vector_stats.get("source_type_distribution", {})
                unique_sources = len(source_distribution)
                
                # Extract repository information from chunks
                repositories = await self._get_repositories_info()
                
                logger.info(f"Stats response - documents: {vector_stats.get('total_chunks', 0)}, repositories: {len(repositories)}")
                logger.info(f"Repositories list: {repositories}")
                
                return {
                    "success": True,
                    "documents": vector_stats.get("total_chunks", 0),
                    "sources": unique_sources,
                    "repositories": len(repositories),
                    "repositories_list": repositories,
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
        
        @self.app.get("/api/status")
        async def get_status():
            """Get system status"""
            try:
                # Get basic stats
                vector_stats = await self.vector_store.get_stats()
                
                return {
                    "status": "running",
                    "documents_indexed": vector_stats.get("total_chunks", 0),
                    "last_crawl": "recent",  # You can add timestamp tracking
                    "system_health": "good",
                    "timestamp": datetime.utcnow().isoformat()
                }
                
            except Exception as e:
                logger.error(f"Error getting status: {e}")
                return {
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.utcnow().isoformat()
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
    
    async def _crawl_github(self, repos: List[str], organization: str):
        """Crawl GitHub repositories"""
        try:
            result = await self.crawler_agent.process({
                "source_type": "github",
                "config": {
                    "repos": repos,
                    "organization": organization
                }
            })
            
            chunks_processed = result.get('chunks_processed', 0)
            logger.info(f"GitHub crawling completed: {chunks_processed} chunks")
            
            return {
                "success": True,
                "chunks": chunks_processed,
                "message": f"Successfully crawled {chunks_processed} chunks from GitHub repositories"
            }
            
        except Exception as e:
            logger.error(f"Error crawling GitHub: {e}")
            return {
                "success": False,
                "error": str(e),
                "chunks": 0
            }
    
    async def _crawl_jira(self, projects: List[str]):
        """Crawl Jira projects"""
        try:
            result = await self.crawler_agent.process({
                "source_type": "jira",
                "config": {
                    "projects": projects
                }
            })
            
            logger.info(f"Jira crawling completed: {result['chunks_processed']} chunks")
            
        except Exception as e:
            logger.error(f"Error crawling Jira: {e}")
    
    async def _crawl_confluence(self, spaces: List[str]):
        """Crawl Confluence spaces"""
        try:
            result = await self.crawler_agent.process({
                "source_type": "confluence",
                "config": {
                    "spaces": spaces
                }
            })
            
            logger.info(f"Confluence crawling completed: {result['chunks_processed']} chunks")
            
        except Exception as e:
            logger.error(f"Error crawling Confluence: {e}")
    
    async def _get_repositories_info(self) -> List[Dict[str, Any]]:
        """Extract repository information from knowledge chunks"""
        try:
            # Get all chunks from vector store
            all_chunks = await self.vector_store.get_all_chunks()
            
            logger.info(f"Processing {len(all_chunks)} chunks for project extraction")
            logger.info(f"First few chunks: {all_chunks[:2] if all_chunks else 'No chunks'}")
            
            # Group chunks by repository/source
            repo_groups = {}
            
            for i, chunk in enumerate(all_chunks):
                source_id = chunk.get("source_id", "")
                source_type = chunk.get("source_type", "unknown")
                
                logger.debug(f"Chunk {i}: source_id='{source_id}', source_type='{source_type}'")
                
                # Extract project name from source_id
                if "/" in source_id:
                    project_name = source_id.split("/")[0]
                else:
                    project_name = source_id
                
                # Skip empty project names, but use chunk ID as fallback
                if not project_name or project_name == "" or project_name == "unknown":
                    # Use chunk ID as project name if source_id is empty
                    project_name = chunk.get("id", f"project-{i}")
                    logger.debug(f"Using chunk ID as project name: '{project_name}'")
                
                if project_name not in repo_groups:
                    repo_groups[project_name] = {
                        "name": project_name,
                        "documents": 0,
                        "source_type": source_type
                    }
                
                repo_groups[project_name]["documents"] += 1
            
            # Convert to list and sort by document count
            repositories = list(repo_groups.values())
            repositories.sort(key=lambda x: x["documents"], reverse=True)
            
            logger.info(f"Found {len(repositories)} projects: {[r['name'] for r in repositories]}")
            
            # If no projects found, try alternative approach
            if len(repositories) == 0:
                logger.warning("No projects found, checking for alternative source_id patterns")
                for chunk in all_chunks[:5]:  # Check first 5 chunks
                    logger.info(f"Sample chunk: {chunk}")
            
            return repositories
            
        except Exception as e:
            logger.error(f"Error getting repositories info: {e}")
            import traceback
            logger.error(traceback.format_exc())
            return []
    
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