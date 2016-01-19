
class Listings:
    """A class containing all of the listing info from a user's request.

    Attributes:
        LISTINGS_PER_PAGE (int): The number of listings in a single JSON response.
        db (MySQLdb.connections.Connection): A connection to the backend MySQL server.
        request (werkzeug.local.LocalProxy): The Flask request object from the user.
        listing_count (int): The total number of listings given the user's query parameters.
        total_pages (int): The total number of pages given the number of listings.
        current_page (int): The current page of JSON the user is on.
        listings (tuple): A set of properties in the form of rows from MySQL.
    """
    LISTINGS_PER_PAGE = 15

    def __init__(self, db, request):
        """Initialize a listings object.

        This runs through a couple tasks:
         * Read the total number of listings given the user's query parameters.
         * Calculate the total number of pages given the number of listings.
         * Store a set of listings given the current page the user is on.

        Args:
            db (MySQLdb.connections.Connection): A connection to the backend MySQL server.
            request (werkzeug.local.LocalProxy): The Flask request object from the user.
        """

        self.db = db
        self.request = request

        # Fetch the number of listings.
        self.listing_count = self._count_listings()

        # Read the number of pages.
        self.total_pages = (self.listing_count / self.LISTINGS_PER_PAGE) + 1
        self.current_page = self._read_page()

        self.listings = self._fetch_listings()

    def pagination_header(self):
        """Build the pagination `Link` header.

        Returns:
            str: The pagination header string for placement in the `Link` header.
        """

        api_endpoint = self.request.host_url.strip('/') + self.request.path

        # Rebuild the current URL and query string without including the current page.
        query_string = '&'.join(['{}={}'.format(key, value) for key, value in self.request.args.items() if key != 'page'])
        base_api_endpoint = '<' + api_endpoint + '?' + (query_string + '&page={}>; rel="{}"').strip('&')

        links = [
            base_api_endpoint.format(1, 'first'),
            base_api_endpoint.format(self.total_pages, 'last'),
        ]
        if self.current_page > 1:
            links.append(base_api_endpoint.format(self.current_page - 1, 'prev'))
        if self.current_page < self.total_pages:
            links.append(base_api_endpoint.format(self.current_page + 1, 'next'))

        return ', '.join(links)

    def to_dict(self):
        """Convert the stored set of listings into a dict.

        Once converted to JSON, this dict will be valid GeoJSON.

        Returns:
            dict: A set of all the listings, ready to be converted to JSON.
        """
        results = {
            'type': 'FeatureCollection',
            'features': [self._property_to_json(listing) for listing in self.listings]
        }

        return results

    def _count_listings(self):
        """Count the number of listings given the provided set of filters.

        Returns:
            int: The number of listings that match the user's filter parameters.
        """

        cursor = self.db.cursor()

        sql = "SELECT count(*) AS count FROM listings" + self._sql_filters()

        cursor.execute(sql)
        return cursor.fetchall()[0][0]

    def _read_page(self):
        """Read the current page of JSON the user is on.

        This handles some basic error correction in case the user requests a
        page that is higher or lower than the highest or lowest bounds.

        Returns:
            int: The current page the user is on.
        """

        current_page = int(self.request.args.get('page', 1))

        if current_page < 1:
            current_page = 1
        if current_page > self.total_pages:
            current_page = self.total_pages

        return current_page

    def _fetch_listings(self):
        """Fetch the listings from the database that match the user's filters.

        Returns:
            tuple: A set of all the listings that match the user's filters.
        """

        cursor = self.db.cursor()

        start = (self.current_page - 1) * self.LISTINGS_PER_PAGE

        sql = 'SELECT id, price, street, bedrooms, bathrooms, sq_ft, lat, lng FROM listings'
        sql = sql + self._sql_filters() + ' LIMIT {}, {}'.format(start, self.LISTINGS_PER_PAGE)

        cursor.execute(sql)
        return cursor.fetchall()

    def _sql_filters(self):
        """Construct a SQL WHERE clause for any user provided filters.

        Returns:
            str: A SQL WHERE clause as a string if the user has specified any
                filters/query parameters.  Otherwise, returns an empty string.
        """

        params = self.request.args
        sql_where = []

        if params.get('min_price', None):
            sql_where.append('price >= %i' % int(params['min_price']))
        if params.get('max_price', None):
            sql_where.append('price <= %i' % int(params['max_price']))
        if params.get('min_bed', None):
            sql_where.append('bedrooms >= %i' % int(params['min_bed']))
        if params.get('max_bed', None):
            sql_where.append('bedrooms <= %i' % int(params['max_bed']))
        if params.get('min_bath', None):
            sql_where.append('bathrooms >= %i' % int(params['min_bath']))
        if params.get('max_bath', None):
            sql_where.append('bathrooms <= %i' % int(params['max_bath']))

        if len(sql_where) > 0:
            return ' WHERE ' + ' AND '.join(sql_where)
        return ''

    def _property_to_json(self, mysql_row):
        """Convert a property listing from a MySQL row into a dict.

        Args:
            mysql_row (tuple): A property listing in the form of a row from the MySQL database.

        Returns:
            dict: The MySQL row in valid GeoJSON format.
        """

        return {
            'type': 'Feature',
            'geometry': {'type': 'Point', 'coordinates': [mysql_row[6], mysql_row[7]]},
            'properties': {
                'id': mysql_row[0],
                'price': mysql_row[1],
                'street': mysql_row[2],
                'bedrooms': mysql_row[3],
                'bathrooms': mysql_row[4],
                'sq_ft': mysql_row[5]
            },
        }
