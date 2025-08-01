#!/usr/bin/env python3
"""
Quick test to validate module imports for Streamlit deployment
"""

def test_imports():
    try:
        print("Testing core package import...")
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        
        print("Testing bhavesh_ai_voice_cloner import...")
        import bhavesh_ai_voice_cloner
        print(f"✅ Core package version: {bhavesh_ai_voice_cloner.__version__}")
        
        print("Testing TTS import...")
        from bhavesh_ai_voice_cloner.tts import BhaveshTTS
        print("✅ BhaveshTTS imported successfully")
        
        print("Testing VC import...")
        from bhavesh_ai_voice_cloner.vc import BhaveshVC
        print("✅ BhaveshVC imported successfully")
        
        print("Testing T3 model import...")
        from bhavesh_ai_voice_cloner.models.t3 import T3
        print("✅ T3 model imported successfully")
        
        print("✅ All imports successful! Ready for Streamlit deployment.")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()
