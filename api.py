from preprocess import preprocess
from flask import Flask
import os


def create_app():
    preprocess(mysql_url=os.environ['CLEARDB_DATABASE_URL'])
    app = Flask(__name__)

    return app

app = create_app()


@app.route('/')
def index():
    return 'Welcome to the Opendoor listings API!'


@app.route('/listings')
def listings():
    return '{}'

if __name__ == '__main__':
    app.run()
