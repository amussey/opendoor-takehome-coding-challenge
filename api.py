from flask import Flask
import os

from preprocess import preprocess
from helpers import return_md_as_html


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
    return '{}'

if __name__ == '__main__':
    app.run()
