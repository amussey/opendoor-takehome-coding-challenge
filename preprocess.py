import csv
import urllib2
from urlparse import urlparse
import MySQLdb


def preprocess(mysql_url, csv_url='https://s3.amazonaws.com/opendoor-problems/listings.csv'):

    print "Connecting to database..."
    mysql_connection_string = urlparse(mysql_url)

    db = MySQLdb.connect(host=mysql_connection_string.hostname,
                         user=mysql_connection_string.username,
                         passwd=mysql_connection_string.password,
                         db=mysql_connection_string.path.strip('/'))

    cursor = db.cursor()

    print "Rebuilding table structure..."
    cursor.execute("DROP TABLE IF EXISTS listings")

    cursor.execute("""
        CREATE TABLE `listings` (
            `id` INT NOT NULL,
            `street` TEXT NULL,
            `status` VARCHAR(64) NULL,
            `price` INT NULL,
            `bedrooms` INT NULL,
            `bathrooms` INT NULL,
            `sq_ft` INT NULL,
            `lat` DOUBLE NULL,
            `lng` DOUBLE NULL,
            PRIMARY KEY (`id`) );
        """)

    print "Loading CSV data..."
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

    cursor.execute("INSERT INTO listings (id, street, status, price, bedrooms, bathrooms, sq_ft, lat, lng) VALUES " + ", ".join(csv_data))

    db.commit()

    print "CSV data loaded."
    db.close()
