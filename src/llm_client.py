#!/usr/bin/env python3
"""
LLM Client for Agentic Mentor
Handles interactions with different LLM providers
"""

import os
import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from loguru import logger
from src.config import settings

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    logger.warning("Google Generative AI not available. Install with: pip install google-generativeai")

try:
    from groq import Groq
    GROQ_AVAILABLE = True
except ImportError:
    GROQ_AVAILABLE = False
    logger.warning("Groq not available. Install with: pip install groq")


class LLMClient:
    """Client for interacting with different LLM providers"""
    
    def __init__(self):
        """Initialize LLM client"""
        self.provider = self._determine_provider()
        self.logger = logger.bind(client="LLMClient")
        
        if self.provider == "gemini" and GEMINI_AVAILABLE:
            genai.configure(api_key=settings.gemini_api_key)
            self.model = genai.GenerativeModel(settings.gemini_model)
            self.logger.info("Using Google Gemini API")
        elif self.provider == "groq" and GROQ_AVAILABLE:
            self.groq_client = Groq(api_key=settings.grok_api_key)
            self.logger.info("Using Groq API")
        else:
            self.logger.warning("Using fallback OpenAI-compatible API")
    
    def _determine_provider(self) -> str:
        """Determine which LLM provider to use"""
        if settings.use_grok and settings.grok_api_key:
            return "groq"
        elif settings.use_gemini and settings.gemini_api_key:
            return "gemini"
        else:
            return "openai"
    
    async def call_llm(self, 
                      messages: List[Dict[str, str]], 
                      model: Optional[str] = None,
                      temperature: Optional[float] = 0.7,
                      max_tokens: Optional[int] = 1000) -> str:
        """Call the LLM with given messages"""
        try:
            if self.provider == "gemini":
                return await self._call_gemini(messages, temperature, max_tokens)
            elif self.provider == "groq":
                return await self._call_groq(messages, temperature, max_tokens)
            else:
                return await self._call_openai(messages, temperature, max_tokens)
        except Exception as e:
            self.logger.error(f"Error calling LLM: {e}")
            return f"I encountered an error while processing your request: {str(e)}"
    
    async def _call_groq(self, 
                         messages: List[Dict[str, str]], 
                         temperature: Optional[float] = 0.7,
                         max_tokens: Optional[int] = 1000) -> str:
        """Call Groq API"""
        try:
            # Convert messages to Groq format
            groq_messages = []
            for message in messages:
                if message["role"] == "system":
                    groq_messages.append({"role": "system", "content": message["content"]})
                elif message["role"] == "user":
                    groq_messages.append({"role": "user", "content": message["content"]})
                elif message["role"] == "assistant":
                    groq_messages.append({"role": "assistant", "content": message["content"]})
            
            # Call Groq API
            response = self.groq_client.chat.completions.create(
                model=settings.grok_model,
                messages=groq_messages,
                temperature=temperature or 0.7,
                max_tokens=max_tokens or 1000,
                top_p=0.8,
                stream=False
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            self.logger.error(f"Error calling Groq API: {e}")
            raise
    
    async def _call_gemini(self, 
                          messages: List[Dict[str, str]], 
                          temperature: Optional[float] = 0.7,
                          max_tokens: Optional[int] = 1000) -> str:
        """Call Google Gemini API"""
        try:
            # Convert messages to Gemini format
            prompt = ""
            for message in messages:
                if message["role"] == "user":
                    prompt += f"User: {message['content']}\n"
                elif message["role"] == "assistant":
                    prompt += f"Assistant: {message['content']}\n"
                elif message["role"] == "system":
                    prompt += f"System: {message['content']}\n"
            
            # Add instruction for comprehensive responses
            prompt += "\n\nPlease provide a detailed, comprehensive, and well-structured response. Use proper markdown formatting with clear headers (## and ###), bullet points, bold text for emphasis, and organized sections. Make the response professional, scannable, and easy to read. Be thorough and informative while maintaining clarity and structure."
            
            # Ensure parameters are valid
            if temperature is None:
                temperature = 0.7
            else:
                temperature = float(temperature)

            if max_tokens is None:
                max_tokens = 2000
            else:
                max_tokens = int(max_tokens)
            
            max_output_tokens = max(1000, max_tokens)
            
            response = await asyncio.to_thread(
                self.model.generate_content,
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=min(temperature, 0.7),
                    max_output_tokens=max_output_tokens,
                    top_p=0.8,
                    candidate_count=1,
                )
            )
            
            if not response or not response.text:
                return "I apologize, but I couldn't generate a response. Please try again."
            
            return response.text
            
        except Exception as e:
            self.logger.error(f"Error calling Gemini API: {e}")
            raise
    
    async def _call_openai(self, 
                          messages: List[Dict[str, str]], 
                          temperature: Optional[float] = 0.7,
                          max_tokens: Optional[int] = 1000) -> str:
        """Call OpenAI API (fallback)"""
        try:
            # This is a fallback implementation
            return "Demo mode: Please configure a valid API key for OpenAI, Gemini, or Groq."
        except Exception as e:
            self.logger.error(f"Error calling OpenAI API: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get the status of the LLM client"""
        return {
            "provider": self.provider,
            "model": settings.grok_model if self.provider == "groq" else settings.gemini_model if self.provider == "gemini" else settings.openai_model,
            "status": "active",
            "api_key_configured": True
        } 