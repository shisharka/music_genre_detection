import os
import codecs
import re
from dataset_config import *
from collections import defaultdict
import numpy as np

PATH_TO_LYRICS_CONCATENATED = 'data/lyrics_concatenated'
songs_per_genre = {'blues': 64, 'country': 95, 'disco': 86, 'hiphop': 96, 'metal': 85, 'pop': 99, 'reggae': 80, 'rock': 100}
number_of_songs = TOTAL_LYRICS_FILES

number_of_genres = len(GENRES)
punctuation_regex = re.compile("[;.,\"()?!/]")


def create_concatenated_lyrics_files():
    for dirname, dirnames, filenames in os.walk(LYRICS_DATA_PATH):
        for genre in dirnames:
            genre_file = codecs.open(os.path.join(PATH_TO_LYRICS_CONCATENATED, genre + ".txt"), 'w', "utf-8")
            for filename in os.listdir(os.path.join(LYRICS_DATA_PATH, genre)):
                f = codecs.open(os.path.join(LYRICS_DATA_PATH, genre, filename), 'r', "utf-8")
                lyrics = re.sub('[\s]+', " ", f.read())
                genre_file.write(lyrics)


def generate_model():
    if not os.listdir(PATH_TO_LYRICS_CONCATENATED):
        create_concatenated_lyrics_files()

    word_frequency = defaultdict(set)
    cond_prob = defaultdict(set)
    sum_of_word_frequency_per_genre = defaultdict(dict)
    prior = defaultdict(dict)

    for file_name in os.listdir(PATH_TO_LYRICS_CONCATENATED):
        file = codecs.open(os.path.join(PATH_TO_LYRICS_CONCATENATED, file_name), 'r', 'utf-8')
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
            word_frequency[genre, word] = file_content.count(word)
            sum_of_word_frequency_per_genre[genre] += word_frequency[genre, word]
        for word in words:
            cond_prob[word, genre] = (word_frequency[genre, word] + 1) / (sum_of_word_frequency_per_genre[genre] + 1)

    return cond_prob, prior


# def test():
    # cond_prob, prior = generate_model()
    # test_lyrics_blues = open(os.path.join(LYRICS_DATA_PATH, 'blues', 'blues.00025.txt'), 'r', encoding="utf-8").read()
    # tokens = re.sub(punctuation_regex, "", test_lyrics_blues).lower().split(" ")
    # score = defaultdict(dict)
    # for genre in GENRES:
        # score[genre] = np.log(prior[genre])
        # for word in tokens:
            # if (word, genre) not in cond_prob:
                # continue
            # score[genre] += np.log(cond_prob[word, genre])

    # print(max(score, key=score.get))

# test()
