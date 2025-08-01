# 🎤 Bhavesh AI Voice Cloner - Streamlit Deployment Guide

This guide will help you deploy the Bhavesh AI Voice Cloner on Streamlit Cloud.

## 🚀 Quick Deployment

### Method 1: One-Click Deploy
[![Deploy to Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy)

### Method 2: Manual Deployment

1. **Fork this repository** to your GitHub account
2. **Connect to Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Sign in with GitHub
   - Click "New app"
   - Select your forked repository
   - Set the main file path to `streamlit_app.py`
   - Click "Deploy!"

## 📋 Configuration

### Environment Variables
No environment variables required for basic deployment.

### Advanced Configuration
Create a `.streamlit/config.toml` file for advanced settings:

```toml
[theme]
primaryColor = "#6366f1"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f8fafc"
textColor = "#1e293b"

[server]
maxUploadSize = 200
enableCORS = false
enableXsrfProtection = true

[browser]
gatherUsageStats = false
```

## 🛠️ Local Development

### Prerequisites
- Python 3.9 or higher
- CUDA-compatible GPU (recommended for faster processing)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/bhavesh-ai/voice-cloner.git
   cd voice-cloner
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser** to `http://localhost:8501`

## 🎯 Features

### 🎙️ Text-to-Speech
- **Zero-shot voice cloning** with reference audio
- **Emotion control** and intensity adjustment
- **Real-time generation** with optimized performance
- **High-quality audio** output (24kHz sample rate)
- **Batch processing** for multiple texts

### 🔄 Voice Conversion
- Convert existing audio to different voices
- Preserve speech content while changing voice characteristics
- Support for multiple audio formats

### 🎨 Modern UI
- **Responsive design** that works on all devices
- **Interactive visualizations** with Plotly
- **Real-time audio waveforms** and spectrograms
- **Progress tracking** with animated indicators
- **Dark/Light theme** support

### 📊 Analytics
- Usage statistics and performance metrics
- Generation trends and parameter analysis
- System monitoring and optimization insights

## 🔧 Customization

### Adding New Voices
1. Upload reference audio files (WAV, MP3, FLAC)
2. Configure voice parameters in the settings
3. Save custom voice presets for reuse

### Modifying the UI
- Edit `streamlit_app.py` for layout changes
- Modify CSS in the `st.markdown()` sections for styling
- Add new pages by creating functions and updating the navigation

### Performance Optimization
- **GPU acceleration**: Ensure CUDA is available for faster processing
- **Memory management**: Adjust batch sizes based on available RAM
- **Caching**: Use Streamlit's caching for model loading

## 📱 Mobile Support

The interface is fully responsive and works on:
- 📱 Mobile phones (iOS/Android)
- 📱 Tablets (iPad, Android tablets)
- 💻 Desktop browsers
- 🖥️ Large displays

## 🐛 Troubleshooting

### Common Issues

**1. Model Loading Errors**
```bash
# Solution: Ensure you have sufficient GPU memory
# Try switching to CPU mode if GPU memory is limited
```

**2. Audio Upload Issues**
```bash
# Solution: Check file format and size
# Supported: WAV, MP3, FLAC, M4A
# Max size: 200MB
```

**3. Slow Performance**
```bash
# Solution: Enable GPU acceleration
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### Memory Requirements
- **Minimum**: 8GB RAM, CPU
- **Recommended**: 16GB RAM, 8GB+ GPU
- **Optimal**: 32GB RAM, 16GB+ GPU

## 🔒 Security & Privacy

### Data Handling
- **No data storage**: Audio files are processed in memory only
- **No tracking**: User interactions are not logged
- **Local processing**: All AI inference happens on the server
- **Secure uploads**: Files are automatically deleted after processing

### Watermarking
All generated audio includes imperceptible watermarks for:
- **Content identification**: Detect AI-generated audio
- **Responsible AI**: Prevent misuse and deepfakes
- **Compliance**: Meet platform requirements for synthetic media

## 📞 Support

### Getting Help
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/bhavesh-ai/voice-cloner/issues)
- 💬 **Discussions**: [GitHub Discussions](https://github.com/bhavesh-ai/voice-cloner/discussions)
- 📧 **Contact**: bhavesh.ai.contact@gmail.com

### Community
- ⭐ **Star the repo** if you find it useful
- 🍴 **Fork and contribute** to make it better
- 📢 **Share with others** who might benefit

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## 🙏 Credits

Built with ❤️ by **Bhavesh AI**

Based on state-of-the-art research in:
- Text-to-Speech synthesis
- Voice cloning technology  
- Neural audio processing
- Transformer architectures

---

<div align="center">
  <p><strong>Transform your ideas into voice with Bhavesh AI</strong></p>
  <p>
    <a href="https://bhavesh-ai-voice-cloner.streamlit.app">🚀 Try Live Demo</a> •
    <a href="https://github.com/bhavesh-ai/voice-cloner">📱 GitHub Repo</a> •
    <a href="mailto:bhavesh.ai.contact@gmail.com">✉️ Contact</a>
  </p>
</div>
