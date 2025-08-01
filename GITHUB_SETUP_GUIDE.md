# 🔑 GitHub API Setup Guide for Agentic Mentor

## 🎯 **What You'll Get**
- **Enhanced GitHub Crawling** - Extract code, issues, PRs, documentation
- **Code Analysis** - AST parsing, function extraction, dependency analysis
- **Pattern Recognition** - Identify API patterns, error handling, etc.
- **Knowledge Synthesis** - Combine information from multiple sources

## 📋 **Step-by-Step Instructions**

### **Step 1: Access GitHub Settings**
1. **Go to GitHub.com** and sign in to your account
2. **Click your profile picture** in the top-right corner
3. **Select "Settings"** from the dropdown menu

### **Step 2: Navigate to Developer Settings**
1. **Scroll down** in the left sidebar
2. **Click "Developer settings"** (at the bottom)
3. **Click "Personal access tokens"**
4. **Click "Tokens (classic)"**

### **Step 3: Generate New Token**
1. **Click "Generate new token"**
2. **Select "Generate new token (classic)"**
3. **Set token name:** `Agentic Mentor - Internal Knowledge Explorer`
4. **Set expiration:** Choose based on your needs (30 days recommended for testing)

### **Step 4: Configure Token Permissions**

#### **🔍 Repository Access (Required)**
- ✅ **`repo`** - Full control of private repositories
  - Access to private repos
  - Read/write repository contents
  - Access to issues, pull requests, etc.

#### **👥 Organization Access (Recommended)**
- ✅ **`read:org`** - Read organization data
  - Access to organization repositories
  - Read team information

#### **👤 User Access (Required)**
- ✅ **`read:user`** - Read user profile data
  - Access to user information
  - Read email addresses

#### **📊 Additional Permissions (Optional)**
- ✅ **`repo:status`** - Access commit status
- ✅ **`repo_deployment`** - Access deployment status
- ✅ **`public_repo`** - Access public repositories

### **Step 5: Generate and Save Token**
1. **Scroll to bottom** and click **"Generate token"**
2. **⚠️ CRITICAL:** Copy the token immediately! You won't see it again
3. **Save it securely** (password manager recommended)

## 🔧 **Add Token to Agentic Mentor**

### **Method 1: Use the Setup Script**
```bash
python setup_github_config.py --setup
```

### **Method 2: Manual .env Update**
Add these lines to your `.env` file:

```bash
# GitHub Integration
GITHUB_TOKEN=ghp_your_token_here
GITHUB_ORGANIZATION=your_organization_name
GITHUB_REPOS=org/repo1,org/repo2,org/repo3
```

### **Method 3: Direct Environment Variables**
```bash
# Set in PowerShell
$env:GITHUB_TOKEN="ghp_your_token_here"
$env:GITHUB_ORGANIZATION="your_organization_name"
$env:GITHUB_REPOS="org/repo1,org/repo2,org/repo3"
```

## 🧪 **Test Your GitHub Configuration**

### **Run the Test Script**
```bash
python setup_github_config.py --setup
```

### **Expected Output**
```
✅ GitHub connection successful!
   User: your_username
   Name: Your Name
```

## 🎯 **What Agentic Mentor Will Crawl**

### **📁 Repository Content**
- **README files** - Project documentation
- **Code files** - Source code with analysis
- **Configuration files** - Setup and config
- **Documentation** - Wiki pages, docs

### **📋 Issues & Pull Requests**
- **Issue titles and descriptions** - Problem reports
- **PR descriptions** - Code changes and reasoning
- **Comments** - Discussion and context
- **Labels** - Categorization

### **📊 Code Analysis**
- **Function extraction** - Method names and parameters
- **Class analysis** - Object structure
- **Dependency tracking** - Library usage
- **Pattern recognition** - Design patterns

## 🔒 **Security Best Practices**

### **Token Security**
- ✅ **Use environment variables** - Never hardcode in source
- ✅ **Set appropriate expiration** - 30-90 days for testing
- ✅ **Limit permissions** - Only what's needed
- ✅ **Store securely** - Password manager recommended

### **Repository Access**
- ✅ **Private repos** - Ensure token has access
- ✅ **Organization repos** - Verify org permissions
- ✅ **Rate limits** - Respect GitHub API limits

## 🚀 **Next Steps After Setup**

### **1. Test Enhanced Crawler**
```bash
# Start enhanced server
python enhanced_gemini_server.py

# Test GitHub crawling
curl -X POST http://localhost:3002/api/crawl \
  -H "Content-Type: application/json" \
  -d '{"job_type": "github_enhanced", "config": {"repos": ["your-org/your-repo"]}}'
```

### **2. Configure Repositories**
Add your repositories to `.env`:
```bash
GITHUB_REPOS=your-org/frontend-app,your-org/backend-api,your-org/docs
```

### **3. Test Knowledge Synthesis**
```bash
# Test synthesis with GitHub data
curl -X POST http://localhost:3002/api/synthesis \
  -H "Content-Type: application/json" \
  -d '{"query": "How do we handle authentication?", "sources": ["github"]}'
```

## 🎯 **Troubleshooting**

### **Common Issues**

#### **❌ "Bad credentials" error**
- **Solution:** Check token is correct and not expired
- **Action:** Generate new token with proper permissions

#### **❌ "Not found" for repositories**
- **Solution:** Ensure token has access to private repos
- **Action:** Check repository permissions and organization access

#### **❌ Rate limit exceeded**
- **Solution:** GitHub has API rate limits
- **Action:** Wait and retry, or implement rate limiting

#### **❌ "Forbidden" error**
- **Solution:** Token lacks required permissions
- **Action:** Regenerate token with proper scopes

## 💡 **Pro Tips**

1. **Start with public repos** for testing
2. **Use organization tokens** for team access
3. **Monitor API usage** to avoid rate limits
4. **Backup your token** securely
5. **Rotate tokens regularly** for security

## 🎉 **You're Ready!**

Once you have your GitHub token configured, your Agentic Mentor will be able to:
- ✅ **Crawl repositories** intelligently
- ✅ **Analyze code** with AST parsing
- ✅ **Extract patterns** and dependencies
- ✅ **Synthesize knowledge** across sources
- ✅ **Build knowledge graphs** from your codebase

**Next:** Get your GitHub token and run `python setup_github_config.py --setup`! 🚀 