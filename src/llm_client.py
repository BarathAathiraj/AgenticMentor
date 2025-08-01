"""
LLM Client for Agentic Mentor - supports OpenAI, Google Gemini, and Grok
"""

import asyncio
import aiohttp
import json
from typing import List, Dict, Any, Optional
from loguru import logger
from openai import OpenAI
import google.generativeai as genai
from src.config import settings


class LLMClient:
    """Client for interacting with LLMs (OpenAI, Google Gemini, or Grok)"""
    
    def __init__(self):
        self.openai_client = None
        self.gemini_client = None
        self.grok_client = None
        self.use_gemini = False
        self.use_grok = False
        
        # Initialize based on configuration
        if hasattr(settings, 'use_gemini') and settings.use_gemini and settings.gemini_api_key:
            self.use_gemini = True
            genai.configure(api_key=settings.gemini_api_key)
            self.gemini_client = genai.GenerativeModel('gemini-1.5-flash')
            logger.info("Using Google Gemini API")
        elif hasattr(settings, 'use_grok') and settings.use_grok and settings.grok_api_key:
            self.use_grok = True
            self.grok_client = OpenAI(
                api_key=settings.grok_api_key,
                base_url="https://api.x.ai/v1"
            )
            logger.info("Using Grok API")
        else:
            # Default to OpenAI
            if settings.openai_api_key and settings.openai_api_key != "demo_key":
                self.openai_client = OpenAI(api_key=settings.openai_api_key)
                logger.info("Using OpenAI API")
            else:
                logger.warning("No valid API key configured. Using demo mode.")
    
    async def call_llm(
        self, 
        messages: List[Dict[str, str]], 
        temperature: Optional[float] = 0.7, 
        max_tokens: Optional[int] = 1000,
        model: Optional[str] = None
    ) -> str:
        """Call the configured LLM with the given messages"""
        
        try:
            if self.use_gemini:
                return await self._call_gemini(messages, temperature, max_tokens)
            elif self.use_grok:
                return await self._call_grok(messages, temperature, max_tokens)
            elif self.openai_client:
                return await self._call_openai(messages, temperature, max_tokens)
            else:
                return "Demo mode: No valid API key configured. Please set OPENAI_API_KEY, GEMINI_API_KEY, or GROK_API_KEY."
                
        except Exception as e:
            logger.error(f"Error calling LLM: {e}")
            return f"Error: {str(e)}"
    
    async def _call_openai(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> str:
        """Call OpenAI API"""
        try:
            response = await asyncio.to_thread(
                self.openai_client.chat.completions.create,
                model=settings.openai_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI: {e}")
            raise
    
    async def _call_gemini(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> str:
        """Call Google Gemini API with retry logic"""
        max_retries = 3
        retry_delay = 2
        
        # Ensure temperature is a valid float
        if temperature is None:
            temperature = 0.7
        else:
            temperature = float(temperature)
        
        # Ensure max_tokens is a valid int
        if max_tokens is None:
            max_tokens = 2000
        else:
            max_tokens = int(max_tokens)
        
        for attempt in range(max_retries):
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
                
                # Add explicit instruction for JSON responses
                if "JSON" in prompt.upper() or "json" in prompt.lower():
                    prompt += "\n\nCRITICAL: Respond with ONLY valid JSON. Do not include any markdown formatting, code blocks, or additional text. Do not use ```json or ``` formatting."
                else:
                    # Add instruction for comprehensive responses
                    prompt += "\n\nPlease provide a detailed, comprehensive response. Be thorough and informative."
                
                # Ensure max_tokens is positive and reasonable - increase for better responses
                max_output_tokens = max(1000, max_tokens)
                
                response = await asyncio.to_thread(
                    self.gemini_client.generate_content,
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=min(temperature, 0.7),  # Cap temperature for more consistent responses
                        max_output_tokens=max_output_tokens,
                        top_p=0.8,
                        top_k=40,
                        candidate_count=1,
                    )
                )
                
                # Check if response is valid
                if not response or not response.text:
                    logger.warning("Empty response from Gemini API")
                    return "I apologize, but I couldn't generate a response. Please try again."
                
                return response.text
                
            except Exception as e:
                error_str = str(e)
                if "429" in error_str and "quota" in error_str.lower():
                    if attempt < max_retries - 1:
                        logger.warning(f"Rate limit hit, retrying in {retry_delay} seconds... (attempt {attempt + 1}/{max_retries})")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2  # Exponential backoff
                        continue
                    else:
                        logger.error("Rate limit exceeded after all retries")
                        return "I'm currently experiencing high demand. Please try again in a few minutes."
                else:
                    logger.error(f"Error calling Gemini: {e}")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        continue
                    raise
    
    async def _call_grok(self, messages: List[Dict[str, str]], temperature: float, max_tokens: int) -> str:
        """Call Grok API"""
        try:
            response = await asyncio.to_thread(
                self.grok_client.chat.completions.create,
                model=settings.grok_model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling Grok: {e}")
            raise
    
    def get_status(self) -> Dict[str, Any]:
        """Get the status of the LLM client"""
        return {
            "provider": "grok" if self.use_grok else "gemini" if self.use_gemini else "openai",
            "model": settings.grok_model if self.use_grok else "gemini-1.5-flash" if self.use_gemini else settings.openai_model,
            "status": "active" if (self.openai_client or self.gemini_client or self.grok_client) else "inactive",
            "api_key_configured": bool(self.openai_client or self.gemini_client or self.grok_client)
        } 