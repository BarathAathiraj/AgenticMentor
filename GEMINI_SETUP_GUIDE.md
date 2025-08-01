# 🚀 Complete Guide: Using Gemini API with Agentic Mentor

## 📋 Overview

Your Agentic Mentor project is already configured to support multiple LLM providers including **Google Gemini**. This guide will help you set up and use Gemini API for all responses.

## 🔧 Current Architecture Analysis

### ✅ **What's Already Working:**
- **Multi-LLM Support**: The `LLMClient` class automatically switches between OpenAI, Gemini, and Grok
- **Configuration Management**: Uses Pydantic settings with environment variable support
- **Web Interface**: FastAPI server with chat interface
- **Vector Store**: ChromaDB for semantic search
- **Agents**: QA, Crawler, Memory, and Reflection agents

### 🎯 **Key Files:**
- `src/config.py` - Configuration management
- `src/llm_client.py` - LLM client with Gemini support
- `src/main.py` - Main application
- `run_gemini.py` - Pre-configured Gemini runner

## 🚀 Quick Setup (3 Steps)

### Step 1: Get Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the generated key (starts with `AIza...`)

### Step 2: Configure Environment
```bash
# Option A: Set environment variable
set GEMINI_API_KEY=your_actual_api_key_here

# Option B: Create .env file
python setup_gemini.py --create-env
# Then edit .env file and replace the placeholder
```

### Step 3: Test and Run
```bash
# Test the connection
python setup_gemini.py --test

# Run the server
python run_gemini.py
```

## 🔍 Detailed Configuration

### Environment Variables for Gemini:
```bash
# Enable Gemini
USE_GEMINI=true

# Your API key
GEMINI_API_KEY=your_actual_api_key_here

# Optional: Override default model
GEMINI_MODEL=gemini-1.5-flash
```

### Configuration Priority:
1. **USE_GEMINI=true** + **GEMINI_API_KEY** → Uses Gemini
2. **USE_GROK=true** + **GROK_API_KEY** → Uses Grok  
3. **OPENAI_API_KEY** → Uses OpenAI
4. **Fallback** → Demo mode

## 🧪 Testing Your Setup

### 1. Test API Connection:
```bash
python setup_gemini.py --test
```

### 2. Test with Simple Query:
```python
from src.llm_client import LLMClient
import asyncio

async def test():
    client = LLMClient()
    response = await client.call_llm([
        {"role": "user", "content": "Hello! Test response."}
    ])
    print(response)

asyncio.run(test())
```

### 3. Check Server Status:
```bash
# Start server
python run_gemini.py

# Check health endpoint
curl http://localhost:8000/api/health
```

## 🌐 Using the Web Interface

### 1. Start the Server:
```bash
python run_gemini.py --port 8000
```

### 2. Access Web Interface:
- **Main Interface**: http://localhost:8000
- **Chat Interface**: http://localhost:8000/chat
- **API Endpoints**: http://localhost:8000/api/

### 3. Test Queries:
Try these example queries:
- "How do we handle authentication in our React apps?"
- "What's our state management strategy?"
- "How do we handle database migrations?"

## 🔧 Advanced Configuration

### Custom Gemini Model:
```python
# In src/llm_client.py, line 30
self.gemini_client = genai.GenerativeModel('gemini-1.5-pro')  # or 'gemini-1.5-flash'
```

### Temperature and Token Settings:
```python
# In src/llm_client.py, _call_gemini method
generation_config=genai.types.GenerationConfig(
    temperature=0.7,        # Adjust creativity (0.0-1.0)
    max_output_tokens=1000, # Adjust response length
    top_p=0.9,             # Nucleus sampling
    top_k=40,              # Top-k sampling
)
```

## 🐛 Troubleshooting

### Common Issues:

#### 1. "Invalid API Key"
```bash
# Solution: Get a new key from Google AI Studio
# Make sure it starts with 'AIza...' and is longer than 40 characters
```

#### 2. "Billing Not Set Up"
```bash
# Solution: Set up billing in Google Cloud Console
# Go to: https://console.cloud.google.com/billing
```

#### 3. "API Not Enabled"
```bash
# Solution: Enable Gemini API
# Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
```

#### 4. "Quota Exceeded"
```bash
# Solution: Check usage limits or upgrade billing plan
# Go to: https://console.cloud.google.com/apis/credentials
```

### Debug Mode:
```bash
# Enable debug logging
set LOG_LEVEL=DEBUG
python run_gemini.py
```

## 📊 Monitoring and Analytics

### Check System Status:
```bash
curl http://localhost:8000/api/stats
```

### View Logs:
```bash
# Check application logs
tail -f ./logs/agentic_mentor.log
```

### Monitor API Usage:
- Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- Check API usage and quotas

## 🚀 Production Deployment

### Environment Variables:
```bash
# Production settings
USE_GEMINI=true
GEMINI_API_KEY=your_production_key
WEB_HOST=0.0.0.0
WEB_PORT=8000
LOG_LEVEL=INFO
SECRET_KEY=your_secure_secret_key
```

### Docker Support:
```dockerfile
# Add to your Dockerfile
ENV USE_GEMINI=true
ENV GEMINI_API_KEY=your_key
```

## 🎯 Next Steps

### 1. **Add Knowledge Sources:**
- Configure GitHub integration
- Set up Jira/Confluence crawling
- Add Slack integration

### 2. **Customize Agents:**
- Modify QA agent prompts
- Adjust reflection agent behavior
- Configure memory settings

### 3. **Scale Up:**
- Add more vector stores (Pinecone)
- Implement caching with Redis
- Add monitoring and analytics

## 📞 Support

If you encounter issues:
1. Check the logs: `./logs/agentic_mentor.log`
2. Test API connection: `python setup_gemini.py --test`
3. Verify environment variables: `echo $GEMINI_API_KEY`
4. Check Google Cloud Console for API status

---

**🎉 You're all set!** Your Agentic Mentor is now configured to use Gemini API for all responses. The system will automatically handle the switching between different LLM providers based on your configuration. 