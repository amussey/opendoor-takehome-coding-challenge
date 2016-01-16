#Opendoor Engineering Problem

Originally found on Google Docs [here](https://docs.google.com/document/d/1VKMT-ajGzRb3B9IrfWJJC9xcMB3MGR6WQvCClLx5nRc/edit).

The question below is meant to give candidates a sense of the problems we tackle at Opendoor. Please submit solutions in the form of a readme + working code. The problems should take under 2 hours to complete.

Write an API endpoint that returns a filtered set of listings from the data provided:

https://s3.amazonaws.com/opendoor-problems/listings.csv

API:
```
GET /listings?min_price=100000&max_price=200000&min_bed=2&max_bed=2&min_bath=2&max_bath=2
```


| Parameter    | Description                           |
|--------------|---------------------------------------|
| `min_price`  | The minimum listing price in dollars. |
| `max_price`  | The maximum listing price in dollars. |
| `min_bed`    | The minimum number of bedrooms.       |
| `max_bed`    | The maximum number of bedrooms.       |
| `min_bath`   | The minimum number of bathrooms.      |
| `max_bath`   | The maximum number of bathrooms.      |


The expected response is a GeoJSON FeatureCollection of listings:

```
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [-112.1,33.4]},
      "properties": {
  "id": "123ABC", # CSV id
  "price": 200000, # Price in Dollars
  "street": "123 Walnut St",
        "bedrooms": 3, # Bedrooms
        "bathrooms": 2, # Bathrooms
        "sq_ft": 1500 # Square Footage
    },
    ...
  ]
}
```

All query parameters are optional, all minimum and maximum fields should be inclusive (e.g. min_bed=2&max_bed=4 should return listings with 2, 3, or 4 bedrooms).

At a minimum:
- Your API endpoint URL is `/listings`
- Your API responds with valid GeoJSON (you can check the output using http://geojson.io)
- Your API should correctly filter any combination of API parameters
- Use a datastore

Bonus Points:
- Pagination via web linking (http://tools.ietf.org/html/rfc5988)

When you're done, please deploy your solution somewhere (Heroku works great) and push your code to a GitHub repository and send us the links. Also, please include a brief write-up in a README on what else you'd want to improve or add if you were going to spend more time on it.


