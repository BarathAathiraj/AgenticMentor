#!/usr/bin/env python3
"""
API Key Setup Script for Agentic Mentor
Helps users configure all necessary API keys
"""

import os
import json
from pathlib import Path

def setup_api_keys():
    """Interactive API key setup"""
    print("🔑 Agentic Mentor API Key Setup")
    print("=" * 50)
    
    # Load existing .env if it exists
    env_file = Path(".env")
    existing_config = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    existing_config[key] = value
    
    print("\n📋 Required API Keys:")
    print("1. LLM Provider (Choose one)")
    print("2. Optional: GitHub, Jira, Confluence, Slack")
    
    # LLM Configuration
    print("\n🤖 LLM Provider Configuration:")
    print("Which LLM provider would you like to use?")
    print("1. Google Gemini (Recommended)")
    print("2. OpenAI GPT")
    print("3. Grok")
    
    llm_choice = input("Enter your choice (1-3): ").strip()
    
    if llm_choice == "1":
        gemini_key = input("Enter your Gemini API Key (or press Enter to use existing): ").strip()
        if gemini_key:
            existing_config["GEMINI_API_KEY"] = gemini_key
        existing_config["USE_GEMINI"] = "true"
        existing_config["USE_OPENAI"] = "false"
        existing_config["USE_GROK"] = "false"
        print("✅ Gemini configured!")
        
    elif llm_choice == "2":
        openai_key = input("Enter your OpenAI API Key: ").strip()
        if openai_key:
            existing_config["OPENAI_API_KEY"] = openai_key
        existing_config["USE_GEMINI"] = "false"
        existing_config["USE_OPENAI"] = "true"
        existing_config["USE_GROK"] = "false"
        print("✅ OpenAI configured!")
        
    elif llm_choice == "3":
        grok_key = input("Enter your Grok API Key: ").strip()
        if grok_key:
            existing_config["GROK_API_KEY"] = grok_key
        existing_config["USE_GEMINI"] = "false"
        existing_config["USE_OPENAI"] = "false"
        existing_config["USE_GROK"] = "true"
        print("✅ Grok configured!")
    
    # GitHub Integration
    print("\n📚 GitHub Integration (Optional):")
    github_token = input("Enter your GitHub Personal Access Token (or press Enter to skip): ").strip()
    if github_token:
        existing_config["GITHUB_TOKEN"] = github_token
        github_org = input("Enter your GitHub organization name: ").strip()
        if github_org:
            existing_config["GITHUB_ORGANIZATION"] = github_org
        print("✅ GitHub integration configured!")
    
    # Jira Integration
    print("\n📋 Jira Integration (Optional):")
    jira_token = input("Enter your Jira API Token (or press Enter to skip): ").strip()
    if jira_token:
        existing_config["JIRA_API_TOKEN"] = jira_token
        jira_server = input("Enter your Jira server URL (e.g., https://company.atlassian.net): ").strip()
        if jira_server:
            existing_config["JIRA_SERVER"] = jira_server
        jira_username = input("Enter your Jira email: ").strip()
        if jira_username:
            existing_config["JIRA_USERNAME"] = jira_username
        print("✅ Jira integration configured!")
    
    # Confluence Integration
    print("\n📖 Confluence Integration (Optional):")
    confluence_token = input("Enter your Confluence API Token (or press Enter to skip): ").strip()
    if confluence_token:
        existing_config["CONFLUENCE_API_TOKEN"] = confluence_token
        confluence_server = input("Enter your Confluence server URL: ").strip()
        if confluence_server:
            existing_config["CONFLUENCE_SERVER"] = confluence_server
        confluence_username = input("Enter your Confluence email: ").strip()
        if confluence_username:
            existing_config["CONFLUENCE_USERNAME"] = confluence_username
        print("✅ Confluence integration configured!")
    
    # Slack Integration
    print("\n💬 Slack Integration (Optional):")
    slack_bot_token = input("Enter your Slack Bot Token (or press Enter to skip): ").strip()
    if slack_bot_token:
        existing_config["SLACK_BOT_TOKEN"] = slack_bot_token
        slack_app_token = input("Enter your Slack App Token: ").strip()
        if slack_app_token:
            existing_config["SLACK_APP_TOKEN"] = slack_app_token
        print("✅ Slack integration configured!")
    
    # Write configuration to .env file
    print("\n💾 Saving configuration...")
    
    # Start with template
    with open("env.example", 'r') as f:
        template_content = f.read()
    
    # Replace values with user input
    for key, value in existing_config.items():
        template_content = template_content.replace(f"{key}=your_{key.lower()}_here", f"{key}={value}")
        template_content = template_content.replace(f"{key}=your-{key.lower()}-here", f"{key}={value}")
    
    # Write to .env file
    with open(".env", 'w') as f:
        f.write(template_content)
    
    print("✅ Configuration saved to .env file!")
    
    # Show next steps
    print("\n🚀 Next Steps:")
    print("1. Run: python setup_knowledge_base.py")
    print("2. Run: python run_server.py")
    print("3. Visit: http://localhost:3000")
    
    return True

def get_api_key_links():
    """Show links to get API keys"""
    print("\n🔗 API Key Sources:")
    print("• Gemini: https://makersuite.google.com/app/apikey")
    print("• OpenAI: https://platform.openai.com/api-keys")
    print("• GitHub: https://github.com/settings/tokens")
    print("• Jira: https://id.atlassian.com/manage-profile/security/api-tokens")
    print("• Slack: https://api.slack.com/apps")

if __name__ == "__main__":
    try:
        setup_api_keys()
        get_api_key_links()
    except KeyboardInterrupt:
        print("\n\n❌ Setup cancelled.")
    except Exception as e:
        print(f"\n❌ Error: {e}") 