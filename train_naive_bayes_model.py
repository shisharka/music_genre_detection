from __future__ import division
import os
import codecs
import sys
from collections import defaultdict
import yaml
from yaml.representer import Representer
yaml.add_representer(defaultdict, Representer.represent_dict)
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from dataset_config import *


def train_model():
    word_frequency = defaultdict(float)
    cond_prob = defaultdict(float)
    sum_of_word_frequency_per_genre = defaultdict(float)
    prior = defaultdict(float)
    
    if not os.path.exists(LYRICS_CONCATENATED_DATA_PATH):
        print('Couldn\'t find preprocessed data, please run preprocess_data.py')
        return

    for file_name in os.listdir(LYRICS_CONCATENATED_DATA_PATH):
        file = codecs.open(os.path.join(LYRICS_CONCATENATED_DATA_PATH, file_name), 'r', 'utf-8')
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

    print('Training finished.')
