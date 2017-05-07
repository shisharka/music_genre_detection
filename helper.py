import numpy as np
from librosa import load, feature
import os
import pickle

GENRES = ['blues', 'classical', 'country', 'disco', 'hiphop', 'jazz', 'metal',
          'pop', 'reggae', 'rock']
AUDIO_DATA_PATH = 'data/genres'
TOTAL_FILES = 1000
FILES_PER_GENRE = 100
DATASET_PATH = 'data/data.pkl'


def extract_features(file_path):
    """Loads an audio file from file_path, calculates mel spectrogram,
    and returns log from mel spectrogram values and song duration"""
    input_track, sample_rate = load(file_path, mono = True)
    features = feature.melspectrogram(input_track, sample_rate, hop_length=1024)

    return np.log(features), input_track.shape[0] * 1.0 / sample_rate


def default_input_shape(axis=None):
    """Returns default shape of log mel spectrogram feature matrix"""
    path = os.path.join(AUDIO_DATA_PATH, 'blues/blues.00000.au')
    temp_input, _ = extract_features(path)

    return temp_input.shape if axis is None else temp_input.shape[axis]


def enforce_default_shape(features):
    """Enforcing default_input_shape as shape for argument matrix features"""
    enforced_features = np.zeros(default_input_shape())

    if default_input_shape(1) <= features.shape[1]:
        enforced_features = features[:, :default_input_shape(1)]
    else:
        enforced_features[:, :features.shape[1]] = features

    return enforced_features


def create_dataset():
    """Creates dataset pickle file with extracted log mel spectrogram features
    and genre vectors. Dataset is extracted from audio files located
    in data/genres, and the pickle file path is data/data.pkl"""
    x = np.zeros((TOTAL_FILES, default_input_shape(0), default_input_shape(1)),
                 dtype=np.float32)
    y = np.zeros((TOTAL_FILES, len(GENRES)), dtype=np.float32)

    for genre_index, genre_name in enumerate(GENRES):
        for i in range(0, FILES_PER_GENRE):
            filename = '{}.000{}.au'.format(genre_name,
                                            str(i).zfill(2))
            path = os.path.join(AUDIO_DATA_PATH, genre_name, filename)
            print 'Processing', filename
            file_index = genre_index * FILES_PER_GENRE + i
            x[file_index] = enforce_default_shape(extract_features(path)[0])
            y[file_index, genre_index] = 1

    pickle.dump({'x': x, 'y': y}, open(DATASET_PATH, 'w'))
