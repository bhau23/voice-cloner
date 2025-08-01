#!/usr/bin/env python3
"""
Bhavesh AI Voice Cloner - Setup and Installation Script
======================================================

This script helps set up the Bhavesh AI Voice Cloner environment.

Usage:
    python setup.py                 # Interactive setup
    python setup.py --auto          # Automatic setup with defaults
    python setup.py --dev           # Development setup
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description="", check=True):
    """Run a command and handle errors."""
    print(f"🔧 {description}")
    print(f"   Command: {cmd}")
    
    try:
        result = subprocess.run(
            cmd.split() if isinstance(cmd, str) else cmd,
            check=check,
            capture_output=True,
            text=True
        )
        
        if result.stdout:
            print(f"   Output: {result.stdout.strip()}")
        
        return result.returncode == 0
    
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Error: {e}")
        if e.stderr:
            print(f"   Error details: {e.stderr.strip()}")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False


def check_python_version():
    """Check if Python version is compatible."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 9):
        print("   ❌ Python 3.9+ is required!")
        return False
    else:
        print("   ✅ Python version is compatible")
        return True


def check_git():
    """Check if git is available."""
    print("📁 Checking Git availability...")
    
    if run_command("git --version", "Checking git version", check=False):
        print("   ✅ Git is available")
        return True
    else:
        print("   ❌ Git not found. Please install Git first.")
        return False


def setup_virtual_environment(env_name="bhavesh_ai_env"):
    """Set up a virtual environment."""
    print(f"🌐 Setting up virtual environment: {env_name}")
    
    # Check if venv exists
    if os.path.exists(env_name):
        print(f"   ⚠️  Environment '{env_name}' already exists")
        response = input("   Do you want to recreate it? (y/N): ").lower()
        if response != 'y':
            print("   Skipping virtual environment setup")
            return True
        else:
            # Remove existing environment
            import shutil
            shutil.rmtree(env_name)
    
    # Create virtual environment
    if not run_command(f"{sys.executable} -m venv {env_name}", "Creating virtual environment"):
        return False
    
    print("   ✅ Virtual environment created successfully")
    print(f"\n   📝 To activate the environment:")
    if os.name == 'nt':  # Windows
        print(f"      {env_name}\\Scripts\\activate")
    else:  # Unix/Linux/macOS
        print(f"      source {env_name}/bin/activate")
    
    return True


def install_dependencies(dev_mode=False):
    """Install project dependencies."""
    print("📦 Installing dependencies...")
    
    requirements_file = "requirements-dev.txt" if dev_mode else "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print(f"   ❌ Requirements file not found: {requirements_file}")
        return False
    
    # Upgrade pip first
    if not run_command(f"{sys.executable} -m pip install --upgrade pip", "Upgrading pip"):
        print("   ⚠️  Failed to upgrade pip, continuing anyway...")
    
    # Install requirements
    if not run_command(
        f"{sys.executable} -m pip install -r {requirements_file}",
        f"Installing from {requirements_file}"
    ):
        return False
    
    print("   ✅ Dependencies installed successfully")
    return True


def install_package(dev_mode=False):
    """Install the package itself."""
    print("📦 Installing Bhavesh AI Voice Cloner package...")
    
    if dev_mode:
        cmd = f"{sys.executable} -m pip install -e ."
        description = "Installing package in development mode"
    else:
        cmd = f"{sys.executable} -m pip install ."
        description = "Installing package"
    
    if not run_command(cmd, description):
        return False
    
    print("   ✅ Package installed successfully")
    return True


def verify_installation():
    """Verify that the installation works."""
    print("🔍 Verifying installation...")
    
    try:
        # Test import
        sys.path.insert(0, str(Path.cwd() / "src"))
        from bhavesh_ai_voice_cloner.tts import BhaveshTTS
        from bhavesh_ai_voice_cloner.vc import BhaveshVC
        
        print("   ✅ Package imports successfully")
        
        # Test torch
        import torch
        print(f"   ✅ PyTorch version: {torch.__version__}")
        print(f"   ✅ CUDA available: {torch.cuda.is_available()}")
        
        return True
        
    except ImportError as e:
        print(f"   ❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"   ❌ Verification error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Bhavesh AI Voice Cloner Setup Script",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Automatic setup with defaults (no prompts)"
    )
    parser.add_argument(
        "--dev",
        action="store_true",
        help="Development setup (installs dev dependencies)"
    )
    parser.add_argument(
        "--skip-venv",
        action="store_true",
        help="Skip virtual environment setup"
    )
    parser.add_argument(
        "--env-name",
        type=str,
        default="bhavesh_ai_env",
        help="Virtual environment name (default: bhavesh_ai_env)"
    )
    
    args = parser.parse_args()
    
    print("🚀 Bhavesh AI Voice Cloner - Setup Script")
    print("=" * 60)
    
    success = True
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Git
    if not check_git():
        print("   💡 Git is recommended but not required for basic usage")
    
    # Setup virtual environment
    if not args.skip_venv:
        if args.auto or input("\n🌐 Set up virtual environment? (Y/n): ").lower() != 'n':
            if not setup_virtual_environment(args.env_name):
                success = False
        else:
            print("   Skipping virtual environment setup")
    
    # Install dependencies
    if success:
        if not install_dependencies(dev_mode=args.dev):
            success = False
    
    # Install package
    if success:
        if not install_package(dev_mode=args.dev):
            success = False
    
    # Verify installation
    if success:
        if not verify_installation():
            success = False
    
    print("\n" + "=" * 60)
    
    if success:
        print("🎉 Setup completed successfully!")
        print("\n📋 Next steps:")
        print("   1. Activate virtual environment (if created)")
        print("   2. Run demo: python demo.py")
        print("   3. Start Streamlit app: streamlit run streamlit_app.py")
        print("   4. Check documentation: README.md")
        
        if args.dev:
            print("\n🔧 Development mode enabled:")
            print("   - Dev dependencies installed")
            print("   - Package installed in editable mode")
            print("   - Run tests: pytest (when implemented)")
    else:
        print("❌ Setup failed! Please check the errors above.")
        print("\n💡 Common solutions:")
        print("   - Ensure Python 3.9+ is installed")
        print("   - Check internet connection for package downloads")
        print("   - Try running with administrator/sudo privileges")
        print("   - Create a fresh virtual environment")
        
        sys.exit(1)


if __name__ == "__main__":
    main()
