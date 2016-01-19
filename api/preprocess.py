import csv
import urllib2


def preprocess(db, csv_url='https://s3.amazonaws.com/opendoor-problems/listings.csv'):
    cursor = db.cursor()

    print "Rebuilding table structure..."
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

    cursor.execute(
        "INSERT INTO listings (id, street, status, price, bedrooms, bathrooms, sq_ft, lat, lng) VALUES " +
        ", ".join(csv_data) +
        " ON DUPLICATE KEY UPDATE street=street, status=status, price=price, bedrooms=bedrooms, bathrooms=bathrooms, sq_ft=sq_ft, lat=lat, lng=lng"
    )

    db.commit()

    print "CSV data loaded."
