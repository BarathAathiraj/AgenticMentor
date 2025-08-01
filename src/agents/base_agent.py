"""
Base agent class for Agentic Mentor
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from loguru import logger
from src.llm_client import LLMClient
from src.config import settings


class BaseAgent(ABC):
    """Base class for all agents in the system"""
    
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.llm_client = LLMClient()
        self.logger = logger.bind(agent=name)
        
    @abstractmethod
    async def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and return output"""
        pass
    
    async def _call_llm(self, 
                        messages: List[Dict[str, str]], 
                        model: Optional[str] = None,
                        temperature: float = 0.7) -> str:
        """Call the LLM with given messages"""
        try:
            return await self.llm_client.call_llm(messages, model, temperature)
        except Exception as e:
            self.logger.error(f"Error calling LLM: {e}")
            raise
    
    def _log_activity(self, activity: str, data: Optional[Dict[str, Any]] = None):
        """Log agent activity"""
        self.logger.info(f"Activity: {activity}", extra=data or {})
    
    def _log_error(self, error: str, data: Optional[Dict[str, Any]] = None):
        """Log agent error"""
        self.logger.error(f"Error: {error}", extra=data or {})
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "description": self.description,
            "status": "active"
        } 