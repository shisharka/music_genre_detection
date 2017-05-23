from keras.models import Sequential
from keras.optimizers import Adam
from keras.layers import Activation, Conv1D, MaxPool1D, Dropout, \
                         GRU, TimeDistributed, Dense, Lambda
from sklearn.model_selection import train_test_split
import pickle
import os
from keras import backend as K
import matplotlib.pyplot as plt
from dataset_config import GENRES

CONV_LAYERS_COUNT = 3
CONV_ARGS = [{
        'kernel_size': 11,
        'strides': 4,
        'filters': 96,
        'padding': 'same'
    },
    {
        'kernel_size': 5,
        'filters': 256,
        'padding': 'same'
    },
    {
        'kernel_size': 5,
        'filters': 384,
        'padding': 'same'
    },
    {
        'kernel_size': 3,
        'filters': 384,
        'padding': 'same'
    },
    {
        'kernel_size': 3,
        'filters': 256,
        'padding': 'same'
    }
]
GRU_LAYER_SIZE = 256
RANDOM_STATE = 1
MODEL_ARGS = {
    'batch_size': 32,
    'epochs': 100
}


def train_model(data):
    x = data['x']
    y = data['y']
    (x_train_val, x_test, y_train_val, y_test) = \
        train_test_split(x, y, test_size=0.33, random_state=RANDOM_STATE)
    (x_train, x_val, y_train, y_val) = train_test_split(x_train_val,
                                                        y_train_val,
                                                        test_size=0.33,
                                                        random_state=RANDOM_STATE)

    # Building model
    model = Sequential()

    input_shape = (x_train.shape[1], x_train.shape[2])

    model.add(Conv1D(input_shape=input_shape, **CONV_ARGS[1]))
    model.add(Activation('relu'))
    model.add(MaxPool1D(2))
    print(model.output.shape)

    for i in range(1, CONV_LAYERS_COUNT):
        model.add(Conv1D(**CONV_ARGS[1]))
        model.add(Activation('relu'))
        if i < 3:
            model.add(MaxPool1D(2))
        print(model.output.shape)

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
        optimizer=Adam(lr=0.0005),
        metrics=['accuracy']
    )

    # Training
    history = model.fit(x_train, y_train, validation_data=(x_val, y_val), **MODEL_ARGS)

    scores = model.evaluate(x_test, y_test)
    print("Accuracy: %.2f%%" % (scores[1] * 100))

    # summarize history for accuracy
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    # summarize history for loss
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()

    return model


with open('data/melspectrogram_data.pkl', 'r') as f:
    data = pickle.load(f)

model = train_model(data)

if not os.path.exists('models'):
    os.makedirs('models')
with open('models/crnn_model.yaml', 'w') as f:
    f.write(model.to_yaml())
model.save_weights('models/crnn_weights.h5')
