"""
Q&A Agent for handling user queries with RAG
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional
from loguru import logger

from src.agents.base_agent import BaseAgent
from src.models import Query, AgentResponse, SearchResult, KnowledgeChunk
from src.knowledge.vector_store import VectorStore
from src.knowledge.search import SemanticSearch
from src.utils.json_parser import parse_llm_json, create_fallback_response


class QAAgent(BaseAgent):
    """Agent responsible for answering user queries using RAG"""
    
    def __init__(self, vector_store: VectorStore, search_engine: SemanticSearch):
        super().__init__(
            name="Q&A Agent",
            description="Answers user queries using semantic search and RAG"
        )
        self.vector_store = vector_store
        self.search_engine = search_engine
        
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a user query and return a response"""
        query_text = input_data.get("query_text")
        user_id = input_data.get("user_id", "anonymous")
        context = input_data.get("context", {})
        
        if not query_text:
            raise ValueError("query_text is required")
        
        # Create query record
        query = Query(
            id=str(uuid.uuid4()),
            user_id=user_id,
            query_text=query_text,
            context=context,
            timestamp=datetime.utcnow()
        )
        
        self._log_activity("Processing query", {"query_id": query.id, "user_id": user_id})
        
        try:
            # Search for relevant knowledge chunks
            search_results = await self.search_engine.search(query_text, limit=5)
            
            # Generate response using LLM
            response = await self._generate_response(query_text, search_results, context)
            
            # Create agent response
            agent_response = AgentResponse(
                query_id=query.id,
                response_text=response["text"],
                sources=search_results,
                confidence_score=response["confidence"],
                reasoning=response["reasoning"],
                suggested_follow_up=response["follow_up"]
            )
            
            self._log_activity("Query processed successfully", {
                "query_id": query.id,
                "sources_found": len(search_results),
                "confidence": response["confidence"]
            })
            
            return {
                "query": query,
                "response": agent_response,
                "search_results": search_results
            }
            
        except Exception as e:
            self._log_error(f"Error processing query: {e}", {"query_id": query.id})
            raise
    
    async def _generate_response(self, 
                               query_text: str, 
                               search_results: List[SearchResult],
                               context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate response using LLM with retrieved context"""
        
        # Prepare context from search results
        context_text = self._prepare_context(search_results)
        
        # Build prompt
        system_prompt = """You are Agentic Mentor, an AI-powered knowledge assistant. Provide detailed, comprehensive answers that are helpful and informative. Always give thorough explanations and be as detailed as possible while remaining clear and concise."""
        
        if search_results:
            user_prompt = f"""Query: {query_text}

Context: {context_text}

Please provide a detailed and comprehensive answer to the query based on the available information. Be thorough, helpful, and informative. Include relevant details and explanations."""
        else:
            user_prompt = f"""Query: {query_text}

No specific context found in the knowledge base, but you can still provide a helpful response based on your general knowledge about Agentic Mentor and AI systems.

Please provide a detailed and comprehensive answer to the query. Be thorough, helpful, and informative."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_text = await self._call_llm(messages, temperature=0.3)
        
        # Check if response is valid
        if not response_text or response_text.strip() == "":
            response_text = "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
        
        # Analyze confidence and extract components
        analysis = await self._analyze_response(response_text, query_text, search_results)
        
        return {
            "text": response_text,
            "confidence": analysis["confidence"],
            "reasoning": analysis["reasoning"],
            "follow_up": analysis["follow_up"]
        }
    
    def _prepare_context(self, search_results: List[SearchResult]) -> str:
        """Prepare context text from search results"""
        context_parts = []
        
        for i, result in enumerate(search_results, 1):
            chunk = result.chunk
            context_parts.append(f"Source {i} (Relevance: {result.similarity_score:.2f}):")
            context_parts.append(f"Type: {chunk.source_type}")
            context_parts.append(f"Content: {chunk.content}")
            if chunk.source_url:
                context_parts.append(f"URL: {chunk.source_url}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    async def _analyze_response(self, 
                               response_text: str, 
                               query_text: str,
                               search_results: List[SearchResult]) -> Dict[str, Any]:
        """Analyze the response to extract confidence and reasoning"""
        
        analysis_prompt = f"""Analyze this response to a query and provide a JSON response with:
1. Confidence score (0-1) based on how well the response answers the query
2. Brief reasoning for the confidence score
3. A relevant follow-up question

Query: {query_text}
Response: {response_text}
Sources available: {len(search_results)}

CRITICAL: Respond with ONLY valid JSON. Do not include any markdown formatting, code blocks, or additional text. Do not use ```json or ``` formatting. The response must be a valid JSON object.

{{
    "confidence": 0.85,
    "reasoning": "The response directly addresses the query with specific examples and clear explanations",
    "follow_up": "What specific implementation details would you like to know about?"
}}"""

        messages = [
            {"role": "system", "content": "You are an AI that analyzes response quality. Respond only with valid JSON, no markdown formatting."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        try:
            analysis_text = await self._call_llm(messages, temperature=0.1)
            
            # Use the robust JSON parser
            expected_keys = ["confidence", "reasoning", "follow_up"]
            parsed_json = parse_llm_json(analysis_text, expected_keys)
            
            if parsed_json:
                return parsed_json
            else:
                # Return fallback response
                return create_fallback_response(expected_keys)
                
        except Exception as e:
            self._log_error(f"Error analyzing response: {e}")
            return create_fallback_response(["confidence", "reasoning", "follow_up"]) 