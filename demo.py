#!/usr/bin/env python3
"""
Bhavesh AI Voice Cloner - Demo Script
=====================================

This script demonstrates the core functionality of the Bhavesh AI Voice Cloner.
Run this to test the voice cloning and text-to-speech capabilities.

Usage:
    python demo.py

Requirements:
    - CUDA-capable GPU recommended
    - Python 3.9+
    - All dependencies installed (pip install -r requirements.txt)
"""

import os
import sys
import argparse
import torchaudio as ta
from pathlib import Path

# Add src to path for local development
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    from bhavesh_ai_voice_cloner.tts import BhaveshTTS
    from bhavesh_ai_voice_cloner.vc import BhaveshVC
except ImportError as e:
    print("❌ Error importing Bhavesh AI modules:")
    print(f"   {e}")
    print("\n💡 Please ensure you have installed the package:")
    print("   pip install -r requirements.txt")
    print("   pip install -e .")
    sys.exit(1)

import torch


def check_system():
    """Check system requirements and GPU availability."""
    print("🔍 System Check")
    print("=" * 50)
    
    # Python version
    print(f"🐍 Python Version: {sys.version}")
    
    # PyTorch and CUDA
    print(f"🔥 PyTorch Version: {torch.__version__}")
    print(f"🚀 CUDA Available: {torch.cuda.is_available()}")
    
    if torch.cuda.is_available():
        print(f"🎮 GPU Count: {torch.cuda.device_count()}")
        print(f"🎯 Current GPU: {torch.cuda.get_device_name()}")
        print(f"💾 GPU Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
    else:
        print("⚠️  Warning: CUDA not available. TTS will run on CPU (slower)")
    
    print()


def demo_tts(device="auto", save_dir="demo_outputs"):
    """Demonstrate Text-to-Speech functionality."""
    print("🎤 Text-to-Speech Demo")
    print("=" * 50)
    
    # Auto-detect device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    print(f"🔧 Using device: {device}")
    
    # Create output directory
    os.makedirs(save_dir, exist_ok=True)
    
    try:
        # Load model
        print("📥 Loading Bhavesh TTS model...")
        model = BhaveshTTS.from_pretrained(device=device)
        print("✅ Model loaded successfully!")
        
        # Demo texts
        demo_texts = [
            "Hello! Welcome to Bhavesh AI Voice Cloner. This is a demonstration of our advanced text-to-speech technology.",
            "I can generate natural-sounding speech with emotion control and perfect pronunciation.",
            "Try uploading your own voice sample to clone it instantly!"
        ]
        
        # Generate speech samples
        for i, text in enumerate(demo_texts, 1):
            print(f"\n🎵 Generating sample {i}: '{text[:50]}...'")
            
            # Generate audio
            wav = model.generate(
                text,
                exaggeration=0.5,
                temperature=0.8,
                cfg_weight=0.5
            )
            
            # Save audio
            output_path = f"{save_dir}/demo_tts_{i}.wav"
            ta.save(output_path, wav, model.sr)
            print(f"💾 Saved: {output_path}")
        
        print(f"\n🎉 TTS Demo completed! Check the '{save_dir}' folder for generated audio files.")
        
    except Exception as e:
        print(f"❌ Error in TTS demo: {e}")
        return False
    
    return True


def demo_voice_cloning(reference_audio=None, device="auto", save_dir="demo_outputs"):
    """Demonstrate Voice Cloning functionality."""
    print("\n🎭 Voice Cloning Demo")
    print("=" * 50)
    
    if reference_audio and not os.path.exists(reference_audio):
        print(f"❌ Reference audio file not found: {reference_audio}")
        print("💡 Skipping voice cloning demo. To test voice cloning:")
        print("   python demo.py --reference_audio path/to/your/audio.wav")
        return False
    
    if not reference_audio:
        print("💡 No reference audio provided. Skipping voice cloning demo.")
        print("   To test voice cloning: python demo.py --reference_audio path/to/your/audio.wav")
        return False
    
    # Auto-detect device
    if device == "auto":
        device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        # Load model
        print("📥 Loading Bhavesh TTS model for voice cloning...")
        model = BhaveshTTS.from_pretrained(device=device)
        
        # Demo text for cloning
        clone_text = "This is a demonstration of voice cloning using Bhavesh AI. The voice you're hearing has been cloned from the reference audio."
        
        print(f"🎵 Cloning voice from: {reference_audio}")
        print(f"📝 Text: '{clone_text}'")
        
        # Generate cloned voice
        wav = model.generate(
            clone_text,
            audio_prompt_path=reference_audio,
            exaggeration=0.5,
            temperature=0.8,
            cfg_weight=0.5
        )
        
        # Save cloned audio
        output_path = f"{save_dir}/demo_voice_clone.wav"
        ta.save(output_path, wav, model.sr)
        print(f"💾 Saved cloned voice: {output_path}")
        
        print("🎉 Voice cloning demo completed!")
        
    except Exception as e:
        print(f"❌ Error in voice cloning demo: {e}")
        return False
    
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Bhavesh AI Voice Cloner - Demo Script",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python demo.py                                    # Basic TTS demo
    python demo.py --reference_audio my_voice.wav     # Voice cloning demo
    python demo.py --device cpu                       # Force CPU usage
    python demo.py --output_dir my_outputs            # Custom output directory
        """
    )
    
    parser.add_argument(
        "--reference_audio",
        type=str,
        help="Path to reference audio file for voice cloning demo"
    )
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cuda", "cpu"],
        help="Device to use for inference (default: auto-detect)"
    )
    parser.add_argument(
        "--output_dir",
        type=str,
        default="demo_outputs",
        help="Directory to save demo outputs (default: demo_outputs)"
    )
    parser.add_argument(
        "--skip_tts",
        action="store_true",
        help="Skip the TTS demo"
    )
    parser.add_argument(
        "--skip_cloning",
        action="store_true",
        help="Skip the voice cloning demo"
    )
    
    args = parser.parse_args()
    
    print("🎤 Bhavesh AI Voice Cloner - Demo")
    print("=" * 60)
    print("Welcome to the Bhavesh AI Voice Cloner demonstration!")
    print("This demo will showcase our advanced TTS and voice cloning capabilities.")
    print()
    
    # System check
    check_system()
    
    success = True
    
    # Run TTS demo
    if not args.skip_tts:
        if not demo_tts(device=args.device, save_dir=args.output_dir):
            success = False
    
    # Run voice cloning demo
    if not args.skip_cloning:
        if not demo_voice_cloning(
            reference_audio=args.reference_audio,
            device=args.device,
            save_dir=args.output_dir
        ):
            success = False
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Demo completed successfully!")
        print(f"📁 Check the '{args.output_dir}' folder for generated audio files.")
    else:
        print("⚠️  Demo completed with some errors.")
    
    print("\n🚀 Ready to try the Streamlit app?")
    print("   streamlit run streamlit_app.py")
    print("\n💡 Need help? Check out our documentation:")
    print("   https://github.com/bhavesh-ai/voice-cloner")


if __name__ == "__main__":
    main()
