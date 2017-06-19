import sys
import yaml
from get_lyrics import get_lyrics
from train_naive_bayes_model import predict


if __name__ == '__main__':
    print('Loading model...')
    try:
        with open('models/nb_cond_prob.yaml') as f:    
            cond_prob = yaml.load(f)
        with open('models/nb_prior.yaml') as f:    
            prior = yaml.load(f)
    except IOError:
        print('Couldn\'t find model, please run train_naive_bayes_model.py first')
        sys.exit()

    if len(sys.argv) == 2:
        file_path = sys.argv[1]
        print('Loading lyrics...')
        try:
            with open(file_path, 'r') as f:
                lyrics = f.read()
        except:
            print('Bad input file path: ' + file_path)
            sys.exit()

    elif len(sys.argv) == 3:
        artist = sys.argv[1]
        song_title = sys.argv[2]
        print('Downloading lyrics...')
        lyrics = get_lyrics(artist, song_title)

        if not lyrics:
            print('We couldn\'t find the song you specified.')
            sys.exit()

    else:
        print('Please specify path to a lyrics file or artist with song title to download lyrics.')
        sys.exit()

    score = predict(cond_prob, prior, lyrics)

    print('Most probable genre: ' + min(score, key=score.get))
