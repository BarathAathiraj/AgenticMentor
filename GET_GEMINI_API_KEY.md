# 🔑 How to Get a Valid Gemini API Key

## 🚨 Current Issue
The API key you provided (`AIzaSyCxJF9REA5IRri3Se4l21R3MRwfiAzUdKw`) is not valid for Gemini API.

## ✅ Step-by-Step Guide to Get Valid API Key

### 1. Go to Google AI Studio
1. Open your browser and go to: https://makersuite.google.com/app/apikey
2. Sign in with your Google account

### 2. Create API Key
1. Click the **"Create API Key"** button
2. A new API key will be generated
3. **Copy the entire key** (it should start with `AIza...`)

### 3. Verify the Key Format
- ✅ Valid key format: `AIzaSyC...` (longer than the one you provided)
- ❌ Your current key: `AIzaSyCxJF9REA5IRri3Se4l21R3MRwfiAzUdKw` (too short)

### 4. Set Up Billing (Required)
1. Go to: https://console.cloud.google.com/billing
2. Create a new billing account or link existing one
3. Enable billing for the Gemini API

### 5. Enable Gemini API
1. Go to: https://console.cloud.google.com/apis/library/generativelanguage.googleapis.com
2. Click **"Enable"** if not already enabled

## 🔧 Alternative: Use OpenAI Instead

If you want to test the system immediately, you can use OpenAI:

```bash
# Set OpenAI API key instead
set OPENAI_API_KEY=your_openai_api_key_here

# Run with OpenAI
python run_server.py --port 8000
```

## 🧪 Test Your New Key

Once you have a valid key:

```bash
# Set the new key
set GEMINI_API_KEY=your_new_valid_key_here

# Test the connection
python test_gemini.py
```

## 🚨 Common Issues

### 1. Invalid API Key
- **Cause**: Wrong key format or expired key
- **Solution**: Generate new key from Google AI Studio

### 2. Billing Not Set Up
- **Cause**: Gemini API requires billing account
- **Solution**: Set up billing in Google Cloud Console

### 3. API Not Enabled
- **Cause**: Gemini API not enabled in project
- **Solution**: Enable API in Google Cloud Console

### 4. Quota Exceeded
- **Cause**: Hit usage limits
- **Solution**: Wait or upgrade billing plan

## 📞 Need Help?

If you're still having issues:
1. Check the [Google AI Studio documentation](https://ai.google.dev/)
2. Verify your billing is set up correctly
3. Make sure you're using the latest API key

---

**Note**: The API key you provided appears to be either:
- An old/expired key
- A key for a different Google service
- A key that hasn't been properly generated from Google AI Studio

Please follow the steps above to get a fresh, valid API key from Google AI Studio. 