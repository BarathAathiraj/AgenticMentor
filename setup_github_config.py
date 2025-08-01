#!/usr/bin/env python3
"""
GitHub Configuration Setup for Agentic Mentor
"""

import os
import sys
from pathlib import Path

def setup_github_config():
    """Setup GitHub configuration for Agentic Mentor"""
    
    print("🔑 GitHub Configuration Setup for Agentic Mentor")
    print("=" * 50)
    
    # Get GitHub token
    github_token = input("Enter your GitHub Personal Access Token: ").strip()
    if not github_token:
        print("❌ GitHub token is required!")
        return False
    
    # Get organization (optional)
    github_org = input("Enter your GitHub organization name (optional): ").strip()
    
    # Get repositories
    repos_input = input("Enter repository names (comma-separated, e.g., org/repo1,org/repo2): ").strip()
    github_repos = [repo.strip() for repo in repos_input.split(",") if repo.strip()]
    
    # Update .env file
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found!")
        return False
    
    # Read current .env content
    with open(env_file, 'r') as f:
        content = f.read()
    
    # Add or update GitHub configuration
    github_config = f"""
# GitHub Integration
GITHUB_TOKEN={github_token}
"""
    
    if github_org:
        github_config += f"GITHUB_ORGANIZATION={github_org}\n"
    
    if github_repos:
        github_config += f"GITHUB_REPOS={','.join(github_repos)}\n"
    
    # Check if GitHub config already exists
    if "GITHUB_TOKEN=" in content:
        # Update existing config
        lines = content.split('\n')
        new_lines = []
        skip_github = False
        
        for line in lines:
            if line.startswith("GITHUB_TOKEN=") or line.startswith("GITHUB_ORGANIZATION=") or line.startswith("GITHUB_REPOS="):
                if not skip_github:
                    new_lines.extend(github_config.strip().split('\n'))
                    skip_github = True
                continue
            new_lines.append(line)
        
        content = '\n'.join(new_lines)
    else:
        # Add new config
        content += github_config
    
    # Write updated .env file
    with open(env_file, 'w') as f:
        f.write(content)
    
    print("✅ GitHub configuration updated in .env file!")
    print(f"   Token: {github_token[:10]}...")
    if github_org:
        print(f"   Organization: {github_org}")
    if github_repos:
        print(f"   Repositories: {', '.join(github_repos)}")
    
    return True

def test_github_connection():
    """Test GitHub API connection"""
    
    print("\n🧪 Testing GitHub API Connection...")
    
    try:
        import requests
        from src.config import settings
        
        # Test GitHub API
        headers = {
            "Authorization": f"token {settings.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        response = requests.get("https://api.github.com/user", headers=headers)
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub connection successful!")
            print(f"   User: {user_data.get('login', 'Unknown')}")
            print(f"   Name: {user_data.get('name', 'Unknown')}")
            return True
        else:
            print(f"❌ GitHub connection failed: {response.status_code}")
            print(f"   Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing GitHub connection: {e}")
        return False

def show_github_setup_instructions():
    """Show GitHub setup instructions"""
    
    print("\n📋 GitHub Setup Instructions:")
    print("=" * 50)
    print("1. Go to GitHub.com and sign in")
    print("2. Click your profile picture → Settings")
    print("3. Scroll down → Developer settings")
    print("4. Personal access tokens → Tokens (classic)")
    print("5. Generate new token (classic)")
    print("6. Set token name: 'Agentic Mentor'")
    print("7. Select scopes:")
    print("   ✅ repo (Full control of private repositories)")
    print("   ✅ read:org (Read organization data)")
    print("   ✅ read:user (Read user profile data)")
    print("8. Generate token and copy it")
    print("9. Run this script again with your token")

if __name__ == "__main__":
    print("🤖 Agentic Mentor - GitHub Configuration")
    print("=" * 50)
    
    # Check if .env exists
    if not Path(".env").exists():
        print("❌ .env file not found! Please run setup_gemini.py first.")
        sys.exit(1)
    
    # Show instructions if no arguments
    if len(sys.argv) == 1:
        show_github_setup_instructions()
        print("\n💡 Run: python setup_github_config.py --setup")
        sys.exit(0)
    
    # Setup mode
    if "--setup" in sys.argv:
        if setup_github_config():
            test_github_connection()
    else:
        show_github_setup_instructions() 