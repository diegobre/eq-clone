"""
EQ Clone – Premium EQ Matching & Impulse Response Generator
============================================================
A Streamlit web application that performs spectral matching between
a Reference track and a Target track, generating an Impulse Response
(.wav) file for use in convolution plugins (VSTs).

Run:  streamlit run app.py
"""

import streamlit as st
import librosa
import numpy as np
import scipy.signal
import soundfile as sf
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import io

# ────────────────────────────────────────────────────────────────
# Page Configuration
# ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="EQ Clone — IR Generator",
    page_icon="🎧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ────────────────────────────────────────────────────────────────
# Premium Dark Theme — Custom CSS
# ────────────────────────────────────────────────────────────────
CUSTOM_CSS = """
<style>
/* ---------- Google Font ---------- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');

/* ---------- Root variables ---------- */
:root {
    --bg-primary: #121214;
    --bg-secondary: #1a1a1d;
    --bg-card: #18181b;
    --bg-card-border: #27272a;
    --accent-primary: #ff5252;
    --accent-secondary: #ff7675;
    --text-primary: #f4f4f5;
    --text-secondary: #a1a1aa;
    --gradient-btn: #27272a;
}

/* ---------- Global ---------- */
html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}

/* Main block container */
[data-testid="stAppViewContainer"] > .main {
    background: var(--bg-primary) !important;
}

.block-container {
    padding-top: 2rem !important;
    max-width: 1200px !important;
}

/* ---------- Scrollbar ---------- */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: #27272a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-primary); }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--bg-card-border) !important;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
    font-weight: 700 !important;
    letter-spacing: -0.02em;
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] label {
    color: var(--text-secondary) !important;
    font-size: 0.88rem !important;
}

/* ---------- Slider Track ---------- */
[data-testid="stSlider"] > div > div > div > div {
    background: var(--accent-primary) !important;
}

[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: var(--accent-primary) !important;
    font-weight: 600 !important;
}

/* ---------- Headers ---------- */
h1, h2, h3, h4 {
    font-family: 'Inter', sans-serif !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
}

/* Gradient hero text */
.hero-title {
    font-size: 2.5rem !important;
    font-weight: 400 !important;
    color: var(--text-primary);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    line-height: 1.1;
    margin-bottom: 0.2rem;
}

.hero-subtitle {
    color: var(--text-secondary) !important;
    font-size: 1.05rem;
    font-weight: 400;
    max-width: 700px;
    line-height: 1.6;
    margin-bottom: 2rem;
}

/* ---------- Upload Cards ---------- */
.upload-card {
    background: var(--bg-card);
    border: 1px solid var(--bg-card-border);
    border-radius: 8px;
    padding: 1.6rem 1.4rem;
    transition: all 0.2s ease;
}

.upload-card:hover {
    border-color: var(--accent-primary);
}

.upload-card h3 {
    font-size: 1.15rem !important;
    margin-bottom: 0.8rem;
}

.card-icon {
    font-size: 2rem;
    margin-bottom: 0.5rem;
    display: block;
}

/* ---------- File Uploader Override ---------- */
[data-testid="stFileUploader"] {
    background: transparent !important;
}

[data-testid="stFileUploader"] section {
    background: var(--bg-secondary) !important;
    border: 1px solid var(--bg-card-border) !important;
    border-radius: 8px !important;
    padding: 1rem !important;
    transition: all 0.2s ease !important;
}

[data-testid="stFileUploader"] section:hover {
    border-color: var(--accent-primary) !important;
}

[data-testid="stFileUploader"] small {
    color: var(--text-secondary) !important;
}

/* ---------- Buttons ---------- */
[data-testid="stButton"] > button,
.stDownloadButton > button {
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.65rem 2rem !important;
    transition: all 0.3s ease !important;
    letter-spacing: 0.01em !important;
}

/* Primary "Analizar" button */
[data-testid="stButton"] > button[kind="primary"],
button[kind="primary"] {
    background: var(--bg-card) !important;
    border: 1px solid var(--bg-card-border) !important;
    color: var(--text-primary) !important;
    text-transform: uppercase;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
}

[data-testid="stButton"] > button[kind="primary"]:hover {
    border-color: var(--accent-primary) !important;
    color: var(--accent-primary) !important;
}

/* Download button */
.stDownloadButton > button {
    background: var(--bg-card) !important;
    border: 1px solid var(--accent-primary) !important;
    color: var(--accent-primary) !important;
    font-size: 0.9rem !important;
    padding: 0.8rem 2.5rem !important;
    text-transform: uppercase;
}

.stDownloadButton > button:hover {
    background: var(--accent-primary) !important;
    color: #121214 !important;
}

/* ---------- Info / Success / Error Boxes ---------- */
[data-testid="stAlert"] {
    background: var(--bg-card) !important;
    border-radius: 8px !important;
    border: 1px solid var(--bg-card-border) !important;
    border-left: 3px solid var(--accent-primary) !important;
}

div[data-testid="stAlert"] p {
    color: var(--text-secondary) !important;
}

/* Success */
div.stSuccess {
    border-left-color: #22c55e !important;
}

/* ---------- Spinner ---------- */
.stSpinner > div {
    border-top-color: var(--accent-cyan) !important;
}

/* ---------- Plot container ---------- */
[data-testid="stImage"],
.stPlotlyChart,
[data-testid="stPyplotChart"] {
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid var(--bg-card-border);
}

/* ---------- Divider ---------- */
hr {
    border-color: var(--bg-card-border) !important;
    margin: 2rem 0 !important;
}

/* ---------- Section Header ---------- */
.section-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 1.2rem;
}

.section-header .dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-primary);
    display: inline-block;
}

/* ---------- Result card ---------- */
.result-card {
    background: var(--bg-card);
    border: 1px solid var(--bg-card-border);
    border-radius: 8px;
    padding: 1.5rem;
    margin-top: 1.5rem;
}

/* ---------- Footer ---------- */
.footer {
    text-align: center;
    padding: 2rem 0 1rem;
    color: var(--text-secondary);
    font-size: 0.8rem;
    opacity: 0.6;
}

/* ---------- Hide Streamlit boilerplate ---------- */
#MainMenu { visibility: hidden; }
header { visibility: hidden; }
footer { visibility: hidden; }

/* Remove default padding at top */
.appview-container .main .block-container {
    padding-top: 2rem !important;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ────────────────────────────────────────────────────────────────
# DSP Helper Functions
# ────────────────────────────────────────────────────────────────

def load_and_normalize(file_uploader, target_sr: int = 44100):
    """
    Load audio from a Streamlit file uploader.
    • Convert to mono
    • Resample to *target_sr*
    • Apply −1.0 dB gain for headroom
    """
    try:
        y, sr = librosa.load(file_uploader, sr=target_sr, mono=True)
        gain_linear = 10 ** (-1.0 / 20.0)      # ≈ 0.891
        y = y * gain_linear
        return y, sr
    except Exception as e:
        return None, str(e)


def analyze_spectrum(y, n_fft: int = 2048, hop_length: int = 512):
    """Compute the average magnitude spectrum via STFT."""
    S = librosa.stft(y, n_fft=n_fft, hop_length=hop_length)
    mag = np.abs(S)
    return np.mean(mag, axis=1)


def smooth_spectrum(mag, window_length: int = 51, polyorder: int = 3):
    """Apply Savitzky‑Golay smoothing to a spectral envelope."""
    if window_length % 2 == 0:
        window_length += 1
    if len(mag) < window_length:
        window_length = len(mag) // 2 * 2 + 1
        if window_length < polyorder + 2:
            return mag
    return scipy.signal.savgol_filter(mag, window_length, polyorder)


def calculate_eq_curve(ref_mag, target_mag, amount, min_freq, max_freq, freqs):
    """
    EQ curve = (Reference / Target) ** Amount, masked by Safe Range.
    Frequencies outside [min_freq, max_freq] → 1.0 (no change).
    """
    epsilon = 1e-10
    ratio = (ref_mag + epsilon) / (target_mag + epsilon)
    ratio_scaled = ratio ** amount

    mask = (freqs >= min_freq) & (freqs <= max_freq)
    return np.where(mask, ratio_scaled, 1.0)


def generate_ir(eq_curve, n_fft: int = 2048):
    """
    Generate a linear‑phase Impulse Response by applying *eq_curve*
    to a Dirac pulse in the frequency domain (IFFT → window → normalize).
    """
    # Reconstruct full symmetric magnitude (DC … Nyquist … mirror)
    mag_full = np.concatenate([eq_curve, eq_curve[-2:0:-1]])

    # IFFT with zero‑phase → shift → window
    ir_time = np.fft.ifft(mag_full)
    ir_real = np.real(ir_time)

    ir_shifted = np.fft.ifftshift(ir_real)
    window = scipy.signal.windows.hann(len(ir_shifted))
    ir_final = ir_shifted * window

    # Normalize peak to −0.1 dB (≈ 0.99)
    peak = np.max(np.abs(ir_final))
    if peak > 0:
        ir_final = ir_final / peak * 0.99

    return ir_final


def apply_ir(audio, ir):
    """
    Apply the generated Impulse Response to the audio using FFT convolution.
    Returns the processed audio normalized to -1 dB.
    """
    # FFT Convolution is faster for long signals
    processed = scipy.signal.fftconvolve(audio, ir, mode='full')
    
    # Trim to original length (optional, but usually desired for direct comparison)
    # acts like a reverb tail if we keep full mode. Let's keep full mode but normalize.
    
    # Normalize
    peak = np.max(np.abs(processed))
    if peak > 0:
        processed = processed / peak * 0.89  # approx -1dB
        
    return processed


# ────────────────────────────────────────────────────────────────
# Sidebar — Parameters
# ────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🎧 EQ Clone")
    st.markdown(
        "<p style='color:#94a3b8;font-size:0.85rem;margin-top:-0.5rem'>"
        "Processing Parameters</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        "<p style='color:#94a3b8;font-size:0.85rem'>"
        "All parameters are optimized for Infinity Bass.</p>",
        unsafe_allow_html=True,
    )

# Hardcoded defaults for removed UI sliders
amount = 1.0
min_freq = 40
max_freq = 18000
smooth_amt = 51


# ────────────────────────────────────────────────────────────────
# Main Area — Hero
# ────────────────────────────────────────────────────────────────

st.markdown(
    '<p class="hero-title">INFINITY EQ</p>',
    unsafe_allow_html=True,
)
st.markdown(
    '<p class="hero-subtitle">'
    'Upload a <strong style="color:#a1a1aa">Reference</strong> track '
    'and a <strong style="color:#a1a1aa">Target</strong> track. '
    'The app will generate a concurrent <strong style="color:#ff5252">audio file (.wav)</strong> '
    'for monitoring and download.</p>',
    unsafe_allow_html=True,
)


# ────────────────────────────────────────────────────────────────
# File Uploaders
# ────────────────────────────────────────────────────────────────

def reset_processing():
    st.session_state.processed = False

col1, spacer, col2 = st.columns([1, 0.08, 1])

with col1:
    st.markdown(
        '<div class="upload-card">'
        '<h3 style="color:#f4f4f5;font-size:1rem;text-transform:uppercase;letter-spacing:0.05em">A. Reference</h3>'
        '</div>',
        unsafe_allow_html=True,
    )
    ref_file = st.file_uploader(
        "Upload Reference file",
        type=["wav", "mp3", "flac"],
        key="ref",
        label_visibility="collapsed",
        on_change=reset_processing
    )
    if ref_file:
        st.audio(ref_file, format="audio/wav")

with col2:
    st.markdown(
        '<div class="upload-card">'
        '<h3 style="color:#f4f4f5;font-size:1rem;text-transform:uppercase;letter-spacing:0.05em">B. Target</h3>'
        '</div>',
        unsafe_allow_html=True,
    )
    target_file = st.file_uploader(
        "Upload Target file",
        type=["wav", "mp3", "flac"],
        key="target",
        label_visibility="collapsed",
        on_change=reset_processing
    )
    if target_file:
        st.audio(target_file, format="audio/wav")


# ────────────────────────────────────────────────────────────────
# Processing State Management
# ────────────────────────────────────────────────────────────────

if "processed" not in st.session_state:
    st.session_state.processed = False
    st.session_state.base_data = {}

# ────────────────────────────────────────────────────────────────
# Processing
# ────────────────────────────────────────────────────────────────

if ref_file and target_file:
    st.markdown("<br>", unsafe_allow_html=True)
    center_col = st.columns([1, 2, 1])[1]
    with center_col:
        run = st.button("⚡  Analyze Base Audio", type="primary", use_container_width=True)

    if run:
        with st.spinner("Analyzing base spectrums (this is done only once)…"):
            target_sr = 44100
            n_fft = 4096
            hop_length = n_fft // 4

            # 1 — Load
            ref_audio, info_ref = load_and_normalize(ref_file, target_sr)
            target_audio, info_tgt = load_and_normalize(target_file, target_sr)

            error = None
            if ref_audio is None:
                error = f"Error loading Reference: {info_ref}"
            if target_audio is None:
                error = f"Error loading Target: {info_tgt}"

            if error:
                st.error(error)
                st.session_state.processed = False
            else:
                # 2 — Spectrum
                ref_spec = analyze_spectrum(ref_audio, n_fft, hop_length)
                target_spec = analyze_spectrum(target_audio, n_fft, hop_length)

                # 4 — Frequency axis
                freqs = librosa.fft_frequencies(sr=target_sr, n_fft=n_fft)

                # Store base data in session state
                st.session_state.base_data = {
                    "ref_spec": ref_spec,
                    "target_spec": target_spec,
                    "freqs": freqs,
                    "ref_audio": ref_audio,
                    "target_audio": target_audio,
                    "target_sr": target_sr,
                    "n_fft": n_fft
                }
                st.session_state.processed = True

# ────────────────────────────────────────────────────────────────
# Results Display (Persistent/Dynamic)
# ────────────────────────────────────────────────────────────────
if st.session_state.get("processed"):
    base = st.session_state.base_data
    
    # Unpack base variables
    ref_spec = base["ref_spec"]
    target_spec = base["target_spec"]
    freqs = base["freqs"]
    ref_audio = base["ref_audio"]
    target_audio = base["target_audio"]
    target_sr = base["target_sr"]
    n_fft = base["n_fft"]

    # ─── Dynamic DSP Calculation ─────────────────────────
    with st.spinner("Updating EQ in real-time..."):
        # 3 — Smooth
        ref_smooth = smooth_spectrum(ref_spec, window_length=smooth_amt)
        target_smooth = smooth_spectrum(target_spec, window_length=smooth_amt)

        # 5 — EQ Curve
        eq_curve = calculate_eq_curve(
            ref_smooth, target_smooth, amount, min_freq, max_freq, freqs,
        )

        # 6 — Estimated result (visual only)
        estimated_result = target_smooth * eq_curve

        # 7 — Generate IR
        ir_audio = generate_ir(eq_curve, n_fft=n_fft)
        
        # 8 — Apply IR for preview
        preview_audio = apply_ir(target_audio, ir_audio)

    # ─── Visualization ───────────────────────────────────
    st.markdown("---")
    st.markdown(
        '<div class="section-header">'
        '<span class="dot"></span>'
        '<h3 style="margin:0;color:#eef2ff">Analyzer</h3>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Dark‑themed Matplotlib figure
    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor("#0a0a0c")
    ax.set_facecolor("#0f0f13")

    def plot_db(f, mag, label, color, ls="-", lw=2, alpha=1.0):
        mag_db = 20 * np.log10(mag + 1e-10)
        ax.plot(f, mag_db, label=label, color=color,
                linestyle=ls, linewidth=lw, alpha=alpha)

    plot_db(freqs, ref_smooth, "Reference", "#22c55e")
    plot_db(freqs, target_smooth, "Target Original", "#ef4444", ls="--")
    plot_db(freqs, estimated_result, "Estimated Target (Matched)", "#3b82f6", lw=2.5)

    # Safe‑range shading
    ax.axvspan(0, min_freq, color="#20151f", alpha=0.6, label="Excluded")
    ax.axvspan(max_freq, target_sr / 2, color="#20151f", alpha=0.6)

    ax.set_xscale("log")
    ax.set_xlim(20, 20_000)
    ax.set_xlabel("Frequency (Hz)", color="#a1a1aa", fontsize=10, fontfamily="Inter")
    ax.set_ylabel("Magnitude (dB)", color="#a1a1aa", fontsize=10, fontfamily="Inter")
    ax.tick_params(colors="#52525b", labelsize=9)
    ax.grid(True, which="both", ls="-", alpha=0.1, color="#3f3f46")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#27272a")
    ax.spines["bottom"].set_color("#27272a")

    legend = ax.legend(
        loc="upper right",
        fontsize=9,
        facecolor="#18181b",
        edgecolor="#27272a",
        labelcolor="#d4d4d8",
        framealpha=1.0,
    )

    # Custom x‑tick labels
    ax.xaxis.set_major_formatter(
        ticker.FuncFormatter(
            lambda x, _: f"{x/1000:.0f}k" if x >= 1000 else f"{x:.0f}"
        )
    )

    fig.tight_layout()
    st.pyplot(fig)

    # ─── Preview (A/B) ───────────────────────────────────
    st.markdown(
        '<div class="result-card" style="margin-top:1rem;">'
        '<div class="section-header">'
        '<span class="dot" style="background:#a1a1aa;"></span>'
        '<h3 style="margin:0;color:#f4f4f5;text-transform:uppercase;font-size:1rem;letter-spacing:0.05em">A/B Listen</h3>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Toggle for A/B
    ab_mode = st.radio(
        "Select what you want to hear:",
        options=["Original (A)", "Cloned (B)"],
        horizontal=True,
        label_visibility="collapsed",
        key="ab_toggle"
    )

    if ab_mode == "Original (A)":
        audio_to_play = target_audio
        st.caption("🔊 Playing: **Original Target**")
    else:
        audio_to_play = preview_audio
        st.caption("🔊 Playing: **Target with Cloned EQ**")

    # Write to buffer for standard st.audio
    preview_buffer = io.BytesIO()
    sf.write(preview_buffer, audio_to_play, target_sr, format="WAV")
    
    st.audio(preview_buffer, format="audio/wav")
    
    st.markdown('</div>', unsafe_allow_html=True)

    # ─── Download ────────────────────────────────────────
    st.markdown(
        '<div class="result-card">'
        '<div class="section-header">'
        '<span class="dot" style="background:#22c55e;"></span>'
        '<h3 style="margin:0;color:#f4f4f5;text-transform:uppercase;font-size:1rem;letter-spacing:0.05em">Output</h3>'
        '</div>',
        unsafe_allow_html=True,
    )

    buffer_audio = io.BytesIO()
    sf.write(buffer_audio, preview_audio, target_sr, format="WAV", subtype="PCM_24")
    buffer_audio.seek(0)

    center_dl = st.columns([1, 2, 1])[1]
    with center_dl:
        st.download_button(
            label="⬇️  Download Processed Audio (.wav)",
            data=buffer_audio,
            file_name="EQ_Clone_Processed_Audio.wav",
            mime="audio/wav",
            use_container_width=True,
        )

else:
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("☝️ Please upload both audio files to begin.")


# ────────────────────────────────────────────────────────────────
# Footer
# ────────────────────────────────────────────────────────────────
st.markdown(
    '<div class="footer">EQ Clone · Built with Streamlit & DSP ❤️</div>',
    unsafe_allow_html=True,
)
