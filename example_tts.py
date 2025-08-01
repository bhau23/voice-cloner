import torchaudio as ta
import torch
from src.bhavesh_ai_voice_cloner.tts import BhaveshTTS

# Automatically detect the best available device
if torch.cuda.is_available():
    device = "cuda"
elif torch.backends.mps.is_available():
    device = "mps"
else:
    device = "cpu"

print(f"Using device: {device}")

model = BhaveshTTS.from_pretrained(device=device)

text = "Hello! This is Bhavesh AI speaking. I can transform any text into natural-sounding speech with incredible quality and emotion control."
wav = model.generate(text)
ta.save("bhavesh_ai_demo.wav", wav, model.sr)

print("Generated speech saved as 'bhavesh_ai_demo.wav'")

# If you want to synthesize with a different voice, specify the audio prompt
# AUDIO_PROMPT_PATH = "YOUR_REFERENCE_VOICE.wav"
# wav_cloned = model.generate(text, audio_prompt_path=AUDIO_PROMPT_PATH)
# ta.save("bhavesh_ai_cloned_voice.wav", wav_cloned, model.sr)
# print("Cloned voice saved as 'bhavesh_ai_cloned_voice.wav'")
