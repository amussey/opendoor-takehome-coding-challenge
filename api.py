from flask import Flask, request, Response
import os
import json

from preprocess import preprocess
from helpers import return_md_as_html, fetch_listings, connect_to_mysql, property_to_json


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
    db = connect_to_mysql(mysql_url=os.environ['CLEARDB_DATABASE_URL'])
    listings, pagination = fetch_listings(db=db, request=request)
    db.close()

    results = {
        "type": "FeatureCollection",
        "features": [property_to_json(listing) for listing in listings]
    }

    response = Response(json.dumps(results))
    response.headers['Links'] = pagination
    return response

if __name__ == '__main__':
    app.run()
