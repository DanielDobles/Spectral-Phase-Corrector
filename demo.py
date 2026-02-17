import numpy as np
import soundfile as sf
from spectral_corrector import SpectralPhaseCorrector
import os

def generate_broken_stereo(duration=5, sr=44100):
    """
    Generates a stereo signal where low frequencies are in phase 
    but mid frequencies (500Hz - 1500Hz) are 180 degrees out of phase.
    """
    t = np.linspace(0, duration, int(sr * duration))
    
    # Bass: 100Hz (In phase)
    bass = 0.5 * np.sin(2 * np.pi * 100 * t)
    
    # Mids: 1000Hz (In phase for L, Out of phase for R)
    mids_l = 0.4 * np.sin(2 * np.pi * 1000 * t)
    mids_r = 0.4 * np.sin(2 * np.pi * 1000 * t + np.pi) # 180 deg shift
    
    # Highs: Noise (Random phase)
    highs_l = 0.1 * np.random.normal(0, 1, len(t))
    highs_r = 0.1 * np.random.normal(0, 1, len(t))
    
    l_chan = bass + mids_l + highs_l
    r_chan = bass + mids_r + highs_r
    
    audio = np.vstack([l_chan, r_chan])
    return audio, sr

if __name__ == "__main__":
    input_file = "broken_stereo.wav"
    output_file = "repaired_stereo.wav"
    
    print("Generating synthetic 'broken' stereo audio...")
    audio, sr = generate_broken_stereo()
    sf.write(input_file, audio.T, sr)
    
    print("\n--- Starting Phase Correction Pipeline ---")
    corrector = SpectralPhaseCorrector(sr=sr)
    # threshold_corr=0.0 means we target everything below 'neutral' coherence
    corrector.process(input_file, output_file, threshold_corr=0.0, plot=False)
    
    print("\nVerification:")
    if os.path.exists(output_file):
        print(f"Success! Repaired file saved: {output_file}")
        
        # Verify Improvement
        audio_orig, _ = librosa.load(input_file, sr=sr, mono=False)
        audio_fixed, _ = librosa.load(output_file, sr=sr, mono=False)
        
        # Calculate global correlation
        corr_orig = np.corrcoef(audio_orig[0], audio_orig[1])[0, 1]
        corr_fixed = np.corrcoef(audio_fixed[0], audio_fixed[1])[0, 1]
        
        print(f"Original Global Correlation: {corr_orig:.4f}")
        print(f"Repaired Global Correlation: {corr_fixed:.4f}")
        
        if corr_fixed > corr_orig:
            print("Status: SUCCESS - Phase coherence significantly improved.")
        else:
            print("Status: WARNING - No significant correlation improvement detected.")
