from flask import Flask, request
import os
import json

from preprocess import preprocess
from helpers import return_md_as_html, fetch_listings, property_to_json


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

    results = {
        "type": "FeatureCollection",
        "features": [
        ]
    }

    for listing in listings:
        results["features"].append(property_to_json(listing))

    return json.dumps(results)

if __name__ == '__main__':
    app.run()
