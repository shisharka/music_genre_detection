from __future__ import division
import os
import codecs
import re
import sys
from dataset_config import *
from get_lyrics import get_lyrics
from collections import defaultdict
import numpy as np
from sklearn import model_selection

songs_per_genre = {'blues': 64, 'country': 95, 'disco': 86, 'hiphop': 96, 'metal': 85, 'pop': 99, 'reggae': 80, 'rock': 100}
number_of_songs = TOTAL_LYRICS_FILES
punctuation_regex = re.compile("[;.,\"()?!/]")
word_frequency = defaultdict(float)
cond_prob = defaultdict(float)
sum_of_word_frequency_per_genre = defaultdict(float)


def train_model():
    if not os.path.exists(LYRICS_CONCATENATED_DATA_PATH):
        print('There are no files needed to train model.')
        return

    prior = defaultdict(float)
    for file_name in os.listdir(LYRICS_CONCATENATED_DATA_PATH):
        file = codecs.open(os.path.join(LYRICS_CONCATENATED_DATA_PATH, file_name), 'r', 'utf-8')
        file_content = file.read().lower()
        file_content = re.sub(punctuation_regex, "", file_content)
        words = re.split('\s+', file_content)
        genre = file_name.split(".")[0]
        prior[genre] = songs_per_genre[genre] / number_of_songs
        sum_of_word_frequency_per_genre[genre] = 0
        # for every element in words list calculate frequency in genre
        for word in words:
            if (genre, word) in word_frequency:
                continue
            word_frequency[(genre, word)] = file_content.count(word)
            sum_of_word_frequency_per_genre[genre] += word_frequency[(genre, word)] + 1
        for word in words:
            cond_prob[(word, genre)] = (word_frequency[(genre, word)] + 1) / sum_of_word_frequency_per_genre[genre]

        file.close()

    return cond_prob, prior


def create_concatenated_lyrics_by_genre_test(train_data):
    """Creates a file for given train data set and returns concatenated lyrics string"""
    genre = train_data[0].split(".")[0]
    genre_concatenated = ""
    for filename in train_data:
        f = codecs.open(os.path.join(LYRICS_DATA_PATH, genre, filename), 'r', "utf-8")
        lyrics = re.sub('[\s]+', " ", f.read())
        genre_concatenated += lyrics
        f.close()

    return genre_concatenated


def train_model_test(test_size):
    if not os.path.exists(LYRICS_CONCATENATED_DATA_TEST_PATH):
        print('There are no files needed to train test model.')
        return

    prior = defaultdict(float)
    for file_name in os.listdir(LYRICS_CONCATENATED_DATA_TEST_PATH):
        file = codecs.open(os.path.join(LYRICS_CONCATENATED_DATA_TEST_PATH, file_name), 'r', 'utf-8')
        file_content = file.read().lower()
        file_content = re.sub(punctuation_regex, "", file_content)
        words = re.split('\s+', file_content)
        genre = file_name.split(".")[0]
        prior[genre] = songs_per_genre[genre] / (number_of_songs*(1 - test_size))
        sum_of_word_frequency_per_genre[genre] = 0
        # for every element in words list calculate frequency in genre
        for word in words:
            if (genre, word) in word_frequency:
                continue
            word_frequency[(genre, word)] = file_content.count(word)
            sum_of_word_frequency_per_genre[genre] += word_frequency[(genre, word)] + 1
        for word in words:
            cond_prob[(word, genre)] = (word_frequency[(genre, word)] + 1) / sum_of_word_frequency_per_genre[genre]

        file.close()

    return cond_prob, prior


def calculate_accuracy():
    test_size = 0.1
    if not os.path.exists(LYRICS_CONCATENATED_DATA_TEST_PATH):
        os.mkdir(LYRICS_CONCATENATED_DATA_TEST_PATH)

    test_data_map = defaultdict()
    for dirname, dirnames, filenames in os.walk(LYRICS_DATA_PATH):
        for genre in dirnames:
            files = []
            for filename in os.listdir(os.path.join(LYRICS_DATA_PATH, genre)):
                files.append(filename)
            train_data, test_data = model_selection.train_test_split(files, test_size = test_size)

            genre_concatenated = create_concatenated_lyrics_by_genre_test(train_data)
            genre_file = codecs.open(os.path.join(LYRICS_CONCATENATED_DATA_TEST_PATH, genre + ".txt"), 'w', "utf-8")
            genre_file.write(genre_concatenated)
            test_data_map[genre] = test_data
            genre_file.close()

    model = train_model_test(test_size)
    if len(model) == 0:
        print("No model for testing data.")
        return

    cond_prob, prior = model
    accuracy_map = defaultdict()

    #test model on test data set
    for key in test_data_map:
        files = test_data_map[key]
        genre = files[0].split(".")[0]
        accuracy_map[genre] = 0
        for filename in files:
            f = codecs.open(os.path.join(LYRICS_DATA_PATH, genre, filename), 'r', "utf-8")
            lyrics = re.sub('[\s]+', " ", f.read())
            f.close()
            words = re.split('\s+', lyrics)
            score = defaultdict(float)
            for genre_iter in GENRES:
                score[genre_iter] = np.log(prior[genre_iter])
                for word in words:
                    if (word, genre_iter) not in cond_prob:
                        continue
                    score[genre_iter] += np.log(cond_prob[(word, genre_iter)])

            if min(score, key=score.get) == genre:
                accuracy_map[genre] += 1

        print(genre, accuracy_map[genre], len(test_data))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        try:
            with open(file_path, 'r') as f:
                lyrics = f.read()
        except:
            print('Bad input file path: ' + file_path)
            sys.exit()

    elif len(sys.argv) == 3:
        artist = sys.argv[1]
        song_title = sys.argv[2]
        lyrics = get_lyrics(artist, song_title)

        if len(lyrics) == 0:
            print('We couldn\'t find song you specified.')
            sys.exit()

    else:
        print('Please specify path to a lyrics file or artist with song title to download lyrics.')
        sys.exit()

    model = train_model()
    if len(model) == 0:
        sys.exit()

    cond_prob, prior = model
    lyrics = re.sub(punctuation_regex, "", lyrics).lower()
    words = re.split('\s+', lyrics)
    score = defaultdict(float)
    for genre in GENRES:
        score[genre] = np.log(prior[genre])
        for word in words:
            if (word, genre) not in cond_prob:
                continue
            score[genre] += np.log(cond_prob[(word, genre)])

    print('Most probable genre: ' + min(score, key=score.get))
