import numpy as np
from librosa import load, feature
import os
import cPickle as pickle
from dataset_config import *

default_input_shape = (660, 128)


def extract_features(file_path):
    """Loads an audio file from file_path, calculates mel-scaled power spectrogram
    (melspectrogram), and returns melspectrogram converted to log scale and song duration"""
    input_track, sample_rate = load(file_path, mono = True)
    features = feature.melspectrogram(input_track, sample_rate, hop_length=1024).T
    print features.shape

    return np.log(features), input_track.shape[0] * 1.0 / sample_rate


def enforce_default_shape(features):
    """Enforcing default_input_shape as shape for argument matrix features"""
    enforced_features = np.zeros(default_input_shape)
    enforced_features[:features.shape[0], :] = features

    return enforced_features


def create_melspectrogram_dataset():
    """Creates dataset pickle file with extracted log melspectrogram features
    and genre vectors. Dataset is extracted from audio files located
    in data/genres, and the pickle file path is data/melspectrogram_data.pkl"""
    x = np.zeros((TOTAL_AUDIO_FILES, default_input_shape[0], default_input_shape[1]),
                 dtype=np.float32)
    y = np.zeros((TOTAL_AUDIO_FILES, len(GENRES)), dtype=np.float32)

    for genre_index, genre_name in enumerate(GENRES):
        for i in range(0, AUDIO_FILES_PER_GENRE):
            filename = '{}.000{}.au'.format(genre_name,
                                            str(i).zfill(2))
            path = os.path.join(AUDIO_DATA_PATH, genre_name, filename)
            print 'Processing', filename
            file_index = genre_index * AUDIO_FILES_PER_GENRE + i
            x[file_index] = enforce_default_shape(extract_features(path)[0])
            y[file_index, genre_index] = 1

    with open(MELSPECTROGRAM_DATASET_PATH, 'w') as melspectrogram_dataset:
        pickle.dump({'x': x, 'y': y}, melspectrogram_dataset)
