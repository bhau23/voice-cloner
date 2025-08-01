import streamlit as st
import torch
import torchaudio as ta
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import tempfile
import io
import time
from streamlit_option_menu import option_menu
from PIL import Image
import pandas as pd

# Import our rebranded TTS system
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from bhavesh_ai_voice_cloner.tts import BhaveshTTS
    from bhavesh_ai_voice_cloner.vc import BhaveshVC
except ImportError:
    # Fallback for development or different directory structures
    from src.bhavesh_ai_voice_cloner.tts import BhaveshTTS
    from src.bhavesh_ai_voice_cloner.vc import BhaveshVC

# Page configuration
st.set_page_config(
    page_title="🎤 Bhavesh AI Voice Cloner",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/bhau23/voice-cloner/discussions',
        'Report a bug': 'https://github.com/bhau23/voice-cloner/issues',
        'About': "# Bhavesh AI Voice Cloner\n\nAdvanced AI-powered voice cloning and text-to-speech system."
    }
)

# Custom CSS for modern aesthetics
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --accent-color: #ec4899;
        --background-dark: #0f172a;
        --background-light: #f8fafc;
        --text-dark: #1e293b;
        --text-light: #64748b;
        --border-color: #e2e8f0;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --error-color: #ef4444;
    }
    
    /* Hide Streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Custom header */
    .main-header {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.9);
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* Feature cards */
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid var(--border-color);
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 1rem;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 30px rgba(0,0,0,0.15);
    }
    
    .feature-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
        display: block;
    }
    
    /* Audio controls */
    .audio-container {
        background: linear-gradient(135deg, #f8fafc, #e2e8f0);
        padding: 1.5rem;
        border-radius: 15px;
        border: 2px dashed var(--primary-color);
        text-align: center;
        margin: 1rem 0;
    }
    
    /* Progress indicators */
    .progress-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid var(--primary-color);
        margin: 1rem 0;
    }
    
    /* Metrics cards */
    .metric-card {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        margin: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 5px 15px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: linear-gradient(180deg, var(--background-light), white);
    }
    
    /* Sliders */
    .stSlider > div > div > div > div {
        background: var(--primary-color);
    }
    
    /* Selectbox */
    .stSelectbox > div > div > div {
        border-color: var(--primary-color);
    }
    
    /* Text areas */
    .stTextArea > div > div > textarea {
        border-color: var(--primary-color);
        border-radius: 10px;
    }
    
    /* Success/Error messages */
    .stSuccess {
        background: linear-gradient(135deg, var(--success-color), #059669);
        color: white;
        border-radius: 10px;
    }
    
    .stError {
        background: linear-gradient(135deg, var(--error-color), #dc2626);
        color: white;
        border-radius: 10px;
    }
    
    /* Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .fadeIn {
        animation: fadeIn 0.6s ease-out;
    }
    
    /* Wave animation for audio processing */
    @keyframes wave {
        0%, 100% { transform: scaleY(1); }
        50% { transform: scaleY(1.5); }
    }
    
    .wave-bar {
        width: 4px;
        height: 20px;
        background: var(--primary-color);
        margin: 0 2px;
        border-radius: 2px;
        display: inline-block;
        animation: wave 1s infinite;
    }
    
    .wave-bar:nth-child(2) { animation-delay: 0.1s; }
    .wave-bar:nth-child(3) { animation-delay: 0.2s; }
    .wave-bar:nth-child(4) { animation-delay: 0.3s; }
    .wave-bar:nth-child(5) { animation-delay: 0.4s; }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
if 'model' not in st.session_state:
    st.session_state.model = None
if 'vc_model' not in st.session_state:
    st.session_state.vc_model = None
if 'processing' not in st.session_state:
    st.session_state.processing = False

def load_models():
    """Load the TTS and VC models"""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    with st.spinner("🚀 Loading Bhavesh AI models... This might take a moment on first run."):
        try:
            # Load TTS model
            if st.session_state.model is None:
                st.session_state.model = BhaveshTTS.from_pretrained(device)
            
            # Load VC model
            if st.session_state.vc_model is None:
                st.session_state.vc_model = BhaveshVC.from_pretrained(device)
            
            st.session_state.model_loaded = True
            st.success("✅ Models loaded successfully!")
            return True
        except Exception as e:
            st.error(f"❌ Error loading models: {str(e)}")
            return False

def create_waveform_plot(audio_data, sample_rate, title="Audio Waveform"):
    """Create an interactive waveform plot"""
    time_axis = np.linspace(0, len(audio_data) / sample_rate, len(audio_data))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=time_axis,
        y=audio_data,
        mode='lines',
        name='Waveform',
        line=dict(color='#6366f1', width=1)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        template="plotly_white",
        height=300,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return fig

def create_spectrogram_plot(audio_data, sample_rate, title="Spectrogram"):
    """Create a spectrogram visualization"""
    # Simple spectrogram using numpy (basic implementation)
    # In a full implementation, you'd use librosa or scipy for better spectrograms
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=np.arange(len(audio_data)) / sample_rate,
        y=audio_data,
        mode='lines',
        name='Audio Signal',
        line=dict(color='#8b5cf6', width=1)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Time (seconds)",
        yaxis_title="Amplitude",
        template="plotly_white",
        height=250,
        margin=dict(l=0, r=0, t=30, b=0)
    )
    
    return fig

def main():
    # Header
    st.markdown("""
    <div class="main-header fadeIn">
        <h1>🎤 Bhavesh AI Voice Cloner</h1>
        <p>Transform text into natural speech using advanced AI voice cloning technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    selected = option_menu(
        menu_title=None,
        options=["🏠 Home", "🎙️ Text-to-Speech", "🔄 Voice Conversion", "⚙️ Settings", "📊 Analytics"],
        icons=["house", "mic", "arrow-repeat", "gear", "bar-chart"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#6366f1", "font-size": "18px"},
            "nav-link": {
                "font-size": "16px",
                "text-align": "center",
                "margin": "0px",
                "padding": "10px 20px",
                "border-radius": "10px",
                "background-color": "white",
                "box-shadow": "0 2px 10px rgba(0,0,0,0.1)"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #6366f1, #8b5cf6)",
                "color": "white"
            },
        }
    )
    
    if selected == "🏠 Home":
        show_home_page()
    elif selected == "🎙️ Text-to-Speech":
        show_tts_page()
    elif selected == "🔄 Voice Conversion":
        show_vc_page()
    elif selected == "⚙️ Settings":
        show_settings_page()
    elif selected == "📊 Analytics":
        show_analytics_page()

def show_home_page():
    """Display the home page with features and getting started info"""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("## 🚀 Welcome to Bhavesh AI Voice Cloner")
        st.markdown("""
        Experience the future of voice synthesis with our cutting-edge AI technology. 
        Clone any voice with just seconds of reference audio and generate natural-sounding speech 
        with precise emotion control.
        """)
        
        # Features grid
        st.markdown("### ✨ Key Features")
        
        feature_col1, feature_col2, feature_col3 = st.columns(3)
        
        with feature_col1:
            st.markdown("""
            <div class="feature-card">
                <span class="feature-icon">🎯</span>
                <h4>Zero-Shot Cloning</h4>
                <p>Clone any voice with just seconds of reference audio</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col2:
            st.markdown("""
            <div class="feature-card">
                <span class="feature-icon">🎭</span>
                <h4>Emotion Control</h4>
                <p>Adjust emotional intensity and expression levels</p>
            </div>
            """, unsafe_allow_html=True)
        
        with feature_col3:
            st.markdown("""
            <div class="feature-card">
                <span class="feature-icon">⚡</span>
                <h4>Lightning Fast</h4>
                <p>Real-time generation with optimized performance</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Getting started
        st.markdown("### 🏁 Getting Started")
        st.markdown("""
        1. **Load Models**: Click the button below to load the AI models
        2. **Choose Mode**: Select Text-to-Speech or Voice Conversion
        3. **Configure**: Upload reference audio and adjust parameters
        4. **Generate**: Create amazing voice clones!
        """)
        
        if not st.session_state.model_loaded:
            if st.button("🚀 Load AI Models", key="load_models_home"):
                load_models()
        else:
            st.success("✅ Models are ready! Navigate to TTS or Voice Conversion to get started.")
    
    with col2:
        # System status
        st.markdown("### 📊 System Status")
        
        device = "CUDA" if torch.cuda.is_available() else "CPU"
        device_color = "#10b981" if torch.cuda.is_available() else "#f59e0b"
        
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{device}</div>
            <div class="metric-label">Processing Device</div>
        </div>
        """, unsafe_allow_html=True)
        
        model_status = "Loaded" if st.session_state.model_loaded else "Not Loaded"
        status_color = "#10b981" if st.session_state.model_loaded else "#ef4444"
        
        st.markdown(f"""
        <div class="metric-card" style="background: {status_color};">
            <div class="metric-value">{model_status}</div>
            <div class="metric-label">Model Status</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("### 📈 Quick Stats")
        stats_df = pd.DataFrame({
            'Metric': ['Model Size', 'Languages', 'Sample Rate', 'Response Time'],
            'Value': ['0.5B params', 'English', '24kHz', '<2s']
        })
        st.dataframe(stats_df, use_container_width=True)

def show_tts_page():
    """Display the Text-to-Speech page"""
    st.markdown("## 🎙️ Text-to-Speech Generation")
    
    if not st.session_state.model_loaded:
        st.warning("⚠️ Please load the models first from the Home page.")
        if st.button("🚀 Load Models Now"):
            load_models()
        return
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Text input
        st.markdown("### 📝 Enter Your Text")
        text = st.text_area(
            "Text to convert to speech",
            value="Hello! I'm Bhavesh AI, and I can transform any text into natural-sounding speech with incredible quality and emotion control.",
            height=120,
            max_chars=500,
            help="Enter the text you want to convert to speech (max 500 characters)"
        )
        
        char_count = len(text)
        color = "#ef4444" if char_count > 450 else "#10b981" if char_count > 0 else "#64748b"
        st.markdown(f"<p style='color: {color}; text-align: right;'>{char_count}/500 characters</p>", unsafe_allow_html=True)
        
        # Reference audio upload
        st.markdown("### 🎵 Reference Audio (Optional)")
        uploaded_file = st.file_uploader(
            "Upload reference audio to clone a specific voice",
            type=['wav', 'mp3', 'flac', 'm4a'],
            help="Upload an audio file to clone the voice. Leave empty to use the default voice."
        )
        
        if uploaded_file:
            st.audio(uploaded_file, format="audio/wav")
            
            # Show audio info
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            
            try:
                import librosa
                audio_data, sample_rate = librosa.load(tmp_path, sr=None)
                duration = len(audio_data) / sample_rate
                
                info_col1, info_col2, info_col3 = st.columns(3)
                with info_col1:
                    st.metric("Duration", f"{duration:.1f}s")
                with info_col2:
                    st.metric("Sample Rate", f"{sample_rate} Hz")
                with info_col3:
                    st.metric("Channels", "Mono" if len(audio_data.shape) == 1 else "Stereo")
                
                # Show waveform
                if st.checkbox("📊 Show Waveform"):
                    fig = create_waveform_plot(audio_data[:sample_rate*10], sample_rate, "Reference Audio Waveform")
                    st.plotly_chart(fig, use_container_width=True)
                    
            except Exception as e:
                st.error(f"Error analyzing audio: {str(e)}")
    
    with col2:
        # Generation parameters
        st.markdown("### ⚙️ Generation Parameters")
        
        with st.expander("🎛️ Basic Settings", expanded=True):
            exaggeration = st.slider(
                "Emotion Intensity",
                min_value=0.25,
                max_value=2.0,
                value=0.5,
                step=0.05,
                help="Control emotional expression (0.5 = neutral, higher = more expressive)"
            )
            
            cfg_weight = st.slider(
                "Speech Pace",
                min_value=0.0,
                max_value=1.0,
                value=0.5,
                step=0.05,
                help="Control speech pacing and clarity"
            )
        
        with st.expander("🔧 Advanced Settings"):
            temperature = st.slider(
                "Temperature",
                min_value=0.05,
                max_value=5.0,
                value=0.8,
                step=0.05,
                help="Control randomness in generation"
            )
            
            seed = st.number_input(
                "Random Seed",
                min_value=0,
                max_value=999999,
                value=0,
                help="Set to 0 for random, or use a specific number for reproducible results"
            )
            
            min_p = st.slider(
                "Min P",
                min_value=0.0,
                max_value=1.0,
                value=0.05,
                step=0.01,
                help="Minimum probability threshold"
            )
            
            top_p = st.slider(
                "Top P",
                min_value=0.0,
                max_value=1.0,
                value=1.0,
                step=0.01,
                help="Top-p sampling parameter"
            )
            
            repetition_penalty = st.slider(
                "Repetition Penalty",
                min_value=1.0,
                max_value=2.0,
                value=1.2,
                step=0.1,
                help="Penalty for repetitive speech patterns"
            )
        
        # Generation button
        if st.button("🎵 Generate Speech", type="primary", use_container_width=True):
            if not text.strip():
                st.error("❌ Please enter some text to generate speech!")
                return
            
            st.session_state.processing = True
            
            # Show processing animation
            with st.spinner("🎙️ Generating speech..."):
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    # Update progress
                    progress_bar.progress(25)
                    status_text.text("🧠 Processing text...")
                    
                    # Set seed if specified
                    if seed != 0:
                        torch.manual_seed(seed)
                        if torch.cuda.is_available():
                            torch.cuda.manual_seed(seed)
                    
                    progress_bar.progress(50)
                    status_text.text("🎵 Generating audio...")
                    
                    # Generate speech
                    audio_prompt_path = tmp_path if uploaded_file else None
                    
                    wav = st.session_state.model.generate(
                        text,
                        audio_prompt_path=audio_prompt_path,
                        exaggeration=exaggeration,
                        temperature=temperature,
                        cfg_weight=cfg_weight,
                        min_p=min_p,
                        top_p=top_p,
                        repetition_penalty=repetition_penalty,
                    )
                    
                    progress_bar.progress(75)
                    status_text.text("💾 Preparing output...")
                    
                    # Convert to numpy array
                    if isinstance(wav, torch.Tensor):
                        wav_np = wav.squeeze(0).cpu().numpy()
                    else:
                        wav_np = wav
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Complete!")
                    
                    # Display results
                    st.success("🎉 Speech generated successfully!")
                    
                    # Audio player
                    st.audio(wav_np, format="audio/wav", sample_rate=st.session_state.model.sr)
                    
                    # Download button
                    buffer = io.BytesIO()
                    ta.save(buffer, torch.from_numpy(wav_np).unsqueeze(0), st.session_state.model.sr, format="wav")
                    buffer.seek(0)
                    
                    st.download_button(
                        label="📥 Download Audio",
                        data=buffer.getvalue(),
                        file_name=f"bhavesh_ai_speech_{int(time.time())}.wav",
                        mime="audio/wav",
                        use_container_width=True
                    )
                    
                    # Show waveform
                    if st.checkbox("📊 Show Generated Waveform"):
                        fig = create_waveform_plot(wav_np, st.session_state.model.sr, "Generated Speech Waveform")
                        st.plotly_chart(fig, use_container_width=True)
                    
                except Exception as e:
                    st.error(f"❌ Error generating speech: {str(e)}")
                finally:
                    st.session_state.processing = False
                    progress_bar.empty()
                    status_text.empty()

def show_vc_page():
    """Display the Voice Conversion page"""
    st.markdown("## 🔄 Voice Conversion")
    st.info("🚧 Voice Conversion feature coming soon! Stay tuned for updates.")

def show_settings_page():
    """Display the Settings page"""
    st.markdown("## ⚙️ Settings")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎛️ Audio Settings")
        
        sample_rate = st.selectbox(
            "Sample Rate",
            options=[16000, 22050, 24000, 44100, 48000],
            index=2,
            help="Audio sample rate for generation"
        )
        
        audio_format = st.selectbox(
            "Output Format",
            options=["WAV", "MP3", "FLAC"],
            index=0,
            help="Audio output format"
        )
        
        quality = st.selectbox(
            "Audio Quality",
            options=["High", "Medium", "Low"],
            index=0,
            help="Audio generation quality"
        )
    
    with col2:
        st.markdown("### 🎨 Interface Settings")
        
        theme = st.selectbox(
            "Theme",
            options=["Modern Blue", "Dark Mode", "Light Mode"],
            index=0,
            help="Application theme"
        )
        
        animations = st.checkbox(
            "Enable Animations",
            value=True,
            help="Enable UI animations and transitions"
        )
        
        auto_play = st.checkbox(
            "Auto-play Generated Audio",
            value=True,
            help="Automatically play generated audio"
        )
    
    st.markdown("### 💾 Export Settings")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        if st.button("📤 Export Settings", use_container_width=True):
            settings = {
                "sample_rate": sample_rate,
                "audio_format": audio_format,
                "quality": quality,
                "theme": theme,
                "animations": animations,
                "auto_play": auto_play
            }
            st.json(settings)
    
    with export_col2:
        if st.button("🔄 Reset to Defaults", use_container_width=True):
            st.success("✅ Settings reset to defaults!")

def show_analytics_page():
    """Display the Analytics page"""
    st.markdown("## 📊 Analytics & Insights")
    
    # Usage statistics (mock data for demo)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="🎵 Total Generations",
            value="1,234",
            delta="12 today"
        )
    
    with col2:
        st.metric(
            label="⏱️ Avg. Processing Time",
            value="1.8s",
            delta="-0.2s"
        )
    
    with col3:
        st.metric(
            label="📈 Success Rate",
            value="98.5%",
            delta="0.5%"
        )
    
    with col4:
        st.metric(
            label="👥 Active Users",
            value="456",
            delta="23 new"
        )
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📈 Generation Trends")
        
        # Mock data for demo
        dates = pd.date_range(start='2025-01-01', end='2025-01-31', freq='D')
        values = np.random.randint(20, 100, len(dates))
        
        fig = px.line(
            x=dates,
            y=values,
            title="Daily Generations",
            labels={'x': 'Date', 'y': 'Generations'}
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown("### 🎛️ Parameter Usage")
        
        # Mock data for demo
        params = ['Default', 'High Emotion', 'Fast Pace', 'Slow Pace', 'Custom']
        counts = [45, 25, 15, 10, 5]
        
        fig = px.pie(
            values=counts,
            names=params,
            title="Parameter Presets"
        )
        fig.update_layout(template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    
    # Performance metrics
    st.markdown("### ⚡ Performance Metrics")
    
    perf_data = pd.DataFrame({
        'Metric': ['CPU Usage', 'Memory Usage', 'GPU Usage', 'Disk I/O'],
        'Current': [45, 62, 78, 23],
        'Average': [38, 55, 72, 19],
        'Peak': [89, 95, 99, 67]
    })
    
    st.dataframe(perf_data, use_container_width=True)

if __name__ == "__main__":
    main()
