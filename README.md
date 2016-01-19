# Opendoor Take-Home Coding Challenge

This API was written as a part of the [Opendoor](http://opendoor.com) interview process.  A full problem description can be found in [PROBLEM.md](PROBLEM.md)

## Querying

Data is loaded from https://s3.amazonaws.com/opendoor-problems/listings.csv on boot.

The available endpoints are:

| Endpoint    | Supported Methods | Description                             |
|-------------|-------------------|-----------------------------------------|
| `/`         | `GET`             | Returns the contents `PROBLEM.md`.      | 
| `/listings` | `GET`             | Fetch a JSON list of house listings.    |

The `/listings` endpoint supports the following query parameters:

| Parameter    | Description                                       |
|--------------|---------------------------------------------------|
| `min_price`  | The minimum listing price in dollars (inclusive). |
| `max_price`  | The maximum listing price in dollars (inclusive). |
| `min_bed`    | The minimum number of bedrooms (inclusive).       |
| `max_bed`    | The maximum number of bedrooms (inclusive).       |
| `min_bath`   | The minimum number of bathrooms (inclusive).      |
| `max_bath`   | The maximum number of bathrooms (inclusive).      |


## Requirements

 * Python 2.7 (currently, `MySQL-python` is not Python 3 compatible)
 * [VirtualEnv](http://docs.python-guide.org/en/latest/dev/virtualenvs/)
 * Foreman

## Running

The easiest way to run the app is to simply deploy it to Heroku.  [View the *Deploying* section](#deploying) for an easy, one click button to do this.

To run the app locally, start by creating a `.env` file containing a `CLEARDB_DATABASE_URL` and your credentials:

```
CLEARDB_DATABASE_URL=mysql://username:password@hostname.com/database
```

Next, run the following commands to install the Python dependencies

```bash
virtualenv env
source env/bin/activate
pip install -r requirements
foreman start
```

If you are running the app on OSX, you may encounter an error while installing `MySQL-python`.  This can generally be cleared up by installing the MySQL C dependencies with `brew install mysql`.

After running `foreman start`, the app should be running on [port 5000](http://localhost:5000).

## Testing

Currently, there are no tests (see the *Future Improvements* section for more info).

To run the Python linter, run:

```
make lint
```

## Deploying

[![One Click Heroku Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy?template=https://github.com/amussey/opendoor-takehome-coding-challenge)

This project is designed to be run on Heroku with a ClearDB MySQL backend (the free *Ignite* tier provides enough storage for the Opendoor CSV file).  Information on manually deploying to Heroku can be found [here](https://devcenter.heroku.com/articles/getting-started-with-python#deploy-the-app).

## Requirements Breakdown

At a minimum:
 - [X] Your API endpoint URL is `/listings`.
 - [X] Your API responds with valid GeoJSON (you can check the output using http://geojson.io).
     + The output of this app has been linted against [GeoJSONlint.com](http://geojsonlint.com).
 - [X] Your API should correctly filter any combination of API parameters.
 - [X] Use a datastore.
     + This projected is backed my MySQL.  The Heroku deploy button creates a ClearDB MySQL instance for storing and manipulating the data.

Bonus Points:
 - [X] Pagination via web linking (http://tools.ietf.org/html/rfc5988).
     + The `Link` header can be easily viewed with `curl` by running `curl -i "http://API-URL:5000/listings?page=30"`.  `first` and `last` paging is always available, and `prev` and `next` are available when applicable.

## Future Improvements

Given more time, I would like to make the following improvements:

 * Tests (primarily unit and acceptance).
 * Filtering based on the `status` of the listings.  Currently, all listings are being returned with no indicator of what state they are in (`active`, `pending`, or `sold`).
 * Currently, every query against `/listings` creates a new MySQL connection.  Ideally, one connection could be created when the app launches and be refreshed when a disconnect is detected.
 * Page sizes are currently static (locked to 15).  There should be a `count` parameter to make this configurable.
 * Better exception handling.  There area a couple places where exception handling could be improved, such as around the database connection and around the handling of the CSV data.
 * Sorting.  The `/listings` endpoint currently always sorts by `id`.
