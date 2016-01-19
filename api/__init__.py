from flask import Flask, request, Response
import os

from api.preprocess import preprocess
from api.helpers import return_md_as_html, connect_to_mysql
from api.listings import Listings


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

    listings = Listings(db=db, request=request)

    response = Response(listings.to_json())
    response.headers['Links'] = listings.pagination_header()

    return response

if __name__ == '__main__':
    app.run()
