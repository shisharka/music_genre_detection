import numpy as np
import matplotlib.pyplot as plt
import copy
from scipy.signal import stft
import sys
from librosa import load, display, power_to_db


def spectrogram(data, fft_size=1024, step_size=512):
    """
    creates a spectrogram
    log: take the log of the spectrogram
    """
    _, _, specgram = np.abs(stft(data, nperseg=fft_size, noverlap=step_size, window='blackman'))

    return specgram


def hz2mel(hz):
    """Convert a value in Hertz to Mels"""
    return 2595 * np.log10(1+hz/700.)
   

def mel2hz(mel):
    """Convert a value in Mels to Hertz"""
    return 700*(10**(mel/2595.0)-1)


def mel_binning_matrix(window_size, sample_rate, num_mel_bands):
    """
    Function that returns a matrix that converts a regular STFT
    to a mel-spaced STFT, by binning coefficients.
    
    window_size: the window length used to compute the spectrograms
    sample_rate: the sample frequency of the input audio
    num_mel_bands: the number of desired mel bands
    
    The output is a matrix with dimensions (window_size/2 + 1, num_bands)
    """
    min_freq, max_freq = 0, sample_rate / 2
    min_mel = hz2mel(min_freq)
    max_mel = hz2mel(max_freq)
    num_specgram_components = window_size / 2 + 1
    m = np.zeros((num_specgram_components, num_mel_bands))
    
    # there are (num_mel_bands + 2) filter boundaries / centers
    r = np.arange(num_mel_bands + 2)

    # evenly spaced filter boundaries in the mel domain:
    mel_filter_boundaries = r * (max_mel - min_mel) / (num_mel_bands + 1) + min_mel
    
    # gets the unnormalised filter coefficient of filter 'idx' for a given mel value
    def coeff(idx, mel):
        lo, cen, hi = mel_filter_boundaries[idx:idx+3]
        if mel <= lo or mel >= hi:
            return 0
        # linearly interpolate
        if lo <= mel <= cen:
            return (mel - lo) / (cen - lo)
        elif cen <= mel <= hi:
            return 1 - (mel - cen) / (hi - cen)
            
    for k in xrange(num_specgram_components):
        # compute mel representation of the given specgram component idx
        freq = k / float(num_specgram_components) * (sample_rate / 2)
        mel = hz2mel(freq)
        for i in xrange(num_mel_bands):
            m[k, i] = coeff(i, mel)

    return m


def make_mel(spectrogram, mel_filter):
    mel_spec = mel_filter.dot(spectrogram)
    return mel_spec

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify path to an audio file')
    else:
        file_path = sys.argv[1]
        ### Parameters ###
        fft_size = 1024 # window size for the FFT
        step_size = fft_size/2 # distance to slide along the window (in time)
        # For mels
        n_mels = 128 # number of mel frequency bins
        try:
            data, sample_rate = load(file_path, mono=True)
            duration = data.shape[0] * 1.0 / sample_rate
            spectrogram = spectrogram(data, fft_size=fft_size, 
                                            step_size=step_size)
            # Generate melspectrogram
            mel_filter = mel_binning_matrix(fft_size, sample_rate, n_mels).T
            mel_spec = make_mel(spectrogram, mel_filter)

            plt.figure(figsize=(10, 4))
            display.specshow(power_to_db(mel_spec), y_axis='mel', x_axis='time')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Mel spectrogram')
            plt.tight_layout()
            plt.show()
        except:
            print('Bad input file path: ' + file_path)