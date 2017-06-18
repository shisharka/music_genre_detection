import matplotlib.pyplot as plt
import sys
import librosa.display
from helper import audio_to_melspectrogram

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please specify path to an audio file')
    else:
        file_path = sys.argv[1]
        try:
            data = audio_to_melspectrogram(file_path)[0].T
            plt.figure(figsize=(10, 4))
            librosa.display.specshow(data, y_axis='mel', x_axis='time')
            plt.colorbar(format='%+2.0f dB')
            plt.title('Mel spectrogram')
            plt.tight_layout()
            plt.show()
        except:
            print('Bad input file path: ' + file_path)
