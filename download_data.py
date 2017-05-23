from urllib import urlretrieve
from progressbar import ProgressBar, Percentage, Bar
import tarfile
import os
import shutil
from dataset_config import AUDIO_DATA_PATH, LYRICS_DATA_PATH

if not os.path.exists('data')
    os.makedirs('data')

if os.path.exists(AUDIO_DATA_PATH):
    shutil.rmtree(AUDIO_DATA_PATH)

if os.path.exists(LYRICS_DATA_PATH):
    shutil.rmtree(LYRICS_DATA_PATH)

progress_bar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Percentage()], maxval=100)
audio_url = 'http://opihi.cs.uvic.ca/sound/genres.tar.gz'
audio_filename = 'data/genres.tar.gz'
lyrics_url = 'http://s000.tinyupload.com/download.php?file_id=28717764016959597486&t=2871776401695959748620334'
lyrics_filename = 'data/lyrics.tar.gz'


def progress(count, block_size, total_size):
    percentage = int(count * block_size * 100 / total_size)
    if percentage > progress_bar.currval:
        progress_bar.update(percentage)


def download(url, filename):
    print 'Downloading audio files from {}...'.format(url)
    progress_bar.start()
    urlretrieve(url, filename, reporthook=progress)
    progress_bar.finish()


def extract(compressed_filename, destination_path):
    print 'Extracting files from {}...'.format(compressed_filename)
    tar = tarfile.open(compressed_filename)
    tar.extractall(destination_path)
    print 'Removing {}...'.format(compressed_filename)
    os.remove(compressed_filename)


download(audio_url, audio_filename)

extract(audio_filename, AUDIO_DATA_PATH)

download(lyrics_url, lyrics_filename)

extract(lyrics_filename, LYRICS_DATA_PATH)