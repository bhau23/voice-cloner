#!/usr/bin/env python3
"""
🚀 GitHub Repository Setup Script for Bhavesh AI Voice Cloner

This script helps you set up the GitHub repository and prepare for deployment.
It will guide you through:
1. Creating a new GitHub repository
2. Setting up remote origin
3. Pushing all code
4. Setting up GitHub Pages (optional)
5. Configuring Streamlit Cloud deployment

Run this after you've completed all your local setup.
"""

import subprocess
import sys
import os
import json
from pathlib import Path

def run_command(command, description, check=True):
    """Run a command with error handling"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return result.stdout.strip()
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return None
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        return None

def check_git_config():
    """Check if Git is configured"""
    print("🔍 Checking Git configuration...")
    
    name = run_command("git config user.name", "Getting Git user name", check=False)
    email = run_command("git config user.email", "Getting Git user email", check=False)
    
    if not name:
        name = input("📝 Enter your Git username: ")
        run_command(f'git config user.name "{name}"', "Setting Git username")
    
    if not email:
        email = input("📧 Enter your Git email: ")
        run_command(f'git config user.email "{email}"', "Setting Git email")
    
    print(f"✅ Git configured for {name} <{email}>")

def create_github_repo():
    """Guide user through GitHub repo creation"""
    print("\n📚 GitHub Repository Setup")
    print("=" * 50)
    
    repo_name = input("📝 Enter repository name (default: voice-cloner): ").strip() or "voice-cloner"
    description = "🎤 Bhavesh AI Voice Cloner - Advanced AI Voice Cloning & Text-to-Speech with Modern Streamlit UI"
    
    print(f"\n🎯 Creating repository: {repo_name}")
    print(f"📄 Description: {description}")
    
    # Check if GitHub CLI is available
    gh_available = run_command("gh --version", "Checking GitHub CLI", check=False)
    
    if gh_available:
        print("\n🚀 GitHub CLI detected! Creating repository automatically...")
        
        # Create repository with GitHub CLI
        create_cmd = f'gh repo create {repo_name} --description "{description}" --public --confirm'
        result = run_command(create_cmd, "Creating GitHub repository")
        
        if result:
            print(f"✅ Repository created: https://github.com/$(gh api user --jq .login)/{repo_name}")
            return f"https://github.com/$(gh api user --jq .login)/{repo_name}.git"
    
    # Manual instructions if GitHub CLI not available
    print("\n📖 Manual GitHub Repository Creation:")
    print("1. Go to https://github.com/new")
    print(f"2. Repository name: {repo_name}")
    print(f"3. Description: {description}")
    print("4. Set to Public")
    print("5. Don't initialize with README (we have our own)")
    print("6. Click 'Create repository'")
    
    repo_url = input("\n🔗 Enter the repository URL (e.g., https://github.com/username/voice-cloner.git): ")
    return repo_url

def setup_git_remote(repo_url):
    """Setup Git remote origin"""
    print(f"\n🔗 Setting up Git remote: {repo_url}")
    
    # Remove existing origin if it exists
    run_command("git remote remove origin", "Removing existing origin", check=False)
    
    # Add new origin
    run_command(f"git remote add origin {repo_url}", "Adding remote origin")
    
    # Verify remote
    remote_check = run_command("git remote -v", "Verifying remote")
    if remote_check:
        print(f"📍 Remote configured:\n{remote_check}")

def push_to_github():
    """Push code to GitHub"""
    print("\n📤 Pushing code to GitHub...")
    
    # Push main branch
    result = run_command("git push -u origin master", "Pushing to GitHub")
    
    if result is not None:
        print("🎉 Code successfully pushed to GitHub!")
        return True
    else:
        print("❌ Failed to push to GitHub. Please check your credentials and try again.")
        return False

def create_streamlit_secrets():
    """Create Streamlit secrets template"""
    secrets_path = Path(".streamlit/secrets.toml")
    
    if not secrets_path.exists():
        print("\n🔐 Creating Streamlit secrets template...")
        
        secrets_content = """# Streamlit Cloud Secrets
# Add any sensitive configuration here
# This file is automatically ignored by Git

[general]
# Add any API keys or sensitive data here
# OPENAI_API_KEY = "your-api-key"
# HUGGINGFACE_TOKEN = "your-token"

[database]
# Database configuration if needed
# DB_URL = "your-database-url"

[auth]
# Authentication settings if needed
# SECRET_KEY = "your-secret-key"
"""
        
        secrets_path.write_text(secrets_content)
        print("✅ Streamlit secrets template created")
        print("⚠️  Remember to configure secrets in Streamlit Cloud dashboard")

def create_deployment_guide():
    """Create deployment guide"""
    guide_path = Path("DEPLOYMENT_GUIDE.md")
    
    if not guide_path.exists():
        print("\n📋 Creating deployment guide...")
        
        guide_content = """# 🚀 Deployment Guide for Bhavesh AI Voice Cloner

## Quick Deployment Options

### 1. Streamlit Cloud (Recommended)
1. Go to [Streamlit Cloud](https://streamlit.io/cloud)
2. Connect your GitHub account
3. Click "New app"
4. Select this repository
5. Set main file path: `streamlit_app.py`
6. Click "Deploy!"

### 2. Heroku
```bash
# Install Heroku CLI
# Create Heroku app
heroku create your-app-name
heroku config:set BUILDPACK_URL=https://github.com/heroku/heroku-buildpack-python
git push heroku master
```

### 3. Docker
```bash
# Build and run locally
docker build -t bhavesh-ai-voice-cloner .
docker run -p 8501:8501 bhavesh-ai-voice-cloner

# Deploy to cloud platforms
docker tag bhavesh-ai-voice-cloner your-registry/bhavesh-ai-voice-cloner
docker push your-registry/bhavesh-ai-voice-cloner
```

### 4. Railway
1. Go to [Railway](https://railway.app)
2. Connect GitHub repository
3. Auto-deploys on push

### 5. Google Cloud Run
```bash
gcloud run deploy --source .
```

## Environment Variables

For production deployment, set these environment variables:
- `STREAMLIT_SHARING_MODE=true`
- `PYTHONPATH=/app/src`

## Performance Optimization

### For GPU-enabled deployments:
- Use CUDA-compatible containers
- Allocate sufficient GPU memory (8GB+ recommended)
- Consider using cloud GPUs (AWS EC2 P3, GCP GPU VMs)

### For CPU-only deployments:
- Increase memory allocation (16GB+ recommended)
- Use multi-core instances
- Consider Redis caching for model loading

## Security Considerations

1. **API Keys**: Store in environment variables or secrets manager
2. **Rate Limiting**: Implement request limits for public deployments
3. **Input Validation**: Validate all user inputs
4. **Content Filtering**: Monitor generated content for abuse

## Monitoring

- Use application monitoring (e.g., Sentry, DataDog)
- Monitor resource usage (CPU, Memory, GPU)
- Set up alerting for errors and performance issues
- Log user interactions for debugging

## Scaling

For high-traffic deployments:
1. Use load balancers
2. Implement horizontal scaling
3. Consider microservices architecture
4. Use CDN for static assets

## Troubleshooting

### Common Issues:
1. **Memory errors**: Increase instance memory
2. **Slow loading**: Implement model caching
3. **CUDA errors**: Ensure GPU compatibility
4. **Import errors**: Check Python path and dependencies

### Support:
- GitHub Issues: https://github.com/bhavesh-ai/voice-cloner/issues
- Email: bhavesh.ai.contact@gmail.com
"""
        
        guide_path.write_text(guide_content)
        print("✅ Deployment guide created")

def main():
    print("🎤 BHAVESH AI VOICE CLONER - GitHub Setup")
    print("=" * 60)
    print()
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Check Git configuration
    check_git_config()
    
    # Create GitHub repository
    repo_url = create_github_repo()
    
    if not repo_url:
        print("❌ Repository URL is required")
        sys.exit(1)
    
    # Setup Git remote
    setup_git_remote(repo_url)
    
    # Create additional deployment files
    create_streamlit_secrets()
    create_deployment_guide()
    
    # Add and commit new files
    run_command("git add .", "Adding new files")
    run_command('git commit -m "📚 Add deployment guides and configuration files"', "Committing changes", check=False)
    
    # Push to GitHub
    if push_to_github():
        print("\n🎉 SUCCESS! Your repository is now on GitHub!")
        print(f"🔗 Repository URL: {repo_url.replace('.git', '')}")
        print("\n📋 Next Steps:")
        print("1. 🌐 Deploy to Streamlit Cloud:")
        print("   - Go to https://streamlit.io/cloud")
        print("   - Connect your GitHub account")
        print("   - Deploy this repository")
        print()
        print("2. 📚 Read the deployment guide:")
        print("   - Check DEPLOYMENT_GUIDE.md for detailed instructions")
        print()
        print("3. 🎯 Customize your deployment:")
        print("   - Update repository description")
        print("   - Add topics/tags")
        print("   - Configure branch protection rules")
        print()
        print("4. 📢 Share your project:")
        print("   - Add to your portfolio")
        print("   - Share on social media")
        print("   - Submit to AI/ML communities")
        print()
        print("🚀 Your Bhavesh AI Voice Cloner is ready for the world!")
    else:
        print("\n❌ GitHub setup incomplete. Please check errors and try again.")

if __name__ == "__main__":
    main()
