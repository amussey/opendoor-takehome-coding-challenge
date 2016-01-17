from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return 'Welcome to the Opendoor listings API!'


@app.route('/listings')
def listings():
    return '{}'

if __name__ == '__main__':
    app.run()
