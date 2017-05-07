from urllib import urlretrieve
from progressbar import ProgressBar, Percentage, Bar
import tarfile
import os
import shutil
from helper import create_dataset

if os.path.exists('data'):
    shutil.rmtree('data')
os.makedirs('data')

progress_bar = ProgressBar(widgets=[Bar('=', '[', ']'), ' ', Percentage()], maxval=100)
url = 'http://opihi.cs.uvic.ca/sound/genres.tar.gz'
filename = 'data/genres.tar.gz'


def progress(count, block_size, total_size):
    percentage = int(count * block_size * 100 / total_size)
    if percentage > progress_bar.currval:
        progress_bar.update(percentage)


print 'Downloading audio files from {}...'.format(url)
progress_bar.start()
urlretrieve(url, filename, reporthook=progress)
progress_bar.finish()

print 'Extracting files from {}...'.format(filename)
tar = tarfile.open(filename)
tar.extractall('data/genres')

print 'Removing {}...'.format(filename)
os.remove(filename)

print 'Creating dataset pickle...'
create_dataset()
