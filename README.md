
# 🎤 Bhavesh AI Voice Cloner

[![Streamlit App](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://bhavesh-ai-voice-cl## 📞 Support & Community

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/bhau23/voice-cloner/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/bhau23/voice-cloner/discussions)
- 📧 **Contact**: bhavesh.ai.contact@gmail.comstreamlit.app)
[![GitHub](https://img.shields.io/github/stars/bhau23/voice-cloner?style=for-the-badge&logo=github)](https://github.com/bhau23/voice-cloner)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

<div align="center">
  <h2>🚀 Advanced AI Voice Cloning & Text-to-Speech</h2>
  <p><em>Transform any text into natural speech using your own voice or any reference audio</em></p>
</div>

---

**Bhavesh AI Voice Cloner** is a cutting-edge, open-source Text-to-Speech (TTS) and voice cloning system powered by state-of-the-art AI technology. With just a few seconds of reference audio, you can clone any voice and generate natural-sounding speech with emotion control and perfect pronunciation.

## ✨ Key Features

- 🎯 **Zero-shot Voice Cloning**: Clone any voice with just seconds of reference audio
- 🎭 **Emotion Control**: Adjust emotional intensity and expression levels
- ⚡ **Lightning Fast**: Optimized for real-time generation
- 🧠 **0.5B Llama Backbone**: Built on state-of-the-art transformer architecture
- 🎵 **High Quality Audio**: Crystal clear, natural-sounding speech output
- 🔒 **Ethical AI**: Built-in watermarking for responsible AI usage
- 🌐 **Multiple Languages**: Supports multiple languages and accents
- 🚀 **Easy to Use**: Simple API and beautiful Streamlit interface

## 🎯 Use Cases

- 🎬 **Content Creation**: Videos, podcasts, audiobooks
- 🎮 **Gaming**: Character voices and narration
- 📱 **Applications**: Voice assistants and chatbots
- 🎭 **Entertainment**: Memes, voice effects, creative projects
- 📚 **Education**: Language learning and accessibility tools

# 🚀 Quick Start

## 📦 Installation

### Method 1: Automated Setup (Recommended)
```bash
# Clone the repository
git clone https://github.com/bhau23/voice-cloner.git
cd voice-cloner

# Run the setup script
python launch.py setup

# Launch the Streamlit app
python launch.py streamlit
```

### Method 2: Manual Installation
```bash
# Clone the repository
git clone https://github.com/bhau23/voice-cloner.git
cd voice-cloner

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run streamlit_app.py
```

### Method 3: Docker (One-Click)
```bash
git clone https://github.com/bhau23/voice-cloner.git
cd voice-cloner
python launch.py docker
```

### Method 4: Install as Package
```bash
pip install bhavesh-ai-voice-cloner
```
## 💻 Usage

### Python API
```python
import torchaudio as ta
from bhavesh_ai_voice_cloner.tts import BhaveshTTS

# Initialize the model
model = BhaveshTTS.from_pretrained(device="cuda")

# Generate speech with default voice
text = "Hello! This is Bhavesh AI speaking. I can clone any voice and make it sound natural!"
wav = model.generate(text)
ta.save("output.wav", wav, model.sr)

# Clone a specific voice
REFERENCE_AUDIO = "path/to/your/reference.wav"
wav = model.generate(text, audio_prompt_path=REFERENCE_AUDIO)
ta.save("cloned_voice.wav", wav, model.sr)
```

### Streamlit Web Interface
For a user-friendly interface, run the Streamlit app:
```bash
# Quick launch
python launch.py streamlit

# Or traditional method
streamlit run streamlit_app.py
```

### Command Line Interface
Generate speech directly from command line:
```bash
python launch.py cli "Your text here"
```

### Interactive Demo
Run the comprehensive demo:
```bash
python launch.py demo
```

## 🛠️ Project Management

### Setup Development Environment
```bash
python launch.py setup
```

### Verify Project Status
```bash
python verify_project.py
```

### Deploy to GitHub
```bash
python github_setup.py
```

## 🎛️ Advanced Parameters

- `exaggeration` (0.25-2.0): Control emotional intensity (default: 0.5)
- `cfg_weight` (0.0-1.0): Control speech pacing and clarity (default: 0.5)
- `temperature` (0.05-5.0): Control randomness in generation (default: 0.8)
- `repetition_penalty` (1.0-2.0): Prevent repetitive speech patterns (default: 1.2)

## 🌍 Supported Languages
Currently supporting **English** with plans to expand to more languages.

## 🤝 Contributing
We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

## 🙏 Acknowledgements
This project builds upon excellent open-source work:
- [Cosyvoice](https://github.com/FunAudioLLM/CosyVoice)
- [Real-Time-Voice-Cloning](https://github.com/CorentinJ/Real-Time-Voice-Cloning)
- [HiFT-GAN](https://github.com/yl4579/HiFTNet)
- [Llama 3](https://github.com/meta-llama/llama3)
- [S3Tokenizer](https://github.com/xingchensong/S3Tokenizer)

## 🔐 Responsible AI & Watermarking

Every audio file generated by Bhavesh AI includes built-in watermarking technology for responsible AI usage. This helps identify AI-generated content and prevents misuse.

### Watermark Detection
```python
import perth
import librosa

# Load the generated audio
audio, sr = librosa.load("generated_audio.wav", sr=None)

# Initialize watermarker
watermarker = perth.PerthImplicitWatermarker()

# Check for watermark
watermark = watermarker.get_watermark(audio, sample_rate=sr)
print(f"AI Generated: {watermark > 0.5}")
```

## 📞 Support & Community

- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/bhavesh-ai/voice-cloner/issues)
- � **Discussions**: [GitHub Discussions](https://github.com/bhavesh-ai/voice-cloner/discussions)
- 📧 **Contact**: bhavesh.ai.contact@gmail.com

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏆 Citation
If you use this project in your research, please cite:
```bibtex
@misc{bhaveshaivoicecloner2025,
  author       = {{Bhavesh AI}},
  title        = {{Bhavesh AI Voice Cloner}},
  year         = {2025},
  howpublished = {\url{https://github.com/bhau23/voice-cloner}},
  note         = {GitHub repository}
}
```

## ⚠️ Disclaimer
This tool is intended for legitimate and ethical uses only. Users are responsible for ensuring they have proper consent before cloning someone's voice. Please use this technology responsibly and in compliance with applicable laws.

---

<div align="center">
  <p>Made with ❤️ by <strong>Bhavesh AI</strong></p>
  <p>
    <a href="https://github.com/bhau23/voice-cloner">GitHub</a> •
    <a href="https://bhavesh-ai-voice-cloner.streamlit.app">Try Online</a> •
    <a href="mailto:bhavesh.ai.contact@gmail.com">Contact</a>
  </p>
</div>
