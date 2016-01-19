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


def connect_to_mysql(mysql_url):
    mysql_connection_string = urlparse(mysql_url)

    db = MySQLdb.connect(host=mysql_connection_string.hostname,
                         user=mysql_connection_string.username,
                         passwd=mysql_connection_string.password,
                         db=mysql_connection_string.path.strip('/'))

    return db


def calculate_pagination(current_page=1, num_of_listings=0):
    listings_per_page = 15

    total_pages = (num_of_listings / listings_per_page) + 1

    if current_page < 1:
        current_page = 1
    if current_page > total_pages:
        current_page = total_pages

    # Calculate the set of listings
    start = (current_page - 1) * listings_per_page
    end = start + listings_per_page

    return start, end


def build_links_header(request, current_page=1, num_of_listings=0):
    listings_per_page = 15

    total_pages = (num_of_listings / listings_per_page) + 1

    if current_page < 1:
        current_page = 1
    if current_page > total_pages:
        current_page = total_pages

    api_endpoint = request.host_url.strip('/') + request.path

    query_string = '&'.join(['{}={}'.format(key, value) for key, value in request.args.items() if key != 'page'])
    base_api_endpoint = '<' + api_endpoint + '?' + (query_string + '&page={}>; rel="{}"').strip('&')

    links = [
        base_api_endpoint.format(1, "first"),
        base_api_endpoint.format(total_pages, "last"),
    ]
    if current_page > 1:
        links.append(base_api_endpoint.format(current_page - 1, "prev"))
    if current_page < total_pages:
        links.append(base_api_endpoint.format(current_page + 1, "next"))

    return ', '.join(links)


def fetch_listings(db, request):
    params = request.args
    cursor = db.cursor()

    sql_select_header = "SELECT id, price, street, bedrooms, bathrooms, sq_ft, lat, lng FROM listings"
    sql_count_header = "SELECT count(*) AS count FROM listings"

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
        sql_count_header = sql_count_header + " WHERE " + " AND ".join(sql_where)

    cursor.execute(sql_count_header)
    num_of_listings = cursor.fetchall()[0][0]

    current_page = int(params.get('page', 1))

    start_page, end_page = calculate_pagination(current_page=current_page, num_of_listings=num_of_listings)
    pagination_header = build_links_header(request=request, current_page=current_page, num_of_listings=num_of_listings)

    if len(sql_where) > 0:
        sql_select_header = sql_select_header + " WHERE " + " AND ".join(sql_where)
    sql_select_header += " LIMIT {}, {}".format(start_page, end_page)

    cursor.execute(sql_select_header)
    rows = cursor.fetchall()

    return rows, pagination_header


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
