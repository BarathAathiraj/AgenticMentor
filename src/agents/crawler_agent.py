"""
Crawler Agent for orchestrating knowledge extraction from various sources
"""

from typing import Dict, Any, List
from loguru import logger

from src.agents.base_agent import BaseAgent
from src.models import KnowledgeChunk, CrawlJob, SourceType
from src.knowledge.crawlers import GitHubCrawler, JiraCrawler, ConfluenceCrawler, SlackCrawler
from src.knowledge.vector_store import VectorStore


class CrawlerAgent(BaseAgent):
    """Agent responsible for crawling knowledge from various sources"""
    
    def __init__(self, vector_store: VectorStore):
        super().__init__(
            name="Crawler Agent",
            description="Crawls and indexes knowledge from various sources"
        )
        self.vector_store = vector_store
        self.crawlers = {
            SourceType.GITHUB: GitHubCrawler(),
            SourceType.JIRA: JiraCrawler(),
            SourceType.CONFLUENCE: ConfluenceCrawler(),
            SourceType.SLACK: SlackCrawler()
        }
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a crawling job"""
        source_type = input_data.get("source_type")
        config = input_data.get("config", {})
        
        if not source_type:
            raise ValueError("source_type is required")
        
        try:
            source_type_enum = SourceType(source_type)
        except ValueError:
            raise ValueError(f"Invalid source_type: {source_type}")
        
        self._log_activity("Starting crawl job", {"source_type": source_type})
        
        try:
            # Get appropriate crawler
            crawler = self.crawlers.get(source_type_enum)
            if not crawler:
                raise ValueError(f"No crawler available for source type: {source_type}")
            
            # Crawl the source
            chunks = await crawler.crawl(config)
            
            # Add chunks to vector store
            if chunks:
                chunk_ids = await self.vector_store.add_chunks(chunks)
                self._log_activity("Crawl completed", {
                    "source_type": source_type,
                    "chunks_processed": len(chunks),
                    "chunk_ids": chunk_ids
                })
            else:
                self._log_activity("Crawl completed with no chunks", {"source_type": source_type})
            
            return {
                "source_type": source_type,
                "chunks_processed": len(chunks),
                "chunks": chunks
            }
            
        except Exception as e:
            self._log_error(f"Error in crawler agent: {e}", {"source_type": source_type})
            raise
    
    async def crawl_all_sources(self, configs: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
        """Crawl all configured sources"""
        results = {}
        
        for source_type, config in configs.items():
            try:
                result = await self.process({
                    "source_type": source_type,
                    "config": config
                })
                results[source_type] = result
            except Exception as e:
                self._log_error(f"Error crawling {source_type}: {e}")
                results[source_type] = {"error": str(e)}
        
        return results
    
    async def get_crawl_status(self) -> Dict[str, Any]:
        """Get status of available crawlers"""
        status = {}
        
        for source_type, crawler in self.crawlers.items():
            status[source_type.value] = {
                "available": True,
                "description": f"Crawler for {source_type.value}",
                "config_required": self._get_config_requirements(source_type)
            }
        
        return status
    
    def _get_config_requirements(self, source_type: SourceType) -> List[str]:
        """Get configuration requirements for a source type"""
        requirements = {
            SourceType.GITHUB: ["github_token", "repos"],
            SourceType.JIRA: ["jira_server", "jira_username", "jira_api_token", "projects"],
            SourceType.CONFLUENCE: ["confluence_server", "confluence_username", "confluence_api_token", "spaces"],
            SourceType.SLACK: ["slack_bot_token", "slack_app_token", "channels"]
        }
        
        return requirements.get(source_type, [])
    
    async def validate_config(self, source_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration for a source type"""
        try:
            source_type_enum = SourceType(source_type)
            requirements = self._get_config_requirements(source_type_enum)
            
            missing = []
            for req in requirements:
                if req not in config:
                    missing.append(req)
            
            return {
                "valid": len(missing) == 0,
                "missing_config": missing,
                "source_type": source_type
            }
            
        except ValueError:
            return {
                "valid": False,
                "error": f"Invalid source type: {source_type}",
                "source_type": source_type
            } 