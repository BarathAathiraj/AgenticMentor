"""
Memory Agent for learning from past interactions
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from loguru import logger

from src.agents.base_agent import BaseAgent
from src.models import AgentMemory, Query, AgentResponse


class MemoryAgent(BaseAgent):
    """Agent responsible for learning from past interactions"""
    
    def __init__(self, memory_size: int = 1000):
        super().__init__(
            name="Memory Agent",
            description="Learns from past interactions to improve future responses"
        )
        self.memory_size = memory_size
        self.memories: List[AgentMemory] = []
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a memory operation"""
        operation = input_data.get("operation")
        
        if operation == "store":
            return await self._store_memory(input_data)
        elif operation == "retrieve":
            return await self._retrieve_memory(input_data)
        elif operation == "learn":
            return await self._learn_from_interaction(input_data)
        elif operation == "analyze":
            return await self._analyze_patterns(input_data)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def _store_memory(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Store a new memory"""
        query = data.get("query")
        response = data.get("response")
        user_id = data.get("user_id", "anonymous")
        satisfaction_score = data.get("satisfaction_score")
        
        if not query or not response:
            raise ValueError("query and response are required")
        
        # Create memory entry
        memory = AgentMemory(
            id=str(uuid.uuid4()),
            query_id=query.id,
            user_id=user_id,
            query_text=query.query_text,
            response=response.response_text,
            satisfaction_score=satisfaction_score,
            learned_patterns=[],
            timestamp=datetime.utcnow()
        )
        
        # Add to memory (with size limit)
        self.memories.append(memory)
        if len(self.memories) > self.memory_size:
            self.memories.pop(0)  # Remove oldest memory
        
        self._log_activity("Stored memory", {
            "memory_id": memory.id,
            "query_id": query.id,
            "user_id": user_id
        })
        
        return {"memory_id": memory.id, "stored": True}
    
    async def _retrieve_memory(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Retrieve relevant memories"""
        query_text = data.get("query_text")
        user_id = data.get("user_id")
        limit = data.get("limit", 5)
        
        if not query_text:
            raise ValueError("query_text is required")
        
        # Find similar memories
        relevant_memories = []
        for memory in self.memories:
            similarity = self._calculate_similarity(query_text, memory.query_text)
            if similarity > 0.3:  # Threshold for relevance
                relevant_memories.append({
                    "memory": memory,
                    "similarity": similarity
                })
        
        # Sort by similarity and limit results
        relevant_memories.sort(key=lambda x: x["similarity"], reverse=True)
        relevant_memories = relevant_memories[:limit]
        
        self._log_activity("Retrieved memories", {
            "query": query_text,
            "memories_found": len(relevant_memories)
        })
        
        return {
            "memories": relevant_memories,
            "count": len(relevant_memories)
        }
    
    async def _learn_from_interaction(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Learn from a completed interaction"""
        query = data.get("query")
        response = data.get("response")
        satisfaction_score = data.get("satisfaction_score")
        feedback = data.get("feedback")
        
        if not query or not response:
            raise ValueError("query and response are required")
        
        # Analyze the interaction for learning
        patterns = await self._extract_patterns(query, response, satisfaction_score, feedback)
        
        # Update existing memory or create new one
        existing_memory = None
        for memory in self.memories:
            if memory.query_id == query.id:
                existing_memory = memory
                break
        
        if existing_memory:
            # Update existing memory
            existing_memory.response = response.response_text
            existing_memory.satisfaction_score = satisfaction_score
            existing_memory.learned_patterns.extend(patterns)
            existing_memory.timestamp = datetime.utcnow()
        else:
            # Create new memory
            memory = AgentMemory(
                id=str(uuid.uuid4()),
                query_id=query.id,
                user_id=query.user_id,
                query_text=query.query_text,
                response=response.response_text,
                satisfaction_score=satisfaction_score,
                learned_patterns=patterns,
                timestamp=datetime.utcnow()
            )
            self.memories.append(memory)
        
        self._log_activity("Learned from interaction", {
            "query_id": query.id,
            "patterns_learned": len(patterns)
        })
        
        return {
            "learned": True,
            "patterns_learned": patterns
        }
    
    async def _analyze_patterns(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze patterns in memory"""
        time_period = data.get("time_period", 30)  # days
        min_occurrences = data.get("min_occurrences", 3)
        
        cutoff_date = datetime.utcnow() - timedelta(days=time_period)
        recent_memories = [m for m in self.memories if m.timestamp >= cutoff_date]
        
        # Analyze query patterns
        query_patterns = {}
        response_patterns = {}
        satisfaction_trends = []
        
        for memory in recent_memories:
            # Query patterns
            words = memory.query_text.lower().split()
            for word in words:
                if len(word) > 3:  # Skip short words
                    query_patterns[word] = query_patterns.get(word, 0) + 1
            
            # Response patterns
            if memory.satisfaction_score:
                satisfaction_trends.append(memory.satisfaction_score)
        
        # Filter patterns by minimum occurrences
        common_query_patterns = {
            word: count for word, count in query_patterns.items() 
            if count >= min_occurrences
        }
        
        # Calculate average satisfaction
        avg_satisfaction = sum(satisfaction_trends) / len(satisfaction_trends) if satisfaction_trends else 0
        
        return {
            "time_period_days": time_period,
            "total_interactions": len(recent_memories),
            "common_query_patterns": common_query_patterns,
            "average_satisfaction": avg_satisfaction,
            "satisfaction_trend": satisfaction_trends
        }
    
    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calculate similarity between two texts"""
        # Simple word overlap similarity
        words1 = set(text1.lower().split())
        words2 = set(text2.lower().split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    async def _extract_patterns(self, 
                               query: Query, 
                               response: AgentResponse,
                               satisfaction_score: Optional[int],
                               feedback: Optional[str]) -> List[str]:
        """Extract learning patterns from an interaction"""
        patterns = []
        
        # Pattern: High satisfaction with detailed responses
        if satisfaction_score and satisfaction_score >= 4:
            if len(response.response_text) > 200:
                patterns.append("detailed_responses_high_satisfaction")
        
        # Pattern: Low satisfaction with short responses
        if satisfaction_score and satisfaction_score <= 2:
            if len(response.response_text) < 100:
                patterns.append("short_responses_low_satisfaction")
        
        # Pattern: Technical queries need code examples
        technical_keywords = ["code", "implementation", "api", "database", "config"]
        if any(keyword in query.query_text.lower() for keyword in technical_keywords):
            if "```" in response.response_text:
                patterns.append("technical_queries_need_code_examples")
        
        # Pattern: Questions about processes need step-by-step answers
        process_keywords = ["how to", "process", "steps", "procedure"]
        if any(keyword in query.query_text.lower() for keyword in process_keywords):
            if "1." in response.response_text or "step" in response.response_text.lower():
                patterns.append("process_queries_need_step_by_step")
        
        # Pattern: High confidence with multiple sources
        if response.confidence_score > 0.8 and len(response.sources) > 2:
            patterns.append("high_confidence_with_multiple_sources")
        
        return patterns
    
    async def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        total_memories = len(self.memories)
        
        if not total_memories:
            return {"total_memories": 0}
        
        # Calculate satisfaction statistics
        satisfaction_scores = [m.satisfaction_score for m in self.memories if m.satisfaction_score]
        avg_satisfaction = sum(satisfaction_scores) / len(satisfaction_scores) if satisfaction_scores else 0
        
        # Count patterns
        all_patterns = []
        for memory in self.memories:
            all_patterns.extend(memory.learned_patterns)
        
        pattern_counts = {}
        for pattern in all_patterns:
            pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        
        return {
            "total_memories": total_memories,
            "average_satisfaction": avg_satisfaction,
            "pattern_counts": pattern_counts,
            "memory_size_limit": self.memory_size
        } 