# 🧠 Gemini API Integration Guide

## Overview

This guide shows you how to integrate Google Gemini API with your Agentic Mentor system to use Google's powerful AI model instead of OpenAI.

## 🚀 Quick Setup

### 1. Get Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy your API key (starts with `AIza...`)

### 2. Set Environment Variable

```bash
# Set your Gemini API key
export GEMINI_API_KEY=AIzaSyBIBrDtx1NeL7h0RJzbhPGx7yCzleZF6_I

# Or on Windows
set GEMINI_API_KEY=AIzaSyBIBrDtx1NeL7h0RJzbhPGx7yCzleZF6_I
```

### 3. Install Dependencies

```bash
pip install google-generativeai
```

### 4. Run Agentic Mentor with Gemini

```bash
# Run on port 8000 (default)
python run_gemini.py

# Run on a different port
python run_gemini.py --port 5000
```

## 🔧 Configuration

The system automatically detects Gemini configuration through environment variables:

```bash
# Enable Gemini
USE_GEMINI=true

# Your Gemini API key
GEMINI_API_KEY=your_gemini_api_key_here
```

## 🎯 Benefits of Using Gemini

- **🚀 Speed**: Fast response times with Google's infrastructure
- **💰 Cost**: Competitive pricing compared to other APIs
- **🔒 Security**: Enterprise-grade security from Google
- **🌐 Reliability**: Google's global infrastructure
- **📊 Quality**: State-of-the-art AI model performance
- **🔧 Easy Integration**: Simple API with good documentation

## 🧠 Model Information

**Gemini 1.5 Flash** is Google's latest AI model:
- **Parameters**: 1.5 billion parameters (optimized for speed)
- **Context Window**: 1M tokens
- **Performance**: Excellent for chat and reasoning tasks
- **Speed**: Optimized for fast responses
- **Cost**: Very competitive pricing

## 🔧 Advanced Configuration

### Custom Model Parameters

You can modify the model parameters in `src/llm_client.py`:

```python
response = self.gemini_client.generate_content(
    prompt,
    generation_config=genai.types.GenerationConfig(
        temperature=0.7,           # Creativity (0.0-1.0)
        max_output_tokens=2000,    # Maximum response length
        top_p=0.9,                # Nucleus sampling
        top_k=40,                 # Top-k sampling
    )
)
```

### Different Models

You can use other Gemini models:

1. **gemini-1.5-flash** - Fast, efficient model (default)
2. **gemini-1.5-pro** - More powerful model
3. **gemini-1.0-pro** - Previous generation

Just change the model name in the client:
```python
self.gemini_client = genai.GenerativeModel('gemini-1.5-pro')
```

## 🚨 Troubleshooting

### API Key Issues
- Make sure your API key is correct
- Check if you have billing set up in Google AI Studio
- Verify the API key has the right permissions

### Connection Errors
- Check your internet connection
- Verify the API key is valid
- Try testing with a simple request first

### Rate Limits
- Gemini has generous rate limits
- If you hit limits, wait a moment and try again
- Consider upgrading your plan if needed

### Performance Issues
- Reduce `max_output_tokens` for faster responses
- Lower `temperature` for more focused answers
- Use `gemini-1.5-flash` for speed, `gemini-1.5-pro` for quality

## 📊 Performance Comparison

| Model | Speed | Quality | Cost | Context |
|-------|-------|---------|------|---------|
| GPT-4 | Fast | Excellent | High | 8K tokens |
| Gemini 1.5 Flash | Very Fast | Very Good | Low | 1M tokens |
| Gemini 1.5 Pro | Fast | Excellent | Medium | 1M tokens |

## 🔄 Switching Between OpenAI and Gemini

You can easily switch between providers:

### Use OpenAI (Cloud)
```bash
python run_server.py --port 8000
```

### Use Gemini (Cloud)
```bash
python run_gemini.py --port 8000
```

## 🎯 Use Cases for Gemini

- **💬 Chat Applications**: Excellent conversational AI
- **📝 Content Generation**: High-quality text generation
- **🔍 Information Retrieval**: Good at finding and summarizing information
- **🧠 Reasoning Tasks**: Strong logical reasoning capabilities
- **🌐 Multilingual**: Good support for multiple languages
- **📊 Data Analysis**: Can help with data interpretation

## 🚀 Next Steps

1. **Get API key** from Google AI Studio
2. **Set environment variable** with your key
3. **Install dependencies** with `pip install google-generativeai`
4. **Test the connection** with `python test_gemini.py`
5. **Start the server** with `python run_gemini.py`
6. **Access the web interface** at http://localhost:8000

## 🔒 Security Best Practices

- **Never commit API keys** to version control
- **Use environment variables** for configuration
- **Rotate API keys** regularly
- **Monitor usage** in Google AI Studio
- **Set up billing alerts** to avoid unexpected charges

## 📈 Monitoring and Analytics

Google AI Studio provides:
- Usage analytics
- Response times
- Error rates
- Cost tracking
- Model performance metrics

---

**Your Agentic Mentor is now powered by Google Gemini! 🎉** 