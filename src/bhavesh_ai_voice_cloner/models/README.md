# Model Architecture Note

⚠️ **Important**: The actual model implementation files were removed during the rebranding process to create a clean project structure.

## Using the Models

The `BhaveshTTS` and `BhaveshVC` classes in `tts.py` and `vc.py` automatically download the required model files from Hugging Face Hub when you call `from_pretrained()`.

### Model Loading
```python
from bhavesh_ai_voice_cloner.tts import BhaveshTTS

# This automatically downloads models from HuggingFace
model = BhaveshTTS.from_pretrained(device="cuda")
```

### Repository Structure
- The models are downloaded from: `ResembleAI/chatterbox`
- Models are cached locally after first download
- No manual model file management required

### Model Files Downloaded
- `ve.safetensors` - Voice encoder
- `t3_cfg.safetensors` - T3 configuration 
- `s3gen.safetensors` - S3 generation model
- `tokenizer.json` - Text tokenizer
- `conds.pt` - Conditional embeddings

### First Run
On the first run, the system will:
1. Check for cached models
2. Download from HuggingFace if not found
3. Cache locally for faster subsequent loads
4. Initialize and return the model

This approach keeps the repository clean while ensuring all required models are available when needed.
