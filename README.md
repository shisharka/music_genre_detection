# Music Genre Detection Project

Automatic music genre classifier

## Usage

### Installing prerequisites

The project is built on python2.7

#### Conda install

Create a fresh virtual environment:

```shell
conda create -n [yourenvname] python=2.7 anaconda
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

### Importing data

For training and testing our classifier we use [GTZAN music genre collection](http://marsyasweb.appspot.com/download/data_sets/), 
but we are restricted
to a subset which is not including classical and jazz genres, because our classifier
also depends on lyrics, and classical and jazz music representatives are mostly instrumentals.
To download and import the dataset, run

```shell
python import_data.py
```
