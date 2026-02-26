# 🌈 Spectral Phase Corrector

### *Surgical Spectral Alignment & Stereo Coherence Recovery*

---

**Spectral Phase Corrector** is a professional-grade DSP tool designed to detect and repair frequency-specific phase issues in stereo signals. Unlike global polarity flippers, this tool analyzes the audio in the frequency domain to surgically identify "Red Zones" (out-of-phase components) and rotate them back into alignment.

## 🚀 Key Features

- 🧠 **Surgical Spectral Analysis:** Uses STFT (Short-Time Fourier Transform) to decompose audio into high-resolution frequency bins.
- 📏 **Coherence Mapping:** Calculates spectral coherence and phase difference per bin to identify exactly where phase cancellation is occurring.
- 🛡️ **The Phase Wall:** Implements an automated correction mask that targets components with negative correlation (anti-phase).
- 📉 **Frequency-Dependent Weighting:** Prioritizes low-frequency stability where phase issues are most destructive to the "punch" and mono compatibility.
- 🤝 **Musical Smoothing:** Features exponential Attack/Release smoothing for the correction mask to prevent audible artifacts or "chatter".
- 📊 **Visual Diagnostics:** Generates detailed spectral reports showing phase distribution and coherence before and after correction.

## 🛠️ Technology Stack

| Module | Technology | Role |
|--------|-----------|------|
| **Digital Signal Processing** | NumPy + SciPy | Spectral decomposition & vector math |
| **Audio Ingestion** | Librosa + SoundFile | Multi-format loading & float32 processing |
| **Visualization** | Matplotlib | Diagnostic plots & coherence heatmaps |
| **Masking Logic** | Custom DSP Pipeline | Temporal smoothing & phase rotation |

## 📦 Installation & Setup

Ensure you have Python 3.8+ installed.

### Dependencies

Install the required libraries using pip:

```bash
pip install -r requirements.txt
```

*Requirements include: `numpy`, `scipy`, `librosa`, `soundfile`, `matplotlib`, `tqdm`.*

## 📖 How it Works

1. **Decomposition:** The stereo signal is split into Left and Right channels and converted to the frequency domain using STFT.
2. **Analysis:** The system calculates the cross-spectrum and coherence. Any bin with a correlation near -1.0 is flagged as out-of-phase.
3. **Masking:** A correction mask is generated, applying frequency-weighting to ensure the most critical bands are prioritized.
4. **Correction:** The phase of the flagged components is surgically rotated to match the reference channel.
5. **Reconstruction:** The signal is resynthesized using Inverse STFT (ISTFT) and saved as a high-fidelity 32-bit float WAV.

## 🚦 Quick Start (Demo)

You can test the corrector using the included demo script, which generates a "broken" stereo signal (out-of-phase mids) and repairs it:

```bash
python demo.py
```

---

> **⚠️ Note:** This tool is designed for surgical correction of phase-related artifacts. For best results, it is recommended to use high-bitrate or lossless source files (WAV, FLAC).
