from __future__ import division
import os
import shutil
import codecs
import sys
from collections import defaultdict
import yaml
from yaml.representer import Representer
yaml.add_representer(defaultdict, Representer.represent_dict)
import numpy as np
from sklearn import model_selection
from sklearn.feature_extraction.text import CountVectorizer
from dataset_config import *

LYRICS_TEST_FILES = defaultdict(int)


def create_concatenated_lyrics_files():
    """Creates a file for each genre by concatenating lyrics for all songs of the same genre.
    Lyrics are located in data/lyrics, and concatenated lyrics files are located
    in data/lyrics_concatenated."""
    if os.path.exists(LYRICS_CONCATENATED_TRAIN_PATH):
        shutil.rmtree(LYRICS_CONCATENATED_TRAIN_PATH)
    os.mkdir(LYRICS_CONCATENATED_TRAIN_PATH)

    for dirname, dirnames, filenames in os.walk(LYRICS_DATA_PATH):
        for genre in dirnames:
            files = []
            for filename in os.listdir(os.path.join(LYRICS_DATA_PATH, genre)):
                files.append(filename)
            train_data, test_data = model_selection.train_test_split(files, test_size=0.1, random_state=3)
            for filename in train_data:
                file_path = os.path.join(LYRICS_CONCATENATED_TRAIN_PATH, genre + ".txt")
                genre_file = codecs.open(file_path, 'a', "utf-8")
                f = codecs.open(os.path.join(LYRICS_DATA_PATH, genre, filename), 'r', "utf-8")
                lyrics = f.read()
                genre_file.write(lyrics)

            LYRICS_TEST_FILES[genre] = test_data


def train_model():
    word_frequency = defaultdict(float)
    cond_prob = defaultdict(float)
    sum_of_word_frequency_per_genre = defaultdict(float)
    prior = defaultdict(float)

    create_concatenated_lyrics_files()

    for file_name in os.listdir(LYRICS_CONCATENATED_TRAIN_PATH):
        file = codecs.open(os.path.join(LYRICS_CONCATENATED_TRAIN_PATH, file_name), 'r', 'utf-8')
        file_content = file.read().lower()
        words = CountVectorizer().build_tokenizer()(file_content)
        genre = file_name.split(".")[0]

        prior[genre] = LYRICS_FILES_PER_GENRE[genre] / TOTAL_LYRICS_FILES
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


def predict(cond_prob, prior, lyrics):
    lyrics = lyrics.lower()
    words = CountVectorizer().build_tokenizer()(lyrics)
    score = defaultdict(float)
    for genre in GENRES:
        score[genre] = np.log(prior[genre])
        for word in words:
            if (word, genre) not in cond_prob:
                continue
            score[genre] += np.log(cond_prob[(word, genre)])

    return score


def get_predictions(cond_prob, prior):
    predicted = []
    true = []
    for genre, files in LYRICS_TEST_FILES.iteritems():
        for file_name in files:
            file = codecs.open(os.path.join(LYRICS_DATA_PATH, genre, file_name), 'r', 'utf-8')
            file_content = file.read()
            score = predict(cond_prob, prior, file_content)
            predicted.append(min(score, key=score.get))
            true.append(genre)
            file.close()

    return predicted, true


def calculate_accuracy(cond_prob, prior):
    predicted, true = get_predictions(cond_prob, prior)
    correct = 0
    for (index, item) in enumerate(predicted):
        if item == true[index]:
            correct += 1
    return correct * 100.0 / len(predicted)


def calculate_accuracy_per_genre(cond_prob, prior):
    accuracy_map = defaultdict()
    print("Accuracy by genre: ")
    for key in LYRICS_TEST_FILES:
        files = LYRICS_TEST_FILES[key]
        genre = files[0].split(".")[0]
        accuracy_map[genre] = 0
        for filename in files:
            f = codecs.open(os.path.join(LYRICS_DATA_PATH, genre, filename), 'r', "utf-8")
            lyrics = f.read()
            score = predict(cond_prob, prior, lyrics)
            if min(score, key=score.get) == genre:
                accuracy_map[genre] += 1

        print(genre + ': ' + str(accuracy_map[genre] * 100.0 / len(files)) + '%')

if __name__ == '__main__':
    print('Training...')
    model = train_model()
    if not model:
        sys.exit()

    cond_prob, prior = model

    if not os.path.exists('models'):
        os.makedirs('models')
    with open('models/nb_cond_prob.yaml', 'w') as f:
        f.write(yaml.dump(cond_prob))
    with open('models/nb_prior.yaml', 'w') as f:
        f.write(yaml.dump(prior))

    accuracy = calculate_accuracy(cond_prob, prior)
    print("Accuracy: %.2f%%" % accuracy)
    calculate_accuracy_per_genre(cond_prob, prior)
