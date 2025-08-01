"""
Utility functions for robust JSON parsing from LLM responses
"""

import json
import re
from typing import Dict, Any, Optional
from loguru import logger


def parse_llm_json(response_text: str, expected_keys: Optional[list] = None) -> Optional[Dict[str, Any]]:
    """
    Parse JSON from LLM response, handling common formatting issues
    
    Args:
        response_text: Raw response from LLM
        expected_keys: List of expected keys to validate JSON structure
    
    Returns:
        Parsed JSON dict or None if parsing fails
    """
    if not response_text or not response_text.strip():
        logger.warning("Empty response text for JSON parsing")
        return None
    
    # Clean the response text
    cleaned_text = response_text.strip()
    
    # Remove markdown code blocks (```json ... ```)
    cleaned_text = re.sub(r'```json\s*', '', cleaned_text)
    cleaned_text = re.sub(r'```\s*$', '', cleaned_text)
    cleaned_text = re.sub(r'^```\s*', '', cleaned_text)
    
    # Also remove any remaining markdown formatting
    cleaned_text = re.sub(r'```\s*', '', cleaned_text)
    cleaned_text = re.sub(r'`\s*', '', cleaned_text)
    
    # Remove any leading/trailing whitespace
    cleaned_text = cleaned_text.strip()
    
    # Try direct JSON parsing first
    try:
        parsed = json.loads(cleaned_text)
        if _validate_json_structure(parsed, expected_keys):
            return parsed
    except json.JSONDecodeError:
        pass
    
    # Try to extract JSON from the response if it's embedded in text
    json_patterns = [
        # Look for JSON with specific expected keys
        r'\{[^{}]*"confidence"[^{}]*"reasoning"[^{}]*"follow_up"[^{}]*\}',
        r'\{[^{}]*"quality_score"[^{}]*"strengths"[^{}]*"improvement_areas"[^{}]*\}',
        # More flexible patterns
        r'\{[^{}]*"confidence"[^{}]*\}',
        r'\{[^{}]*"quality_score"[^{}]*\}',
        # General JSON object patterns - more lenient
        r'\{[^{}]*\}',
        r'\{.*\}',
        # Even more lenient patterns
        r'\{.*"confidence".*\}',
        r'\{.*"quality_score".*\}'
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, cleaned_text, re.DOTALL)
        for match in matches:
            try:
                parsed = json.loads(match)
                if _validate_json_structure(parsed, expected_keys):
                    return parsed
            except json.JSONDecodeError:
                continue
    
    # If still no success, try to fix common JSON issues
    fixed_text = _fix_common_json_issues(cleaned_text)
    try:
        parsed = json.loads(fixed_text)
        if _validate_json_structure(parsed, expected_keys):
            return parsed
    except json.JSONDecodeError:
        pass
    
    logger.warning(f"Failed to parse JSON from LLM response: {response_text[:200]}...")
    return None


def _validate_json_structure(parsed: Dict[str, Any], expected_keys: Optional[list] = None) -> bool:
    """Validate that the parsed JSON has the expected structure"""
    if not isinstance(parsed, dict):
        return False
    
    if expected_keys:
        return all(key in parsed for key in expected_keys)
    
    return True


def _fix_common_json_issues(text: str) -> str:
    """Fix common JSON formatting issues"""
    # Fix unescaped quotes in string values
    text = re.sub(r'([^\\])"([^"]*)"([^"]*)"', r'\1"\2\\"\3"', text)
    
    # Fix missing quotes around keys
    text = re.sub(r'(\s*)(\w+)(\s*):', r'\1"\2"\3:', text)
    
    # Fix trailing commas
    text = re.sub(r',(\s*[}\]])', r'\1', text)
    
    # Fix single quotes to double quotes
    text = text.replace("'", '"')
    
    return text


def create_fallback_response(expected_keys: list) -> Dict[str, Any]:
    """Create a fallback response with default values"""
    fallback_values = {
        "confidence": 0.5,
        "reasoning": "Unable to parse analysis response",
        "follow_up": "Is there anything specific about this topic you'd like to know more about?",
        "quality_score": 0.5,
        "strengths": ["Response provided"],
        "improvement_areas": ["Unable to analyze"],
        "accuracy_score": 0.5,
        "completeness_score": 0.5,
        "clarity_score": 0.5,
        "source_utilization_score": 0.5,
        "confidence_appropriateness": 0.5,
        "overall_assessment": "Unable to analyze response quality"
    }
    
    return {key: fallback_values.get(key, "Unknown") for key in expected_keys} 