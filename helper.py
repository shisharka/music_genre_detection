import numpy as np
from librosa import load, feature
import keras.backend as K

MEL_ARGS = {
    'n_fft': 2048,
    'hop_length': 1024,
    'n_mels': 128
}

default_input_shape = (660, 128)


def audio_to_melspectrogram(file_path, enforce_shape=False):
    """Loads an audio file from file_path, calculates mel-scaled power spectrogram
    (melspectrogram), and returns melspectrogram converted to log scale and song duration"""
    input_track, sample_rate = load(file_path, mono = True)
    features = feature.melspectrogram(input_track, sample_rate, **MEL_ARGS).T

    if enforce_shape:
        # enforcing default input shape for features
        enforced_features = np.zeros(default_input_shape)
        enforced_features[:features.shape[0], :] = features
        features = enforced_features

    features[features == 0] = 10**-6 # because of log scaling

    return np.log(features), input_track.shape[0] * 1.0 / sample_rate


def get_layer_output_function(model, layer_index):
    input = model.layers[0].input
    output = model.layers[layer_index].output
    f = K.function([input, K.learning_phase()], [output])
    return lambda x: f([x, 0]) # learning_phase = 0 means test