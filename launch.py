#!/usr/bin/env python3
"""
🎤 Bhavesh AI Voice Cloner - Quick Launch Script

This script provides multiple ways to run the Bhavesh AI Voice Cloner:
1. Streamlit Web App (Recommended for beginners)
2. Command Line Interface
3. Python API Demo
4. Docker Container
5. Development Setup

Usage:
    python launch.py --help
    python launch.py streamlit
    python launch.py cli "Hello world!"
    python launch.py demo
    python launch.py docker
    python launch.py setup
"""

import argparse
import subprocess
import sys
import os
import platform
from pathlib import Path
import importlib.util

def check_system_requirements():
    """Check system requirements and dependencies"""
    print("🔍 Checking system requirements...")
    
    # Check Python version
    python_version = sys.version_info
    if python_version < (3, 9):
        print("❌ Python 3.9+ is required. Current version:", platform.python_version())
        return False
    print(f"✅ Python {platform.python_version()}")
    
    # Check if we're in the right directory
    if not Path("streamlit_app.py").exists():
        print("❌ Please run this script from the project root directory")
        return False
    print("✅ Project directory structure")
    
    # Check if virtual environment is recommended
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Not running in a virtual environment. Consider using:")
        print("   python -m venv venv")
        print("   source venv/bin/activate  # or venv\\Scripts\\activate on Windows")
    else:
        print("✅ Virtual environment detected")
    
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def check_gpu():
    """Check GPU availability"""
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0) if gpu_count > 0 else "Unknown"
            print(f"🚀 GPU Available: {gpu_name} ({gpu_count} device(s))")
            return "cuda"
        elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
            print("🍎 Apple Metal Performance Shaders (MPS) available")
            return "mps"
        else:
            print("💻 Using CPU (GPU acceleration not available)")
            return "cpu"
    except ImportError:
        print("⚠️  PyTorch not installed - will be installed with dependencies")
        return "cpu"

def launch_streamlit():
    """Launch the Streamlit web application"""
    print("🌐 Launching Streamlit web application...")
    print("📖 The app will open in your default browser")
    print("🔗 If it doesn't open automatically, go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch Streamlit: {e}")
        print("💡 Try installing Streamlit: pip install streamlit")
    except KeyboardInterrupt:
        print("\n👋 Streamlit app stopped")

def launch_cli(text):
    """Launch command line interface"""
    print("🎙️ Launching CLI voice generation...")
    print(f"📝 Text: {text}")
    
    try:
        # Import and use the TTS model
        from src.bhavesh_ai_voice_cloner.tts import BhaveshTTS
        import torchaudio as ta
        import torch
        
        device = check_gpu()
        print(f"🔧 Using device: {device}")
        
        print("🤖 Loading Bhavesh AI model...")
        model = BhaveshTTS.from_pretrained(device=device)
        
        print("🎵 Generating speech...")
        wav = model.generate(text)
        
        output_file = "cli_output.wav"
        ta.save(output_file, wav, model.sr)
        print(f"💾 Saved to: {output_file}")
        
        # Try to play the audio if possible
        try:
            if platform.system() == "Windows":
                import winsound
                winsound.PlaySound(output_file, winsound.SND_FILENAME)
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(["afplay", output_file])
            elif platform.system() == "Linux":
                subprocess.run(["aplay", output_file])
            print("🔊 Audio played successfully!")
        except Exception:
            print("🔇 Could not play audio automatically. Please play the file manually.")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all dependencies are installed: python launch.py setup")
    except Exception as e:
        print(f"❌ Error: {e}")

def launch_demo():
    """Launch the demo script"""
    print("🎬 Launching interactive demo...")
    try:
        subprocess.run([sys.executable, "demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to launch demo: {e}")
    except FileNotFoundError:
        print("❌ Demo script not found. Make sure demo.py exists.")

def launch_docker():
    """Launch using Docker"""
    print("🐳 Launching with Docker...")
    
    # Check if Docker is available
    try:
        subprocess.run(["docker", "--version"], check=True, capture_output=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Docker not found. Please install Docker first.")
        print("🔗 Visit: https://docs.docker.com/get-docker/")
        return
    
    print("🔨 Building Docker image...")
    try:
        subprocess.run(["docker", "build", "-t", "bhavesh-ai-voice-cloner", "."], check=True)
        print("🚀 Running Docker container...")
        subprocess.run([
            "docker", "run", "-p", "8501:8501", 
            "--name", "bhavesh-ai-vc",
            "bhavesh-ai-voice-cloner"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker error: {e}")
    except KeyboardInterrupt:
        print("\n🛑 Stopping Docker container...")
        subprocess.run(["docker", "stop", "bhavesh-ai-vc"], capture_output=True)
        subprocess.run(["docker", "rm", "bhavesh-ai-vc"], capture_output=True)

def setup_development():
    """Setup development environment"""
    print("🛠️ Setting up development environment...")
    
    if not check_system_requirements():
        return
    
    # Install dependencies
    if not install_dependencies():
        return
    
    # Install development dependencies
    print("📚 Installing development dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements-dev.txt"], check=True)
        print("✅ Development dependencies installed")
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Failed to install dev dependencies: {e}")
    
    # Setup pre-commit hooks
    print("🔧 Setting up pre-commit hooks...")
    try:
        subprocess.run([sys.executable, "-m", "pre_commit", "install"], check=True)
        print("✅ Pre-commit hooks installed")
    except subprocess.CalledProcessError:
        print("⚠️  Pre-commit not available - skipping hook setup")
    
    print("🎉 Development environment setup complete!")
    print("\n📋 Next steps:")
    print("1. Activate your virtual environment")
    print("2. Run tests: pytest")
    print("3. Start development: python launch.py streamlit")
    print("4. Read CONTRIBUTING.md for guidelines")

def main():
    parser = argparse.ArgumentParser(
        description="🎤 Bhavesh AI Voice Cloner - Launch Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py streamlit                    # Launch web interface
  python launch.py cli "Hello world!"          # Generate speech from command line
  python launch.py demo                        # Run interactive demo
  python launch.py docker                      # Use Docker container
  python launch.py setup                       # Setup development environment

Visit: https://github.com/bhavesh-ai/voice-cloner
        """
    )
    
    parser.add_argument(
        "command",
        choices=["streamlit", "cli", "demo", "docker", "setup"],
        help="Command to execute"
    )
    
    parser.add_argument(
        "text",
        nargs="?",
        default="Hello! This is Bhavesh AI speaking. Welcome to the voice cloning demo!",
        help="Text to convert to speech (for CLI mode)"
    )
    
    parser.add_argument(
        "--skip-checks",
        action="store_true",
        help="Skip system requirement checks"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="Bhavesh AI Voice Cloner v1.0.0"
    )
    
    args = parser.parse_args()
    
    # Print header
    print("=" * 60)
    print("🎤 BHAVESH AI VOICE CLONER")
    print("🚀 Advanced AI Voice Cloning & Text-to-Speech")
    print("=" * 60)
    print()
    
    # Check system requirements (unless skipped)
    if not args.skip_checks and args.command != "setup":
        if not check_system_requirements():
            print("\n💡 Run 'python launch.py setup' to configure your environment")
            sys.exit(1)
        check_gpu()
        print()
    
    # Execute command
    if args.command == "streamlit":
        launch_streamlit()
    elif args.command == "cli":
        launch_cli(args.text)
    elif args.command == "demo":
        launch_demo()
    elif args.command == "docker":
        launch_docker()
    elif args.command == "setup":
        setup_development()

if __name__ == "__main__":
    main()
