def _build_query(q, genres, tags):
    query = {}
    query["query"] = {}
    query["query"]["bool"] = {}
    query["query"]["bool"]["must"] = [{}]
    if q:
        query["query"]["bool"]["must"][0]["match"] = {"title": q}
    else:
        query["query"]["bool"]["must"][0]["match_all"] = {}

    query["query"]["bool"]["must"].append({})
    query["query"]["bool"]["must"][1] = {}
    query["query"]["bool"]["must"][1]["bool"] = {}
    query["query"]["bool"]["must"][1]["bool"]["must"] = []

    for genre in genres:
        filter_term = {}
        filter_term["term"] = {"genres": genre}
        query["query"]["bool"]["must"][1]["bool"]["must"].append(filter_term)

    for tag in tags:
        filter_term = {}
        filter_term["term"] = {"tags": tag}
        query["query"]["bool"]["must"][1]["bool"]["must"].append(filter_term)

    return query


def _parse_response(reponse):
    row_count = reponse["hits"]["total"]["value"]
    hits = reponse["hits"]["hits"]
    # Add the doc id to the record
    rows = [dict(h["_source"], **{"id": int(h["_id"])}) for h in hits]

    return rows, row_count


def search(es, index, q, genres, tags, page, page_size):
    limit = page_size
    offset = (page - 1) * page_size  # First page is 1

    body = _build_query(q, genres, tags)
    params = {
        "from": offset,
        "size": limit,
    }
    response = es.search(body=body, index=index, params=params)
    result = _parse_response(response)

    return result
