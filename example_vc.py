import torch
import torchaudio as ta

from src.bhavesh_ai_voice_cloner.vc import BhaveshVC

# Automatically detect the best available device
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device: {device}")

AUDIO_PATH = "YOUR_SOURCE_AUDIO.wav"
TARGET_VOICE_PATH = "YOUR_TARGET_VOICE.wav"

model = BhaveshVC.from_pretrained(device)
wav = model.generate(
    audio=AUDIO_PATH,
    target_voice_path=TARGET_VOICE_PATH,
)
ta.save("bhavesh_ai_voice_conversion.wav", wav, model.sr)
print("Voice conversion saved as 'bhavesh_ai_voice_conversion.wav'")
