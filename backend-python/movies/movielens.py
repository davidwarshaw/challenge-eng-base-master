import os
from elasticsearch import helpers
import io
import json
import ssl
import pandas as pd
from urllib.request import urlopen
from zipfile import ZipFile

DATASETS = [
    "links",
    "ratings",
    "movies",
    "tags",
]
METADATA = {
    "url": "https://files.grouplens.org/datasets/movielens/ml-latest-small.zip",
    "dir": "ml-latest-small",
    "files": [f"{ds}.csv" for ds in DATASETS],
}
TMP_DIR = f"/tmp/{METADATA['dir']}"

ES_MAPPING = {"properties": {}}
# We want to run match queries against the movie title
ES_MAPPING["properties"]["title"] = {"type": "text"}
# We only want to run term queries against genres and tags
ES_MAPPING["properties"]["tags"] = {"type": "keyword"}
ES_MAPPING["properties"]["genres"] = {"type": "keyword"}


def _paths():
    return [os.path.join(TMP_DIR, file) for file in METADATA["files"]]


def datasets_and_paths():
    return zip(DATASETS, _paths())


def is_already_downloaded():
    return all([os.path.isfile(path) for path in _paths()])


def download_and_unzip():
    # The movieliens file server is missing an intermediate cert, so we won't check it
    context = ssl.create_default_context()
    context.check_hostname = False
    context.verify_mode = ssl.CERT_NONE

    with urlopen(METADATA["url"], context=context) as response:
        with ZipFile(io.BytesIO(response.read())) as archive:
            archive.extractall("/tmp")


def _record_generator(df, index):
    for record in df.to_dict(orient="records"):
        record["_index"] = index
        record["_op_type"] = "index"
        yield record


def _load_index(es, df, index):
    # First delete the index (if it doesn't exist, mission accomplished)
    es.indices.delete(index=index, ignore=[404])

    # Create the index and load the dataset
    body = {"mappings": ES_MAPPING}
    es.indices.create(index=index, body=body)
    helpers.bulk(es, _record_generator(df, index))


def load_to_es(es, echo):
    echo("Loading dataset CSVs")
    dfs = {}
    for dataset, path in datasets_and_paths():
        dfs[dataset] = pd.read_csv(path)

    echo("Transforming datasets")
    tags = (
        dfs["tags"][["movieId", "tag"]]
        .drop_duplicates()
        .groupby("movieId")["tag"]
        .apply(list)
    ).rename("tags")

    movies = dfs["movies"].set_index("movieId")
    genres = movies["genres"].str.split("|")

    search = (
        movies[["title"]]
        .join(genres, how="left")
        .join(tags, how="left")
        .rename_axis("_id")
        .reset_index()
    )
    search["genres"] = search["genres"].fillna("").apply(list)
    search["tags"] = search["tags"].fillna("").apply(list)

    echo(f"Recreating es index: movies")
    _load_index(es, search, "movies")
