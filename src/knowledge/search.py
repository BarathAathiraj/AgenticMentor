"""
Semantic search engine for knowledge retrieval
"""

from typing import List, Optional, Dict, Any
from loguru import logger

from src.models import SearchResult, KnowledgeChunk, SourceType
from src.knowledge.vector_store import VectorStore


class SemanticSearch:
    """Semantic search engine for knowledge retrieval"""
    
    def __init__(self, vector_store: VectorStore):
        self.vector_store = vector_store
        self.logger = logger.bind(component="semantic_search")
    
    async def search(self, 
                    query: str, 
                    limit: int = 10,
                    source_types: Optional[List[SourceType]] = None,
                    filters: Optional[Dict[str, Any]] = None,
                    min_similarity: float = 0.001) -> List[SearchResult]:
        """Search for relevant knowledge chunks"""
        try:
            # Perform vector search
            results = await self.vector_store.search(
                query=query,
                limit=limit * 3,  # Get more results for filtering
                source_types=source_types,
                filters=filters
            )
            
            # Filter by similarity threshold and convert to SearchResult objects
            search_results = []
            for result in results:
                # Use a very low similarity threshold to be more inclusive
                if result["similarity_score"] >= min_similarity:
                    search_result = SearchResult(
                        chunk=result["chunk"],
                        similarity_score=result["similarity_score"],
                        relevance_explanation=self._generate_relevance_explanation(
                            query, result["chunk"], result["similarity_score"]
                        )
                    )
                    search_results.append(search_result)
            
            # If still no results, try with even lower threshold
            if not search_results:
                for result in results:
                    if result["similarity_score"] >= 0.0001:  # Extremely low threshold
                        search_result = SearchResult(
                            chunk=result["chunk"],
                            similarity_score=result["similarity_score"],
                            relevance_explanation=self._generate_relevance_explanation(
                                query, result["chunk"], result["similarity_score"]
                            )
                        )
                        search_results.append(search_result)
            
            # Sort by similarity and limit results
            search_results.sort(key=lambda x: x.similarity_score, reverse=True)
            search_results = search_results[:limit]
            
            self.logger.info(f"Search for '{query}' returned {len(search_results)} results")
            return search_results
            
        except Exception as e:
            self.logger.error(f"Error in semantic search: {e}")
            return []
    
    async def search_by_source(self, 
                             query: str, 
                             source_type: SourceType,
                             limit: int = 10) -> List[SearchResult]:
        """Search within a specific source type"""
        return await self.search(
            query=query,
            limit=limit,
            source_types=[source_type]
        )
    
    async def search_recent(self, 
                          query: str, 
                          days: int = 30,
                          limit: int = 10) -> List[SearchResult]:
        """Search for recent knowledge chunks"""
        from datetime import datetime, timedelta
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        filters = {
            "created_at": {"$gte": cutoff_date.isoformat()}
        }
        
        return await self.search(
            query=query,
            limit=limit,
            filters=filters
        )
    
    async def search_similar(self, 
                           chunk_id: str, 
                           limit: int = 5) -> List[SearchResult]:
        """Find chunks similar to a given chunk"""
        try:
            # Get the reference chunk
            results = await self.vector_store.search(
                query="",  # We'll use the chunk content directly
                limit=1,
                filters={"id": chunk_id}
            )
            
            if not results:
                return []
            
            reference_chunk = results[0]["chunk"]
            
            # Search for similar chunks
            return await self.search(
                query=reference_chunk.content,
                limit=limit + 1  # +1 to account for the reference chunk
            )
            
        except Exception as e:
            self.logger.error(f"Error in similar search: {e}")
            return []
    
    def _generate_relevance_explanation(self, 
                                      query: str, 
                                      chunk: KnowledgeChunk, 
                                      similarity_score: float) -> str:
        """Generate explanation for why a chunk is relevant"""
        explanations = []
        
        # High similarity
        if similarity_score > 0.8:
            explanations.append("Very high semantic similarity")
        elif similarity_score > 0.6:
            explanations.append("High semantic similarity")
        elif similarity_score > 0.4:
            explanations.append("Moderate semantic similarity")
        else:
            explanations.append("Low semantic similarity")
        
        # Source type context
        source_explanations = {
            SourceType.GITHUB: "Code or documentation from repository",
            SourceType.JIRA: "Issue tracking or project management information",
            SourceType.CONFLUENCE: "Documentation or knowledge base article",
            SourceType.SLACK: "Team discussion or communication",
            SourceType.EMAIL: "Email communication or decision",
            SourceType.MANUAL: "Manually added knowledge"
        }
        
        explanations.append(source_explanations.get(chunk.source_type, "Unknown source type"))
        
        # Content length context
        if len(chunk.content) > 1000:
            explanations.append("Detailed content")
        elif len(chunk.content) > 500:
            explanations.append("Moderate detail")
        else:
            explanations.append("Brief content")
        
        return "; ".join(explanations)
    
    async def get_all_chunks(self, limit: int = 50) -> List[SearchResult]:
        """Get all chunks for general queries"""
        try:
            # Use a simple query that should match everything
            results = await self.vector_store.search(
                query="repository project code documentation",
                limit=limit,
                source_types=None,
                filters=None
            )
            
            search_results = []
            for result in results:
                search_result = SearchResult(
                    chunk=result["chunk"],
                    similarity_score=result["similarity_score"],
                    relevance_explanation="General repository information"
                )
                search_results.append(search_result)
            
            return search_results
            
        except Exception as e:
            self.logger.error(f"Error getting all chunks: {e}")
            return []

    async def get_search_stats(self) -> Dict[str, Any]:
        """Get search statistics"""
        try:
            vector_stats = await self.vector_store.get_stats()
            
            return {
                "total_chunks": vector_stats["total_chunks"],
                "source_distribution": vector_stats["source_type_distribution"],
                "search_capabilities": [
                    "semantic_search",
                    "source_filtered_search", 
                    "recent_search",
                    "similar_chunk_search"
                ]
            }
        except Exception as e:
            self.logger.error(f"Error getting search stats: {e}")
            return {"error": str(e)} 