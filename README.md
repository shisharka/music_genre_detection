# Music Genre Detection Project

Automatic music genre detection using CRNN (Convolutional Recurrent Neural Networks)

## Usage

### Installing prerequisites

In a fresh virtual environment, run
```shell
conda install --yes --file requirements.txt
```
If you get a `PackageNotFoundError`, add conda-forge channel:
```shell
conda config --add channels conda-forge
```
and run the previous command again.

### Importing data

For training and testing our classifier we use [GTZAN music genre collection](conda config --add channels). 
To download and import the dataset, run
```shell
python import_data.py
```