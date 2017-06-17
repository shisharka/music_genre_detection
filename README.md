# Music Genre Detection Project

Automatic music genre classifier

## Usage

### Installing prerequisites

The project is built on python2.7

#### Conda install

Create and activate a fresh virtual environment:

```shell
conda create -n [yourenvname] python=2.7 anaconda
source activate [yourenvname] 
```

Install required packages:

```shell
conda install -n [yourenvname] --yes --file requirements.txt
```

If you get a `PackageNotFoundError`, add necessary channels:

```shell
conda config --add channels conda-forge
conda config --add channels litl-rnd
```

and run the previous command again.

#### Pip install

In a fresh virtual environment, run

```shell
pip install -r requirements.txt
```

### Dataset

For training and testing our classifier we use [GTZAN music genre collection](http://marsyasweb.appspot.com/download/data_sets/), 
but we are restricted
to a subset which is not including classical and jazz genres, because our classifier
also depends on lyrics, and classical and jazz music representatives are mostly instrumentals.
To download raw data, run

```shell
python download_data.py
```

This will create _data/_ directory in project's root, and download and extract both audio and lyrics datasets
into it's subdirectories: _data/genres/_ and _data/lyrics/_

After that, run 

```shell
python preprocess_data.py
```

to create preprocessed datasets (also stored in _data/_ directory).

### Training

To train CRNN (Convolutional Recurrent Neural Network) classifier, run

```shell
python train_crnn_model.py
```

Model and weights are saved in _models/_ directory.

To train Naive Bayes classifier, run

```shell
python train_lyrics_model.py
```

### App server

This project includes a small python app that demonstrates the CRNN classifier.

If you want to enable downloading audio from YouTube, make sure you have youtube-dl and pafy libraries installed:

```shell
pip install youtube_dl==2017.5.23
pip install pafy==0.5.3.1
``` 

Command to run demo app:

```shell
python server.py
```

Now you can access the demo app from your browser at localhost:8080.

There are some example songs on _/examples_

### Presentation
English: https://docs.google.com/presentation/d/1HUuCpDaassL3Gv5E0909chKlsM4lW4hI-D0pcd43uy8/edit?usp=sharing
Serbian: https://docs.google.com/presentation/d/1T7h60enALTi2MvlT5r0MIeifv8tQiTAlrOHrlZa7wxk/edit?usp=sharing
