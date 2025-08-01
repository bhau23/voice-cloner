# 🤝 Contributing to Bhavesh AI Voice Cloner

We love your input! We want to make contributing to Bhavesh AI Voice Cloner as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## 🚀 Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### 📋 Pull Request Process

1. **Fork the repo** and create your branch from `main`
2. **Add tests** if you've added code that should be tested
3. **Update documentation** if you've changed APIs
4. **Ensure the test suite passes**
5. **Make sure your code lints**
6. **Issue that pull request!**

### 🐛 Bug Reports

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/bhau23/voice-cloner/issues/new).

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### 💡 Feature Requests

We welcome feature requests! Please:

1. **Check existing issues** to avoid duplicates
2. **Describe the feature** in detail
3. **Explain why it would be useful**
4. **Consider implementation challenges**

## 🛠️ Development Setup

### Prerequisites

- Python 3.9+
- Git
- CUDA-compatible GPU (recommended)

### Local Setup

```bash
# Clone your fork
git clone https://github.com/your-username/voice-cloner.git
cd voice-cloner

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_tts.py
```

### Code Style

We use several tools to maintain code quality:

```bash
# Format code
black src/ tests/
isort src/ tests/

# Lint code
flake8 src/ tests/
mypy src/

# Run all checks
pre-commit run --all-files
```

## 📁 Project Structure

```
bhavesh-ai-voice-cloner/
├── src/
│   └── bhavesh_ai_voice_cloner/
│       ├── __init__.py
│       ├── tts.py          # Main TTS implementation
│       ├── vc.py           # Voice conversion
│       └── models/         # Model architectures
├── tests/                  # Test files
├── streamlit_app.py        # Streamlit web interface
├── requirements.txt        # Python dependencies
└── README.md              # Project documentation
```

## 🎨 UI/UX Guidelines

### Design Principles

- **Modern & Clean**: Use contemporary design patterns
- **Accessible**: Follow WCAG guidelines
- **Responsive**: Work on all device sizes
- **Fast**: Optimize for performance
- **Intuitive**: Clear user flows

### Color Palette

```css
Primary: #6366f1 (Indigo)
Secondary: #8b5cf6 (Purple)
Accent: #ec4899 (Pink)
Success: #10b981 (Green)
Warning: #f59e0b (Amber)
Error: #ef4444 (Red)
```

### Component Guidelines

- Use **consistent spacing** (8px grid system)
- Follow **Material Design** principles
- Implement **smooth animations** (300ms transitions)
- Ensure **high contrast** for accessibility

## 🧪 Testing Guidelines

### Test Categories

1. **Unit Tests**: Test individual functions/classes
2. **Integration Tests**: Test component interactions
3. **End-to-End Tests**: Test complete user flows
4. **Performance Tests**: Test speed and memory usage

### Writing Tests

```python
import pytest
from src.bhavesh_ai_voice_cloner.tts import BhaveshTTS

def test_model_loading():
    """Test that the model loads correctly."""
    model = BhaveshTTS.from_pretrained("cpu")
    assert model is not None
    assert model.device == "cpu"

def test_text_generation():
    """Test basic text-to-speech generation."""
    model = BhaveshTTS.from_pretrained("cpu")
    text = "Hello, world!"
    wav = model.generate(text)
    
    assert wav is not None
    assert len(wav.shape) == 2  # Should be stereo
    assert wav.shape[1] > 0     # Should have samples
```

## 📚 Documentation

### Code Documentation

- Use **docstrings** for all public functions/classes
- Follow **Google style** docstring format
- Include **type hints** for better IDE support
- Add **examples** in docstrings when helpful

```python
def generate_speech(
    text: str,
    voice_path: Optional[str] = None,
    emotion: float = 0.5
) -> torch.Tensor:
    """Generate speech from text using AI voice cloning.
    
    Args:
        text: The input text to convert to speech.
        voice_path: Optional path to reference voice audio.
        emotion: Emotional intensity from 0.0 to 2.0.
        
    Returns:
        Generated audio as a tensor with shape (1, samples).
        
    Example:
        >>> model = BhaveshTTS.from_pretrained("cuda")
        >>> audio = model.generate_speech("Hello world!")
        >>> save_audio(audio, "output.wav")
    """
```

### README Updates

When adding features:

1. Update the **feature list**
2. Add **usage examples**
3. Update **installation instructions** if needed
4. Add **screenshots** for UI changes

## 🔄 Release Process

### Version Numbering

We use [Semantic Versioning](https://semver.org/):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes (backward compatible)

### Release Checklist

- [ ] All tests pass
- [ ] Documentation updated
- [ ] Version number bumped
- [ ] Changelog updated
- [ ] GitHub release created
- [ ] PyPI package published

## 🎖️ Recognition

Contributors are recognized in:

- **README.md** contributors section
- **CHANGELOG.md** for significant contributions
- **GitHub releases** for version contributions

## 📞 Getting Help

- **Questions**: [GitHub Discussions](https://github.com/bhau23/voice-cloner/discussions)
- **Issues**: [GitHub Issues](https://github.com/bhau23/voice-cloner/issues)
- **Email**: bhavesh.ai.contact@gmail.com

## 📄 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Bhavesh AI Voice Cloner! 🎉
