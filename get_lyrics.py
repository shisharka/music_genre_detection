import re
from urllib import urlopen
from bs4 import BeautifulSoup
import json
import codecs
import sys


def azlyrics_url(artist, song_title):
    # replace '&' with 'And' in artist and song_title
    artist = artist.replace('&', 'And')
    song_title = song_title.replace('&', 'And')
    # remove all except alphanumeric characters from artist and song_title
    artist = re.sub('[^A-Za-z0-9]+', '', artist)
    song_title = re.sub('[^A-Za-z0-9]+', '', song_title)
    # convert to lowercase
    artist = artist.lower()
    song_title = song_title.lower()
    if artist.startswith('the'):  # remove starting 'the' from artist e.g. the who -> who
        artist = artist[3:]

    return 'http://azlyrics.com/lyrics/' + artist + '/' + song_title + '.html'


def metrolyrics_url(artist, song_title):
    # remove all except alphanumeric characters and spaces from artist and song_title
    artist = re.sub('[^A-Za-z0-9\s]+', '', artist)
    song_title = re.sub('[^A-Za-z0-9\s]+', '', song_title)
    # replaces spaces with dashes and convert to lowercase
    artist = re.sub('\s+', '-', artist).lower()
    song_title = re.sub('\s+', '-', song_title).lower()

    return 'http://www.metrolyrics.com/' + song_title + '-lyrics-' + artist + '.html'


def oldielyrics_url(artist, song_title):
    # remove all except alphanumeric characters and spaces from artist and song_title
    artist = re.sub('[^A-Za-z0-9\s]+', '', artist)
    song_title = re.sub('[^A-Za-z0-9\s]+', '', song_title)
    # replaces spaces with underscores and convert to lowercase
    artist = re.sub('\s+', '_', artist).lower()
    song_title = re.sub('\s+', '_', song_title).lower()

    return 'http://www.oldielyrics.com/lyrics/' + artist + '/' + song_title + '.html'


def parse_lyrics(url, selector='div', selector_class=None, selector_id=None):
    try:
        content = urlopen(url).read()
        soup = BeautifulSoup(content, 'html.parser')
        lyrics_tags = soup.find_all(selector,
                                    attrs={'class': selector_class,
                                           'id': selector_id})
        lyrics = [re.sub('<[a-z]*?>', '', tag.getText()) for tag in lyrics_tags]

        return "\n".join(lyrics).strip()
    except Exception as e:
        print('Exception occurred: ' + str(e))

        return None


def get_lyrics(artist, song_title):
    azlyrics    = parse_lyrics(azlyrics_url(artist, song_title))
    metrolyrics = parse_lyrics(metrolyrics_url(artist, song_title),
                               selector='p',
                               selector_class='verse')
    oldielyrics = parse_lyrics(oldielyrics_url(artist, song_title),
                               selector_class='lyrics')

    return azlyrics or metrolyrics or oldielyrics

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please specify artist and song title')
    else:
        artist = sys.argv[1]
        song_title = sys.argv[2]
        lyrics = get_lyrics(artist, song_title)
        print(lyrics)
