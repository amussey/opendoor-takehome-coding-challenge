import mistune
from urlparse import urlparse
import MySQLdb


def return_md_as_html(filename, title):
    markdown = open(filename, 'r')
    markdown_html = mistune.markdown(markdown.read())
    markdown.close()

    html = """
        <html>
            <head>
                <title>{title}</title>
                <link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" />
                <style>
                table, th, td {{
                    border: 1px solid black;
                    padding: 5px;
                }}
                body {{
                    padding: 0 20px;
                }}
                </style>
            </head>
            <body>
                <div id="content">
            {problem_html}
                </div>
            <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js"></script>
            </body>
        </html>
    """.format(title=title, problem_html=markdown_html.strip())

    return html


def fetch_listings(mysql_url, params=[]):
    mysql_connection_string = urlparse(mysql_url)

    db = MySQLdb.connect(host=mysql_connection_string.hostname,
                         user=mysql_connection_string.username,
                         passwd=mysql_connection_string.password,
                         db=mysql_connection_string.path.strip('/'))

    cursor = db.cursor()

    sql = """
        SELECT
            id,
            price,
            street,
            bedrooms,
            bathrooms,
            sq_ft,
            lat,
            lng
        FROM listings
    """

    sql_where = []

    if params.get('min_price', None):
        sql_where.append("price >= %i" % int(params['min_price']))
    if params.get('max_price', None):
        sql_where.append("price <= %i" % int(params['max_price']))
    if params.get('min_bed', None):
        sql_where.append("bedrooms >= %i" % int(params['min_bed']))
    if params.get('max_bed', None):
        sql_where.append("bedrooms <= %i" % int(params['max_bed']))
    if params.get('min_bath', None):
        sql_where.append("bathrooms >= %i" % int(params['min_bath']))
    if params.get('max_bath', None):
        sql_where.append("bathrooms <= %i" % int(params['max_bath']))

    if len(sql_where) > 0:
        sql = sql + " WHERE " + " AND ".join(sql_where)

    print sql

    cursor.execute(sql)
    rows = cursor.fetchall()

    db.close()

    return rows


def property_to_json(mysql_row):
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": [mysql_row[6], mysql_row[7]]},
        "properties": {
            "id": mysql_row[0],
            "price": mysql_row[1],
            "street": mysql_row[2],
            "bedrooms": mysql_row[3],
            "bathrooms": mysql_row[4],
            "sq_ft": mysql_row[5]
        },
    }
