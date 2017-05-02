import numpy as np
import librosa as lbr

GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal',
         'pop', 'reggae', 'rock']

def load_track(file_path):
    """ 
    function returns log from mel spectrogram values and song duration
    function arguments: file_path
    """
    input, sample_rate = lbr.load(file_path, mono = True)
    features = lbr.feature.melspectrogram(input, n_fft = 2048,
                                          hop_length = 1024, n_mels = 128)

    return(np.log(features), float(input.shape[0] / sample_rate))
