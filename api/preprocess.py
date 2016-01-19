import csv
import urllib2


def preprocess(db, csv_url='https://s3.amazonaws.com/opendoor-problems/listings.csv'):
    """This function used to load the CSV data into the MYSQL database.

    When the Flask app is first launched, this function loads the from the
    remote CSV file into the MySQL database.  The data is keyed off of the id.
    If the `listings` table or data is already detected in the database, the
    data is updated in-place.

    Args:
        db (MySQLdb.connections.Connection): A connection to the backend MySQL server.
        csv_url (Optional[str]): A URL string to the CSV listing data.
    """

    cursor = db.cursor()

    print 'Rebuilding table structure...'
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS `listings` (
            `id` INT NOT NULL,
            `street` TEXT NULL,
            `status` VARCHAR(64) NULL,
            `price` INT NULL,
            `bedrooms` INT NULL,
            `bathrooms` INT NULL,
            `sq_ft` INT NULL,
            `lat` DOUBLE NULL,
            `lng` DOUBLE NULL,
            PRIMARY KEY (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=latin1;
        """)

    print 'Loading CSV data...'
    csv_data = []

    csv_file = urllib2.urlopen(csv_url)
    reader = csv.DictReader(csv_file)

    for row in reader:
        csv_data.append(
            "('%i', '%s', '%s', '%i', '%i', '%i', '%i', '%s', '%s')" % (
                int(row['id']),
                row['street'],
                row['status'],
                int(row['price']),
                int(row['bedrooms']),
                int(row['bathrooms']),
                int(row['sq_ft']),
                float(row['lat']),
                float(row['lng']),
            ))

    cursor.execute(
        'INSERT INTO listings (id, street, status, price, bedrooms, bathrooms, sq_ft, lat, lng) VALUES ' +
        ', '.join(csv_data) +
        ' ON DUPLICATE KEY UPDATE street=street, status=status, price=price, bedrooms=bedrooms, bathrooms=bathrooms, sq_ft=sq_ft, lat=lat, lng=lng'
    )

    db.commit()

    print 'CSV data loaded.'
