import librosa
import numpy as np
import matplotlib.pyplot as plt
from spectral_corrector import SpectralPhaseCorrector
import soundfile as sf
import os

def run_analysis():
    input_file = "Zduhac_Boj.mp3"
    output_file = "Zduhac_Boj_repaired.wav"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found.")
        return

    corrector = SpectralPhaseCorrector()
    
    print(f"Loading {input_file}...")
    audio_orig, sr = librosa.load(input_file, sr=None, mono=False)
    
    print("Processing with Spectral Phase Corrector...")
    # We call the internal methods to get the coherence before correction
    S_l, S_r = corrector.decompose(audio_orig)
    phase_l, phase_r, phase_diff, coherence_orig = corrector.analyze_phase(S_l, S_r)
    
    # Process and save
    corrector.process(input_file, output_file, threshold_corr=0.0, plot=False)
    
    # Load repaired to check coherence again
    audio_rep, _ = librosa.load(output_file, sr=sr, mono=False)
    S_l_rep, S_r_rep = corrector.decompose(audio_rep)
    _, _, _, coherence_rep = corrector.analyze_phase(S_l_rep, S_r_rep)
    
    print("Generating Comparison Plots...")
    plt.figure(figsize=(15, 12))
    
    # Plot 1: Original Coherence
    plt.subplot(3, 1, 1)
    librosa.display.specshow(coherence_orig, x_axis='time', y_axis='hz', sr=sr, hop_length=corrector.hop_length, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(label='Coherence')
    plt.title('ANTES: Salud Estéreo (Verde = Sano, Rojo = Cancelación)')
    
    # Plot 2: Mask (What we corrected)
    mask = corrector.calculate_mask(coherence_orig, threshold_corr=0.0)
    mask = corrector.apply_smoothing(mask)
    plt.subplot(3, 1, 2)
    librosa.display.specshow(mask, x_axis='time', y_axis='hz', sr=sr, hop_length=corrector.hop_length, cmap='magma')
    plt.colorbar(label='Intensidad')
    plt.title('CIRUGÍA: Mapa de Intervención (Zonas Reparadas)')
    
    # Plot 3: Repaired Coherence
    plt.subplot(3, 1, 3)
    librosa.display.specshow(coherence_rep, x_axis='time', y_axis='hz', sr=sr, hop_length=corrector.hop_length, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(label='Coherence')
    plt.title('DESPUÉS: Salud Estéreo Corregida (Mono-Compatible)')
    
    plt.tight_layout()
    plt.savefig('analisis_fase_zduhac.png')
    print("Visualización guardada en 'analisis_fase_zduhac.png'")
    
    # Correlation Summary
    corr_orig = np.corrcoef(audio_orig[0], audio_orig[1])[0, 1]
    corr_rep = np.corrcoef(audio_rep[0], audio_rep[1])[0, 1]
    print(f"\nCorrelación Global Original: {corr_orig:.4f}")
    print(f"Correlación Global Reparada: {corr_rep:.4f}")

if __name__ == "__main__":
    run_analysis()
