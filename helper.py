import numpy as np
from librosa import load, feature
import keras.backend as K
from dataset_config import GENRES

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

def get_genre_distribution_over_time(predictions, duration, merged_predictions):
    '''
    Turns the matrix of predictions given by a model into a dict mapping
    time in the song to a music genre distribution.
    '''
    predictions = np.reshape(predictions, predictions.shape[1:])
    n_steps = predictions.shape[0]
    delta_t = duration / n_steps

    def get_genre_distribution(step):
        return {genre_name: float(predictions[step, genre_index])
                for (genre_index, genre_name) in enumerate(GENRES)}

    def get_merged_genre():
        return {genre_name: float(merged_predictions[0, genre_index])
                for (genre_index, genre_name) in enumerate(GENRES)}

    return [((step + 1) * delta_t, get_genre_distribution(step))
            for step in xrange(n_steps - 2)] + [((n_steps - 1) * delta_t, get_merged_genre())]
