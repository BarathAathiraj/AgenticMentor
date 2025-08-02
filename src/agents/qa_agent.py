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
        
        # Build enhanced system prompt
        system_prompt = """You are Agentic Mentor, an advanced AI-powered knowledge assistant. 

CRITICAL FORMATTING RULES:
- ALWAYS use proper markdown formatting
- ALWAYS put each sentence on a new line
- ALWAYS put each bullet point on a single line
- ALWAYS separate sections with blank lines
- NEVER put all content in one paragraph
- Use ## for main headings
- Use ### for subheadings
- Use bullet points (-) for lists
- Use **bold** for important terms
- Include emojis in headings

MANDATORY STRUCTURE:
## 🚀 [Project Name] Analysis

### 📊 Overview
- **Key Information:** [Summary]

- **Main Purpose:** [What it does]

- **Current Status:** [Development stage]

### 🔧 Technical Details
| Aspect | Details |
|--------|---------|
| **Technology Stack** | [Technologies] |
| **Architecture** | [System design] |
| **Dependencies** | [Libraries/frameworks] |

### 📈 Process Flow
```mermaid
graph TD
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]
```

### 🎯 Key Features
- **Feature 1:** [Description]

- **Feature 2:** [Description]

### 💡 Summary
- [Key point 1]

- [Key point 2]

CRITICAL: Follow this EXACT structure. Each sentence on new line. Each bullet on single line."""
        
        if search_results:
            user_prompt = f"""Query: {query_text}

Context: {context_text}

Provide a well-structured response using this format:

## 🚀 [Project Name] Analysis

### 📊 Overview
- **Key Information:** [Summary]

- **Main Purpose:** [What it does]

- **Current Status:** [Development stage]

### 🔧 Technical Details
| Aspect | Details |
|--------|---------|
| **Technology Stack** | [Technologies] |
| **Architecture** | [System design] |
| **Dependencies** | [Libraries/frameworks] |

### 📈 Process Flow
```mermaid
graph TD
    A[Start] --> B[Step 1]
    B --> C[Step 2]
    C --> D[End]
```

### 🎯 Key Features
- **Feature 1:** [Description]

- **Feature 2:** [Description]

### 💡 Summary
- [Key point 1]

- [Key point 2]

CRITICAL: Each sentence on new line. Each bullet on single line."""
        else:
            user_prompt = f"""Query: {query_text}

Provide a simple, well-structured response:

## 📋 [Topic] Information

### 🎯 Key Points
- **Point 1:** [Description]

- **Point 2:** [Description]

### 🔧 Technical Details
| Aspect | Details |
|--------|---------|
| **Category** | [Classification] |
| **Technology** | [Tech stack] |

CRITICAL: Each sentence on new line. Each bullet on single line."""
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        response_text = await self._call_llm(messages, temperature=0.3)
        
        # Check if response is valid
        if not response_text or response_text.strip() == "":
            response_text = "I apologize, but I couldn't generate a proper response. Please try rephrasing your question."
        
        # Enhance the response with structured formatting
        response_text = EnhancedResponseFormatter.enhance_response_structure(response_text, query_text, search_results)
        
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
        
        # Generate follow-up suggestions based on query type
        query_lower = query_text.lower()
        
        if any(word in query_lower for word in ['project', 'repository', 'code']):
            follow_up_suggestions = [
                "Would you like me to explain the technical architecture in more detail?",
                "Should I create a flowchart for the development process?",
                "Would you like to see the project structure diagram?",
                "Should I provide implementation steps for this project?",
                "Would you like to compare this with similar projects?"
            ]
        elif any(word in query_lower for word in ['process', 'workflow', 'steps']):
            follow_up_suggestions = [
                "Would you like me to create a detailed process flowchart?",
                "Should I explain each step in more detail?",
                "Would you like to see the decision points in the workflow?",
                "Should I provide automation suggestions for this process?",
                "Would you like to see the efficiency analysis?"
            ]
        elif any(word in query_lower for word in ['technology', 'stack', 'framework']):
            follow_up_suggestions = [
                "Would you like me to create a technology comparison table?",
                "Should I explain the architecture diagram in detail?",
                "Would you like to see the dependency relationships?",
                "Should I provide migration guidelines?",
                "Would you like to see performance benchmarks?"
            ]
        else:
            follow_up_suggestions = [
                "Would you like me to explain any specific aspect in more detail?",
                "Should I create a flowchart for the process flow?",
                "Would you like to see the technical architecture diagram?",
                "Should I provide implementation steps for this?",
                "Would you like to compare this with similar projects?"
            ]
        
        follow_up = follow_up_suggestions[hash(query_text) % len(follow_up_suggestions)]
        
        return {
            "confidence": confidence,
            "reasoning": reasoning,
            "follow_up": follow_up
        } 