"""
Reflection Agent for analyzing and improving response quality
"""

from typing import Dict, Any, List, Optional
from loguru import logger

from src.agents.base_agent import BaseAgent
from src.models import Query, AgentResponse, SearchResult
from src.utils.json_parser import parse_llm_json, create_fallback_response


class ReflectionAgent(BaseAgent):
    """Agent responsible for reflecting on and improving response quality"""
    
    def __init__(self):
        super().__init__(
            name="Reflection Agent",
            description="Analyzes responses and suggests improvements"
        )
    
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process a reflection operation"""
        operation = input_data.get("operation")
        
        if operation == "analyze":
            return await self._analyze_response(input_data)
        elif operation == "improve":
            return await self._improve_response(input_data)
        elif operation == "validate":
            return await self._validate_response(input_data)
        else:
            raise ValueError(f"Unknown operation: {operation}")
    
    async def _analyze_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the quality of a response"""
        query = data.get("query")
        response = data.get("response")
        search_results = data.get("search_results", [])
        
        if not query or not response:
            raise ValueError("query and response are required")
        
        analysis = await self._perform_analysis(query, response, search_results)
        
        self._log_activity("Analyzed response", {
            "query_id": query.id,
            "quality_score": analysis["quality_score"],
            "improvement_areas": len(analysis["improvement_areas"])
        })
        
        return analysis
    
    async def _improve_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Improve a response based on analysis"""
        query = data.get("query")
        original_response = data.get("response")
        analysis = data.get("analysis")
        search_results = data.get("search_results", [])
        
        if not query or not original_response or not analysis:
            raise ValueError("query, response, and analysis are required")
        
        improved_response = await self._generate_improved_response(
            query, original_response, analysis, search_results
        )
        
        self._log_activity("Improved response", {
            "query_id": query.id,
            "improvements_made": len(improved_response["improvements"])
        })
        
        return improved_response
    
    async def _validate_response(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if a response is accurate and complete"""
        query = data.get("query")
        response = data.get("response")
        search_results = data.get("search_results", [])
        
        if not query or not response:
            raise ValueError("query and response are required")
        
        validation = await self._perform_validation(query, response, search_results)
        
        self._log_activity("Validated response", {
            "query_id": query.id,
            "is_valid": validation["is_valid"],
            "validation_score": validation["validation_score"]
        })
        
        return validation
    
    async def _perform_analysis(self, 
                               query: Query, 
                               response: AgentResponse,
                               search_results: List[SearchResult]) -> Dict[str, Any]:
        """Perform comprehensive analysis of a response"""
        
        analysis_prompt = f"""Analyze this response to a query and provide a detailed assessment.

Query: {query.query_text}
Response: {response.response_text}
Confidence Score: {response.confidence_score}
Sources Found: {len(search_results)}

Please analyze the response for:
1. Accuracy and relevance to the query
2. Completeness of information
3. Clarity and readability
4. Use of available sources
5. Confidence level appropriateness

IMPORTANT: Respond with ONLY valid JSON, no additional text, formatting, or markdown.
{{
    "quality_score": 0.85,
    "strengths": ["Clear explanation", "Good use of sources"],
    "improvement_areas": ["Could include more examples", "Missing step-by-step process"],
    "accuracy_score": 0.9,
    "completeness_score": 0.7,
    "clarity_score": 0.8,
    "source_utilization_score": 0.9,
    "confidence_appropriateness": 0.85,
    "overall_assessment": "Good response with room for improvement in completeness"
}}"""

        messages = [
            {"role": "system", "content": "You are an AI that analyzes response quality. Respond only with valid JSON, no markdown formatting."},
            {"role": "user", "content": analysis_prompt}
        ]
        
        try:
            analysis_text = await self._call_llm(messages, temperature=0.1)
            
            # Use the robust JSON parser
            expected_keys = ["quality_score", "strengths", "improvement_areas", "accuracy_score", 
                           "completeness_score", "clarity_score", "source_utilization_score", 
                           "confidence_appropriateness", "overall_assessment"]
            parsed_json = parse_llm_json(analysis_text, expected_keys)
            
            if parsed_json:
                return parsed_json
            else:
                # Return fallback response
                return create_fallback_response(expected_keys)
                
        except Exception as e:
            self._log_error(f"Error analyzing response: {e}")
            return create_fallback_response(["quality_score", "strengths", "improvement_areas", "accuracy_score", 
                                         "completeness_score", "clarity_score", "source_utilization_score", 
                                         "confidence_appropriateness", "overall_assessment"])
    
    async def _generate_improved_response(self, 
                                        query: Query, 
                                        original_response: AgentResponse,
                                        analysis: Dict[str, Any],
                                        search_results: List[SearchResult]) -> Dict[str, Any]:
        """Generate an improved version of the response"""
        
        improvement_prompt = f"""Improve this response based on the analysis provided.

Original Query: {query.query_text}
Original Response: {original_response.response_text}

Analysis:
- Quality Score: {analysis.get('quality_score', 0)}
- Strengths: {', '.join(analysis.get('strengths', []))}
- Improvement Areas: {', '.join(analysis.get('improvement_areas', []))}
- Accuracy Score: {analysis.get('accuracy_score', 0)}
- Completeness Score: {analysis.get('completeness_score', 0)}
- Clarity Score: {analysis.get('clarity_score', 0)}

Available Sources: {len(search_results)} sources

Please provide an improved response that addresses the improvement areas while maintaining the strengths. Focus on:
1. Making the response more complete
2. Improving clarity and readability
3. Better utilizing available sources
4. Adding examples where helpful
5. Providing step-by-step guidance where appropriate

Improved Response:"""

        messages = [
            {"role": "system", "content": "You are an AI that improves response quality. Provide clear, helpful, and complete responses."},
            {"role": "user", "content": improvement_prompt}
        ]
        
        try:
            improved_text = await self._call_llm(messages, temperature=0.3)
            
            # Identify specific improvements made
            improvements = await self._identify_improvements(original_response.response_text, improved_text)
            
            return {
                "original_response": original_response.response_text,
                "improved_response": improved_text,
                "improvements": improvements,
                "analysis_used": analysis
            }
            
        except Exception as e:
            self._log_error(f"Error improving response: {e}")
            return {
                "original_response": original_response.response_text,
                "improved_response": original_response.response_text,
                "improvements": ["Unable to improve response"],
                "analysis_used": analysis
            }
    
    async def _perform_validation(self, 
                                query: Query, 
                                response: AgentResponse,
                                search_results: List[SearchResult]) -> Dict[str, Any]:
        """Validate the accuracy and completeness of a response"""
        
        validation_prompt = f"""Validate this response to ensure it's accurate and complete.

Query: {query.query_text}
Response: {response.response_text}
Sources Available: {len(search_results)} sources

Please validate:
1. Does the response accurately answer the query?
2. Is the information factually correct based on the sources?
3. Is the response complete and comprehensive?
4. Are there any missing important details?
5. Is the confidence level appropriate?

IMPORTANT: Respond with ONLY valid JSON, no additional text, formatting, or markdown.
{{
    "is_valid": true,
    "validation_score": 0.9,
    "accuracy_validated": true,
    "completeness_validated": true,
    "confidence_appropriate": true,
    "issues_found": [],
    "missing_information": [],
    "validation_notes": "Response is accurate and complete"
}}"""

        messages = [
            {"role": "system", "content": "You are an AI that validates response accuracy. Respond only with valid JSON, no markdown formatting."},
            {"role": "user", "content": validation_prompt}
        ]
        
        try:
            validation_text = await self._call_llm(messages, temperature=0.1)
            
            # Use the robust JSON parser
            expected_keys = ["is_valid", "validation_score", "accuracy_validated", "completeness_validated", 
                           "confidence_appropriate", "issues_found", "missing_information", "validation_notes"]
            parsed_json = parse_llm_json(validation_text, expected_keys)
            
            if parsed_json:
                return parsed_json
            else:
                # Return fallback response
                return create_fallback_response(expected_keys)
                
        except Exception as e:
            self._log_error(f"Error validating response: {e}")
            return create_fallback_response(["is_valid", "validation_score", "accuracy_validated", "completeness_validated", 
                                         "confidence_appropriate", "issues_found", "missing_information", "validation_notes"])
    
    async def _identify_improvements(self, original: str, improved: str) -> List[str]:
        """Identify specific improvements made to the response"""
        improvements = []
        
        # Check for length improvement
        if len(improved) > len(original) * 1.2:
            improvements.append("Added more detailed information")
        
        # Check for code examples
        if "```" in improved and "```" not in original:
            improvements.append("Added code examples")
        
        # Check for step-by-step structure
        if any(marker in improved.lower() for marker in ["1.", "2.", "3.", "step", "first", "then", "finally"]):
            if not any(marker in original.lower() for marker in ["1.", "2.", "3.", "step", "first", "then", "finally"]):
                improvements.append("Added step-by-step structure")
        
        # Check for examples
        if any(word in improved.lower() for word in ["example", "instance", "case"]) and not any(word in original.lower() for word in ["example", "instance", "case"]):
            improvements.append("Added examples")
        
        # Check for links/references
        if any(word in improved.lower() for word in ["link", "reference", "source"]) and not any(word in original.lower() for word in ["link", "reference", "source"]):
            improvements.append("Added references to sources")
        
        if not improvements:
            improvements.append("Clarified and refined existing content")
        
        return improvements
    
    async def get_reflection_stats(self) -> Dict[str, Any]:
        """Get reflection agent statistics"""
        return {
            "capabilities": [
                "response_analysis",
                "response_improvement", 
                "response_validation",
                "quality_assessment"
            ],
            "analysis_metrics": [
                "quality_score",
                "accuracy_score", 
                "completeness_score",
                "clarity_score",
                "source_utilization_score"
            ]
        } 