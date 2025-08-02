#!/usr/bin/env python3
"""
QA Agent for Agentic Mentor
Handles question answering and response generation
"""

import asyncio
import logging
from typing import Dict, Any, List
from src.agents.base_agent import BaseAgent
from src.knowledge.vector_store import VectorStore
from src.knowledge.search import SemanticSearch
from src.llm_client import LLMClient
from src.models import Query, SearchResult
from src.utils.enhanced_response_formatter import EnhancedResponseFormatter


class QAAgent(BaseAgent):
    """QA Agent for processing queries and generating responses"""
    
    def __init__(self, vector_store: VectorStore, search_engine: SemanticSearch):
        """Initialize QA Agent with vector store and search engine"""
        super().__init__("QA Agent", "AI-powered question answering agent that provides structured responses")
        self.vector_store = vector_store
        self.search_engine = search_engine
        self.llm_client = LLMClient()
        self.logger = logging.getLogger(__name__)
    
    async def process(self, input_data) -> Dict[str, Any]:
        """Process a user query and generate a response"""
        try:
            # Handle both Query objects and dictionaries
            if hasattr(input_data, 'query_text'):
                # It's a Query object
                query_text = input_data.query_text
                user_id = input_data.user_id
                context = input_data.context or {}
            else:
                # It's a dictionary
                query_text = input_data.get("query_text", "")
                user_id = input_data.get("user_id", "anonymous")
                context = input_data.get("context", {})
            
            if not query_text:
                return {
                    "text": "I didn't receive a valid query. Please try again.",
                    "confidence": 0.0,
                    "reasoning": "Empty query provided",
                    "follow_up": "What would you like to know about?"
                }
            
            # Log activity
            self._log_activity("Processing query")
            
            # Search for relevant knowledge
            # For general queries about projects/repositories, get all chunks
            if any(word in query_text.lower() for word in ['project', 'repository', 'list', 'show', 'what', 'tell me about']):
                search_results = await self.search_engine.get_all_chunks(limit=20)
            else:
                search_results = await self.search_engine.search(query_text, limit=10)
            
            # Generate response
            response = await self._generate_enhanced_response(query_text, search_results)
            
            # Log successful processing
            self._log_activity("Query processed successfully")
            
            # Store in memory
            self._log_activity("Stored memory")
            
            return response
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return {
                "text": f"I encountered an error while processing your query: {str(e)}",
                "confidence": 0.0,
                "reasoning": f"Error occurred: {str(e)}",
                "follow_up": "Please try rephrasing your question."
            }
    
    async def _generate_enhanced_response(self, 
                                        query_text: str, 
                                        search_results: List[SearchResult]) -> Dict[str, Any]:
        """Generate enhanced structured response using the new formatter"""
        
        # Prepare context from search results
        context_text = self._prepare_context(search_results)
        
        # Build enhanced system prompt for crisp responses
        system_prompt = """You are Agentic Mentor, an advanced AI-powered knowledge assistant. 

CRITICAL FORMATTING RULES:
- Keep responses SHORT and CRISP
- Use proper markdown formatting
- Put each sentence on a new line
- Put each bullet point on a single line
- Separate sections with blank lines
- Use ## for main headings
- Use ### for subheadings
- Use bullet points (-) for lists
- Use **bold** for important terms
- Include emojis in headings
- MAXIMUM 3-4 sections per response
- MAXIMUM 3 bullet points per section

MANDATORY STRUCTURE FOR PROJECTS:
## 🚀 [Project Name] Analysis

### 📊 Overview
- **Purpose:** [What it does]
- **Status:** [Development stage]
- **Tech Stack:** [Key technologies]

### 🎯 Key Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

### 💡 Summary
- [Key point 1]
- [Key point 2]

### 🎯 Next Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]

MANDATORY STRUCTURE FOR GENERAL QUERIES:
## 📋 [Topic] Information

### 🎯 Key Points
- [Point 1]
- [Point 2]
- [Point 3]

### 🔧 Technical Details
| Aspect | Details |
|--------|---------|
| **Category** | [Classification] |
| **Technology** | [Tech stack] |

### 💡 Summary
- [Key takeaway 1]
- [Key takeaway 2]

CRITICAL: Keep it SHORT, CRISP, and STRUCTURED. Each sentence on new line. Each bullet on single line."""
        
        # Determine if this is a project-specific query
        is_project_query = any(word in query_text.lower() for word in ['project', 'repository', 'codebase', 'application'])
        
        if is_project_query:
            user_prompt = f"""Query: {query_text}

Context: {context_text}

Provide a SHORT, CRISP, well-structured response:

## 🚀 [Project Name] Analysis

### 📊 Overview
- **Purpose:** [What it does]
- **Status:** [Development stage]
- **Tech Stack:** [Key technologies]

### 🎯 Key Features
- [Feature 1]
- [Feature 2]
- [Feature 3]

### 💡 Summary
- [Key point 1]
- [Key point 2]

### 🎯 Next Steps
1. [Action 1]
2. [Action 2]
3. [Action 3]

CRITICAL: Keep it SHORT and CRISP. Each sentence on new line. Each bullet on single line."""
        else:
            user_prompt = f"""Query: {query_text}

Context: {context_text}

Provide a SHORT, CRISP, well-structured response:

## 📋 [Topic] Information

### 🎯 Key Points
- [Point 1]
- [Point 2]
- [Point 3]

### 🔧 Technical Details
| Aspect | Details |
|--------|---------|
| **Category** | [Classification] |
| **Technology** | [Tech stack] |

### 💡 Summary
- [Key takeaway 1]
- [Key takeaway 2]

CRITICAL: Keep it SHORT and CRISP. Each sentence on new line. Each bullet on single line."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_text = await self._call_llm(messages, temperature=0.3)
        
        # Check if response is valid
        if not response_text or response_text.strip() == "":
            response_text = "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
        
        # Check for generic responses and improve them
        if any(phrase in response_text.lower() for phrase in [
            "no specific context was provided",
            "awaiting further instructions", 
            "further information is needed",
            "general inquiry",
            "n/a",
            "### 💡 **Summary**",
            "### 🎯 **Next Steps**"
        ]):
            # Generate a more helpful response
            response_text = EnhancedResponseFormatter._generate_helpful_fallback_response(query_text)
        
        # Clean up any duplicate sections before enhancing
        response_text = EnhancedResponseFormatter._clean_duplicate_sections(response_text)
        
        # Enhance the response with structured formatting
        response_text = EnhancedResponseFormatter.enhance_response_structure(response_text, query_text, search_results)
        
        # Analyze confidence and extract components
        analysis = await self._analyze_response(response_text, query_text, search_results)
        
        return {
            "text": response_text,
            "confidence": analysis.get("confidence", 0.7),
            "reasoning": analysis.get("reasoning", "Based on available knowledge"),
            "follow_up": analysis.get("follow_up", "What else would you like to know?"),
            "sources": [result.dict() for result in search_results[:3]]  # Limit to 3 sources
        }
    
    def _prepare_context(self, search_results: List[SearchResult]) -> str:
        """Prepare context text from search results"""
        if not search_results:
            return "No specific context found in the knowledge base."
        
        context_parts = []
        context_parts.append("## 📚 **Available Knowledge Sources**")
        context_parts.append("")
        
        for i, result in enumerate(search_results, 1):
            chunk = result.chunk
            context_parts.append(f"### 📄 **Source {i}** (Relevance: {result.similarity_score:.2f})")
            context_parts.append(f"**Type:** {chunk.source_type.value}")
            context_parts.append(f"**Content:** {chunk.content}")
            if chunk.source_url:
                context_parts.append(f"**URL:** {chunk.source_url}")
            if chunk.metadata:
                metadata_str = ", ".join([f"{k}: {v}" for k, v in chunk.metadata.items()])
                context_parts.append(f"**Metadata:** {metadata_str}")
            context_parts.append("")
        
        return "\n".join(context_parts)
    
    async def _analyze_response(self, 
                              response_text: str, 
                              query_text: str,
                              search_results: List[SearchResult]) -> Dict[str, Any]:
        """Analyze response quality and extract components"""
        
        # Simple confidence calculation based on response length and search results
        confidence = min(0.9, 0.3 + (len(response_text) / 1000) + (len(search_results) * 0.1))
        
        # Extract reasoning
        reasoning = f"Generated response based on {len(search_results)} relevant sources"
        
        # Generate crisp follow-up suggestions based on query type
        query_lower = query_text.lower()
        
        if any(word in query_lower for word in ['project', 'repository', 'code']):
            follow_up_suggestions = [
                "Show me the technical architecture",
                "Create a development flowchart",
                "Explain the implementation steps",
                "Compare with similar projects",
                "Show me the project structure"
            ]
        elif any(word in query_lower for word in ['process', 'workflow', 'steps']):
            follow_up_suggestions = [
                "Create a detailed process flowchart",
                "Explain each step in detail",
                "Show me the decision points",
                "Suggest automation opportunities",
                "Analyze efficiency improvements"
            ]
        elif any(word in query_lower for word in ['technology', 'stack', 'framework']):
            follow_up_suggestions = [
                "Create a technology comparison",
                "Explain the architecture diagram",
                "Show dependency relationships",
                "Provide migration guidelines",
                "Show performance benchmarks"
            ]
        else:
            follow_up_suggestions = [
                "Explain this in more detail",
                "Create a flowchart for this",
                "Show me the architecture",
                "Provide implementation steps",
                "Compare with similar topics"
            ]
        
        follow_up = follow_up_suggestions[hash(query_text) % len(follow_up_suggestions)]
        
        return {
            "confidence": confidence,
            "reasoning": reasoning,
            "follow_up": follow_up
        } 