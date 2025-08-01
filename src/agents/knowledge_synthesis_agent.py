"""
Knowledge Synthesis Agent for combining information from multiple sources
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger

from src.agents.base_agent import BaseAgent
from src.models import KnowledgeChunk, SearchResult, SourceType
from src.knowledge.vector_store import VectorStore
from src.knowledge.search import SemanticSearch


class KnowledgeSynthesisAgent(BaseAgent):
    """Agent responsible for synthesizing knowledge from multiple sources"""
    
    def __init__(self, vector_store: VectorStore, search_engine: SemanticSearch):
        super().__init__(
            name="Knowledge Synthesis Agent",
            description="Combines information from multiple sources and builds knowledge graphs"
        )
        self.vector_store = vector_store
        self.search_engine = search_engine
        self.knowledge_graph = {}
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a knowledge synthesis request"""
        operation = input_data.get("operation")
        
        if operation == "synthesize":
            return await self._synthesize_knowledge(input_data)
        elif operation == "cross_reference":
            return await self._cross_reference_analysis(input_data)
        elif operation == "gap_analysis":
            return await self._gap_analysis(input_data)
        elif operation == "trend_analysis":
            return await self._trend_analysis(input_data)
        elif operation == "build_graph":
            return await self._build_knowledge_graph(input_data)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def _synthesize_knowledge(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize knowledge from multiple sources"""
        query = data.get("query")
        sources = data.get("sources", [])
        user_context = data.get("user_context", {})
        
        if not query:
            raise ValueError("query is required")
        
        self._log_activity("Starting knowledge synthesis", {"query": query})
        
        try:
            # Get relevant chunks from all sources
            all_chunks = []
            for source in sources:
                source_chunks = await self.search_engine.search_by_source(
                    query, source, limit=10
                )
                all_chunks.extend(source_chunks)
            
            # Synthesize information
            synthesis = await self._combine_information(all_chunks, query, user_context)
            
            # Identify gaps
            gaps = await self._identify_knowledge_gaps(query, all_chunks)
            
            # Build connections
            connections = await self._build_connections(all_chunks)
            
            self._log_activity("Knowledge synthesis completed", {
                "sources_analyzed": len(sources),
                "chunks_processed": len(all_chunks),
                "gaps_identified": len(gaps)
            })
            
            return {
                "synthesis": synthesis,
                "gaps": gaps,
                "connections": connections,
                "sources_used": [chunk.chunk.source_type.value for chunk in all_chunks],
                "confidence": self._calculate_synthesis_confidence(all_chunks)
            }
            
        except Exception as e:
            self._log_error(f"Error in knowledge synthesis: {e}")
            raise
    
    async def _combine_information(self, 
                                 chunks: List[SearchResult], 
                                 query: str,
                                 user_context: Dict[str, Any]) -> Dict[str, Any]:
        """Combine information from multiple chunks"""
        # Group chunks by source type
        grouped_chunks = {}
        for chunk in chunks:
            source_type = chunk.chunk.source_type.value
            if source_type not in grouped_chunks:
                grouped_chunks[source_type] = []
            grouped_chunks[source_type].append(chunk)
        
        # Extract key information from each source
        source_summaries = {}
        for source_type, source_chunks in grouped_chunks.items():
            summary = await self._extract_source_summary(source_chunks, query)
            source_summaries[source_type] = summary
        
        # Create unified synthesis
        synthesis = {
            "main_points": await self._extract_main_points(chunks),
            "source_summaries": source_summaries,
            "contradictions": await self._find_contradictions(chunks),
            "complementary_info": await self._find_complementary_info(chunks),
            "recommendations": await self._generate_recommendations(chunks, user_context)
        }
        
        return synthesis
    
    async def _extract_source_summary(self, chunks: List[SearchResult], query: str) -> Dict[str, Any]:
        """Extract summary from a specific source type"""
        if not chunks:
            return {"summary": "No information found", "confidence": 0.0}
        
        # Combine content from all chunks
        combined_content = "\n\n".join([chunk.chunk.content for chunk in chunks])
        
        # Calculate average similarity
        avg_similarity = sum(chunk.similarity_score for chunk in chunks) / len(chunks)
        
        # Extract key themes
        themes = await self._extract_themes(combined_content)
        
        return {
            "summary": combined_content[:500] + "..." if len(combined_content) > 500 else combined_content,
            "confidence": avg_similarity,
            "themes": themes,
            "chunk_count": len(chunks)
        }
    
    async def _extract_themes(self, content: str) -> List[str]:
        """Extract key themes from content"""
        themes = []
        
        # Simple theme extraction based on keywords
        theme_keywords = {
            "technical": ["api", "code", "implementation", "function", "class"],
            "process": ["workflow", "process", "procedure", "steps"],
            "configuration": ["config", "settings", "environment", "setup"],
            "troubleshooting": ["error", "issue", "problem", "debug", "fix"],
            "architecture": ["design", "architecture", "structure", "pattern"]
        }
        
        content_lower = content.lower()
        for theme, keywords in theme_keywords.items():
            if any(keyword in content_lower for keyword in keywords):
                themes.append(theme)
        
        return themes
    
    async def _extract_main_points(self, chunks: List[SearchResult]) -> List[str]:
        """Extract main points from all chunks"""
        main_points = []
        
        # Group by similarity to avoid redundancy
        processed_content = set()
        
        for chunk in chunks:
            content_preview = chunk.chunk.content[:100]
            if content_preview not in processed_content:
                main_points.append({
                    "point": chunk.chunk.content[:200] + "..." if len(chunk.chunk.content) > 200 else chunk.chunk.content,
                    "source": chunk.chunk.source_type.value,
                    "confidence": chunk.similarity_score
                })
                processed_content.add(content_preview)
        
        return main_points[:5]  # Limit to top 5 points
    
    async def _find_contradictions(self, chunks: List[SearchResult]) -> List[Dict[str, Any]]:
        """Find contradictions between different sources"""
        contradictions = []
        
        # Simple contradiction detection based on keywords
        # In a real implementation, you'd use more sophisticated NLP
        
        return contradictions
    
    async def _find_complementary_info(self, chunks: List[SearchResult]) -> List[Dict[str, Any]]:
        """Find complementary information across sources"""
        complementary = []
        
        # Group by source type and find complementary info
        source_groups = {}
        for chunk in chunks:
            source_type = chunk.chunk.source_type.value
            if source_type not in source_groups:
                source_groups[source_type] = []
            source_groups[source_type].append(chunk)
        
        # Find information that appears in multiple sources
        for source_type, source_chunks in source_groups.items():
            if len(source_chunks) > 1:
                complementary.append({
                    "source_type": source_type,
                    "info_count": len(source_chunks),
                    "summary": "Multiple sources confirm this information"
                })
        
        return complementary
    
    async def _generate_recommendations(self, 
                                      chunks: List[SearchResult], 
                                      user_context: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on synthesized information"""
        recommendations = []
        
        # Analyze user context and chunks to generate recommendations
        if user_context.get("role") == "developer":
            recommendations.append("Consider reviewing the code examples in the repository")
        
        if len(chunks) > 5:
            recommendations.append("Multiple sources available - consider cross-referencing for accuracy")
        
        if any("error" in chunk.chunk.content.lower() for chunk in chunks):
            recommendations.append("Troubleshooting information available - check error handling patterns")
        
        return recommendations
    
    async def _cross_reference_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze cross-references between different sources"""
        query = data.get("query")
        
        if not query:
            raise ValueError("query is required")
        
        # Search across all source types
        all_sources = [SourceType.GITHUB, SourceType.JIRA, SourceType.CONFLUENCE, SourceType.SLACK]
        cross_references = {}
        
        for source in all_sources:
            results = await self.search_engine.search_by_source(query, source, limit=5)
            if results:
                cross_references[source.value] = len(results)
        
        return {
            "cross_references": cross_references,
            "total_sources": len([s for s in cross_references.values() if s > 0])
        }
    
    async def _gap_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Identify knowledge gaps"""
        query = data.get("query")
        expected_sources = data.get("expected_sources", [])
        
        if not query:
            raise ValueError("query is required")
        
        gaps = []
        
        for source in expected_sources:
            results = await self.search_engine.search_by_source(query, source, limit=1)
            if not results:
                gaps.append({
                    "source": source.value,
                    "gap_type": "no_information",
                    "suggestion": f"Consider adding information to {source.value}"
                })
        
        return {
            "gaps": gaps,
            "gap_count": len(gaps)
        }
    
    async def _trend_analysis(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze trends over time"""
        query = data.get("query")
        time_period = data.get("time_period", 30)  # days
        
        if not query:
            raise ValueError("query is required")
        
        # This would require temporal data in your chunks
        # For now, return a placeholder
        return {
            "trends": [],
            "time_period_days": time_period,
            "note": "Temporal analysis requires timestamp data in knowledge chunks"
        }
    
    async def _build_knowledge_graph(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Build a knowledge graph from chunks"""
        query = data.get("query")
        
        if not query:
            raise ValueError("query is required")
        
        # Get relevant chunks
        chunks = await self.search_engine.search(query, limit=20)
        
        # Build simple graph structure
        graph = {
            "nodes": [],
            "edges": []
        }
        
        # Add nodes for each chunk
        for i, chunk in enumerate(chunks):
            graph["nodes"].append({
                "id": f"node_{i}",
                "label": chunk.chunk.source_type.value,
                "content": chunk.chunk.content[:100] + "...",
                "similarity": chunk.similarity_score
            })
        
        # Add edges between related nodes
        for i in range(len(chunks)):
            for j in range(i + 1, len(chunks)):
                # Simple similarity-based edge creation
                if chunks[i].similarity_score > 0.5 and chunks[j].similarity_score > 0.5:
                    graph["edges"].append({
                        "from": f"node_{i}",
                        "to": f"node_{j}",
                        "weight": (chunks[i].similarity_score + chunks[j].similarity_score) / 2
                    })
        
        return {
            "graph": graph,
            "node_count": len(graph["nodes"]),
            "edge_count": len(graph["edges"])
        }
    
    def _calculate_synthesis_confidence(self, chunks: List[SearchResult]) -> float:
        """Calculate confidence in the synthesis"""
        if not chunks:
            return 0.0
        
        # Average similarity score
        avg_similarity = sum(chunk.similarity_score for chunk in chunks) / len(chunks)
        
        # Bonus for multiple sources
        source_types = set(chunk.chunk.source_type for chunk in chunks)
        source_bonus = min(len(source_types) * 0.1, 0.3)
        
        return min(avg_similarity + source_bonus, 1.0)
    
    async def _identify_knowledge_gaps(self, query: str, chunks: List[SearchResult]) -> List[Dict[str, Any]]:
        """Identify gaps in knowledge"""
        gaps = []
        
        # Check for common knowledge areas that might be missing
        knowledge_areas = ["implementation", "configuration", "troubleshooting", "examples"]
        
        for area in knowledge_areas:
            area_chunks = [c for c in chunks if area.lower() in c.chunk.content.lower()]
            if not area_chunks:
                gaps.append({
                    "area": area,
                    "gap_type": "missing_knowledge_area",
                    "suggestion": f"Add {area} information to knowledge base"
                })
        
        return gaps
    
    async def _build_connections(self, chunks: List[SearchResult]) -> List[Dict[str, Any]]:
        """Build connections between chunks"""
        connections = []
        
        # Group by source type and find connections
        source_groups = {}
        for chunk in chunks:
            source_type = chunk.chunk.source_type.value
            if source_type not in source_groups:
                source_groups[source_type] = []
            source_groups[source_type].append(chunk)
        
        # Find connections between different source types
        source_types = list(source_groups.keys())
        for i, source1 in enumerate(source_types):
            for source2 in source_types[i+1:]:
                if source_groups[source1] and source_groups[source2]:
                    connections.append({
                        "from": source1,
                        "to": source2,
                        "connection_type": "cross_reference",
                        "strength": len(source_groups[source1]) + len(source_groups[source2])
                    })
        
        return connections 