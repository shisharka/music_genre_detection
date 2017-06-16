from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Activation, Conv1D, MaxPool1D, Dropout, \
                         GRU, TimeDistributed, Dense, Lambda
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import numpy as np
import pickle
import os
from keras import backend as K
import matplotlib.pyplot as plt
import random as rn
import tensorflow as tf
from dataset_config import GENRES

# This is needed to make reproducible training model,
# see https://github.com/fchollet/keras/issues/2280#issuecomment-306959926
# Setting PYTHONHASHSEED for determinism was not listed anywhere for TensorFlow,
# but apparently it is necessary for the Theano backend
# (https://github.com/fchollet/keras/issues/850).
os.environ['PYTHONHASHSEED'] = '0'
np.random.seed(7)
rn.seed(7)
# Limit operation to 1 thread for deterministic results.
session_conf = tf.ConfigProto(
    intra_op_parallelism_threads=1,
    inter_op_parallelism_threads=1
)
tf.set_random_seed(7)
sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
K.set_session(sess)

CONV_LAYERS_COUNT = 3
CONV_ARGS = [{
        'kernel_size': 8,
        'strides': 2,
        'filters': 96,
        'padding': 'same'
    },
    {
        'kernel_size': 6,
        'filters': 256,
        'padding': 'same'
    },
    {
        'kernel_size': 6,
        'filters': 256,
        'padding': 'same'
    }
]
GRU_LAYER_SIZE = 256
RANDOM_STATE = 3
MODEL_ARGS = {
    'batch_size': 16,
    'epochs': 100
}


def vectors_to_labels(y):
    result = np.array([])
    for l in y:
        i = np.argmax(l)
        result = np.append(result, GENRES[i])
    return result


def train_model(data):
    x = data['x']
    y = data['y']
    (x_train_val, x_test, y_train_val, y_test) = \
        train_test_split(x, y, test_size=0.1, random_state=RANDOM_STATE)
    (x_train, x_val, y_train, y_val) = train_test_split(x_train_val,
                                                        y_train_val,
                                                        test_size=0.111,
                                                        random_state=RANDOM_STATE)

    # Building model
    model = Sequential()

    input_shape = (None, x_train.shape[2])

    model.add(Conv1D(input_shape=input_shape, **CONV_ARGS[0]))
    model.add(Activation('elu'))
    model.add(MaxPool1D(4))

    for i in range(1, CONV_LAYERS_COUNT):
        model.add(Conv1D(**CONV_ARGS[i]))
        model.add(Activation('elu'))
        model.add(MaxPool1D(2))

    model.add(Dropout(0.5))
    model.add(GRU(GRU_LAYER_SIZE, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(TimeDistributed(Dense(len(GENRES))))
    model.add(Activation('softmax', name='realtime_output'))

    model.add(Lambda(
        function=lambda x: K.mean(x, axis=1),
        name='merged_output'
    ))

    model.compile(
        loss='categorical_crossentropy',
        optimizer=Adam(lr=2e-4),
        metrics=['accuracy']
    )

    # Training
    history = model.fit(x_train, y_train, validation_data=(x_val, y_val), **MODEL_ARGS)

    # summarize history for accuracy
    axes = plt.gca()
    axes.set_xlim([0, MODEL_ARGS['epochs']])
    axes.set_ylim([0, 1])
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    axes = plt.gca()
    axes.set_xlim([0, MODEL_ARGS['epochs']])
    axes.set_ylim([0, 3])
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    scores = model.evaluate(x_test, y_test)
    print("Accuracy: %.2f%%" % (scores[1] * 100))

    y_true = vectors_to_labels(y_test)
    y = model.predict(x_test)
    y_predicted = vectors_to_labels(y)
    conf_matrix = confusion_matrix(y_true, y_predicted, labels=GENRES)
    print('Confusion matrix:')
    print(conf_matrix)

    return model

if __name__ == '__main__':
    with open('data/melspectrogram_data.pkl', 'r') as f:
        data = pickle.load(f)

    model = train_model(data)

    if not os.path.exists('models'):
        os.makedirs('models')
    with open('models/crnn_model.yaml', 'w') as f:
        f.write(model.to_yaml())
    model.save_weights('models/crnn_weights.h5')
