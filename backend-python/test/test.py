import json
import unittest
from unittest import mock

from flask_api import status
import requests

from app import app
import movies.es

MOVIE_SEARCH_MOCK_RESPONSE = [
    {
        "genres": ["Adventure", "Animation", "Children", "Comedy", "Fantasy"],
        "id": 1,
        "tags": ["pixar", "fun"],
        "title": "Toy Story (1995)",
    },
    {
        "genres": ["Adventure", "Children", "Fantasy"],
        "id": 2,
        "tags": ["fantasy", "magic board game", "Robin Williams", "game"],
        "title": "Jumanji (1995)",
    },
    {
        "genres": ["Comedy", "Romance"],
        "id": 3,
        "tags": ["moldy", "old"],
        "title": "Grumpier Old Men (1995)",
    },
    {
        "genres": ["Comedy", "Drama", "Romance"],
        "id": 4,
        "tags": [],
        "title": "Waiting to Exhale (1995)",
    },
]


class TestCase(unittest.TestCase):
    @mock.patch("movies.es.search")
    def test_route(self, movie_search_mock):
        movie_search_mock.return_value = (
            MOVIE_SEARCH_MOCK_RESPONSE,
            len(MOVIE_SEARCH_MOCK_RESPONSE),
        )
        c = app.test_client()

        page = 1
        page_size = 4
        response = c.get(f"/movies?page={page}&page_size={page_size}")
        data = response.json

        self.assertEqual(response.status_code, 200)
        # Our mock should be preserved
        self.assertEqual(len(data["data"]), data["pagination"]["row_count"])
        # Page and page size params should be preserved
        self.assertEqual(data["pagination"]["page"], page)
        self.assertEqual(data["pagination"]["page_size"], page_size)

        # Empty query params should be okay
        response = c.get(f"/movies?q=&genres=&tags=&page=&page_size=")
        self.assertEqual(response.status_code, 200)

    @mock.patch("movies.es.search")
    def test_route_bad_input(self, movie_search_mock):
        movie_search_mock.return_value = (
            MOVIE_SEARCH_MOCK_RESPONSE,
            len(MOVIE_SEARCH_MOCK_RESPONSE),
        )
        c = app.test_client()

        # page and page_size must be postive integers
        bad_pages = [-1, 0, "a string"]
        for page in bad_pages:
            page_size = 4
            response = c.get(f"/movies?page={page}&page_size={page_size}")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        bad_page_sizes = [-1, 0, "a string"]
        for page_size in bad_page_sizes:
            page = 1
            response = c.get(f"/movies?page={page}&page_size={page_size}")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_parse_response(self):
        es_response_json = """
        {
            "_shards":{
                "failed":0,
                "skipped":0,
                "successful":2,
                "total":2
            },
            "hits":{
                "hits":[
                    {
                        "_id":"588",
                        "_index":"search",
                        "_score":6.9985013,
                        "_source":{
                            "genres":["Adventure","Animation","Children","Comedy","Musical"],
                            "tags":["Disney"],
                            "title":"Aladdin (1992)"
                        },
                        "_type":"_doc"
                    }
                ],
                "max_score":6.9985013,
                "total":{
                    "relation":"eq",
                    "value":22
                }
            },
            "timed_out":false,
            "took":9
        }
        """
        expected_parsed_rows = [
            {
                "genres": ["Adventure", "Animation", "Children", "Comedy", "Musical"],
                "tags": ["Disney"],
                "title": "Aladdin (1992)",
                "id": 588,
            }
        ]
        expected_parsed_row_count = 22
        parsed_rows, parsed_row_count = movies.es._parse_response(
            json.loads(es_response_json)
        )

        self.assertEqual(parsed_rows, expected_parsed_rows)
        self.assertEqual(parsed_row_count, expected_parsed_row_count)

    def test_build_query(self):
        q = "abc"
        genres = ["One", "Two"]
        tags = ["Three", "Four", "Five"]
        expected_query_json = """
        {
            "query": {
                "bool": {
                    "must": [
                        {
                            "match": {
                                "title": "abc"
                            }
                        },
                        {
                            "bool": {
                                "must": [
                                    {"term": {"genres": "One"}},
                                    {"term": {"genres": "Two"}},
                                    {"term": {"tags": "Three"}},
                                    {"term": {"tags": "Four"}},
                                    {"term": {"tags": "Five"}}
                                ]
                            }
                        }
                    ]
                }
            }
        }
        """
        query = movies.es._build_query(q, genres, tags)

        self.assertEqual(query, json.loads(expected_query_json))
