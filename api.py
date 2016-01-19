from flask import Flask, request, Response
import os
import json

from preprocess import preprocess
from helpers import return_md_as_html, fetch_listings, paginate_listings, property_to_json


def create_app():
    preprocess(mysql_url=os.environ['CLEARDB_DATABASE_URL'])
    app = Flask(__name__)

    return app

app = create_app()


@app.route('/')
def index():
    return return_md_as_html(filename='PROBLEM.md', title='Opendoor Engineering Problem')


@app.route('/listings')
def listings():
    listings = fetch_listings(mysql_url=os.environ['CLEARDB_DATABASE_URL'], params=request.args)
    listings, link_header = paginate_listings(
        listings=listings,
        params=request.args,
        api_endpoint=request.host_url.strip('/') + request.path
    )

    results = {
        "type": "FeatureCollection",
        "features": [
        ]
    }

    for listing in listings:
        results["features"].append(property_to_json(listing))

    response = Response(json.dumps(results))
    response.headers['Links'] = link_header
    return response

if __name__ == '__main__':
    app.run()
