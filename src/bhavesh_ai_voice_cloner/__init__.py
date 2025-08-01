try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version  # For Python <3.8

try:
    __version__ = version("bhavesh-ai-voice-cloner")
except Exception:
    # Fallback version when package is not installed via pip
    __version__ = "1.0.0"


from .tts import BhaveshTTS
from .vc import BhaveshVC
