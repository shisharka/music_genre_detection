# Global variables describing our dataset
GENRES = ['blues', 'country', 'disco', 'hiphop', 'metal', 'pop', 'reggae', 'rock']

AUDIO_DATA_PATH = 'data/genres'
TOTAL_AUDIO_FILES = 800
AUDIO_FILES_PER_GENRE = 100
MELSPECTROGRAM_DATASET_PATH = 'data/melspectrogram_data.pkl'

LYRICS_DATA_PATH = 'data/lyrics'
TOTAL_LYRICS_FILES = 705
LYRICS_FILES_PER_GENRE = {'blues': 64,
                          'country': 95,
                          'disco': 86,
                          'hiphop': 96,
                          'metal': 85,
                          'pop': 99,
                          'reggae': 80,
                          'rock': 100}

LYRICS_CONCATENATED_DATA_PATH = 'data/lyrics_concatenated'
LYRICS_CONCATENATED_DATA_TEST_PATH = 'data/lyrics_concatenated_test'
