import click
import csv
from flask import Flask, jsonify, request
from flask_api import status
from elasticsearch import Elasticsearch, helpers


import movies.es
import movies.movielens

app = Flask(__name__)
es = Elasticsearch(["es:9200"])


def make_paginated_response(data, page, page_size, row_count):
    return {
        "data": data,
        "pagination": {
            "page": page,
            "page_size": page_size,
            "row_count": row_count,
        },
    }


@app.route("/movies")
def test():
    q = request.args.get("q") or ""
    genres = request.args.get("genres") or None
    tags = request.args.get("tags") or None
    page = request.args.get("page") or 1
    page_size = request.args.get("page_size") or 20

    # Split the embedded arrays
    genre_list = genres.split(",") if genres else []
    tag_list = tags.split(",") if tags else []

    # Validate input
    try:
        page = int(page)
        assert page > 0
        page_size = int(page_size)
        assert page_size > 0
    except:
        return (
            "page and page_size must be positive integers",
            status.HTTP_400_BAD_REQUEST,
        )

    data, row_count = movies.es.search(
        es, "movies", q, genre_list, tag_list, page, page_size
    )
    response = make_paginated_response(data, page, page_size, row_count)
    return jsonify(response)


@app.cli.command("load-movielens")
def load_movielens():

    if not movies.movielens.is_already_downloaded():
        click.echo(f"Downloading datasets")
        movies.movielens.download_and_unzip()
    else:
        click.echo(f"Loading previously downloaded datasets")

    movies.movielens.load_to_es(es, click.echo)

    click.echo(f"Loading complete")
