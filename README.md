# Music Genre Detection Project

Automatic music genre classifier

## Usage

### Installing prerequisites

In a fresh virtual environment, run

```shell
pip install -r requirements.txt
```

### Importing data

For training and testing our classifier we use [GTZAN music genre collection]
(http://marsyasweb.appspot.com/download/data_sets/), but we are restricted
to a subset which is not including classical and jazz genres, because our classifier
also depends on lyrics, and classical and jazz music representatives are mostly instrumentals.
To download and import the dataset, run

```shell
python import_data.py
```
