from helper import audio_to_melspectrogram, get_layer_output_function
import numpy as np
from keras.models import model_from_yaml


class GenreDetector():
    def __init__(self, model_path, weights_path):
        with open(model_path, 'r') as f:
            model = model_from_yaml(f.read())
        model.load_weights(weights_path)
        self.pred_fun_realtime = get_layer_output_function(model, -2)
        self.pred_fun_merged = get_layer_output_function(model, -1)
        print('Loaded model.')

    def detect_realtime(self, track_path):
        print('Loading song', track_path)
        (features, duration) = audio_to_melspectrogram(track_path)
        self.features = np.reshape(features, (1, ) + features.shape)
        return self.pred_fun_realtime(self.features)[0], duration

    def detect_merged(self):
        return self.pred_fun_merged(self.features)[0]
