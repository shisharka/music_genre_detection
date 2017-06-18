import numpy as np
import os
import cPickle as pickle
import re
import codecs
from dataset_config import *
from helper import audio_to_melspectrogram, default_input_shape

def create_melspectrogram_dataset():
    """Creates dataset pickle file with extracted melspectrogram features
    and genre distribution vectors. Dataset is extracted from audio files located
    in data/genres, and the pickle file path is data/melspectrogram_data.pkl"""
    x = np.zeros((TOTAL_AUDIO_FILES, default_input_shape[0], default_input_shape[1]),
                 dtype=np.float32)
    y = np.zeros((TOTAL_AUDIO_FILES, len(GENRES)), dtype=np.float32)

    for genre_index, genre_name in enumerate(GENRES):
        for i in range(0, AUDIO_FILES_PER_GENRE):
            filename = '{}.000{}.au'.format(genre_name,
                                            str(i).zfill(2))
            path = os.path.join(AUDIO_DATA_PATH, genre_name, filename)
            print('Processing ' + filename)
            file_index = genre_index * AUDIO_FILES_PER_GENRE + i
            x[file_index] = audio_to_melspectrogram(path, enforce_shape=True)[0]
            y[file_index, genre_index] = 1

    with open(MELSPECTROGRAM_DATASET_PATH, 'w') as melspectrogram_dataset:
        pickle.dump({'x': x, 'y': y}, melspectrogram_dataset)


def create_concatenated_lyrics_files():
    """Creates a file for each genre by concatenating lyrics for all songs of the same genre.
    Lyrics are located in data/lyrics, and concatenated lyrics files are located
    in data/lyrics_concatenated."""
    if not os.path.exists(LYRICS_CONCATENATED_DATA_PATH):
        os.mkdir(LYRICS_CONCATENATED_DATA_PATH)

    for dirname, dirnames, filenames in os.walk(LYRICS_DATA_PATH):
        for genre in dirnames:
            genre_file = codecs.open(os.path.join(LYRICS_CONCATENATED_DATA_PATH, genre + ".txt"), 'w', "utf-8")
            for filename in os.listdir(os.path.join(LYRICS_DATA_PATH, genre)):
                f = codecs.open(os.path.join(LYRICS_DATA_PATH, genre, filename), 'r', "utf-8")
                lyrics = re.sub('[\s]+', " ", f.read())
                genre_file.write(lyrics)

if __name__ == '__main__':
    print('Creating mel-scaled spectrogram dataset based on raw audio data...')
    create_melspectrogram_dataset()

    print('Creating concatenated lyrics files...')
    create_concatenated_lyrics_files()
