#!/usr/bin/env python3
"""
Streamlit deployment validation test - imports only (no dependencies)
"""

def test_module_structure():
    """Test that all module directories have proper __init__.py files"""
    import os
    import sys
    
    # Add src to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    print("🔍 Testing module structure for Streamlit deployment...")
    
    # Test basic package structure
    required_files = [
        'src/bhavesh_ai_voice_cloner/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/t3/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/t3/modules/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/t3/inference/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/s3gen/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/s3gen/matcha/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/s3gen/utils/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/s3gen/transformer/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/s3tokenizer/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/tokenizers/__init__.py',
        'src/bhavesh_ai_voice_cloner/models/voice_encoder/__init__.py',
    ]
    
    missing_files = []
    for file_path in required_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
        else:
            print(f"✅ {file_path}")
    
    if missing_files:
        print(f"\n❌ Missing files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    print(f"\n🎉 All {len(required_files)} required __init__.py files are present!")
    print("✅ Module structure is ready for Streamlit Cloud deployment!")
    return True

if __name__ == "__main__":
    success = test_module_structure()
    exit(0 if success else 1)
