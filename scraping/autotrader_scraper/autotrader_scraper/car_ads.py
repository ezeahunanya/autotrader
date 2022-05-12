import mysql.connector
from autotrader_scraper.config import mysql_details

DB_NAME = 'autotrader_adverts'
advert_ids = []

try:
    cnx = mysql.connector.connect(**mysql_details)
    cursor = cnx.cursor()

    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute("SELECT advert_id FROM vehicle_features")
    results = cursor.fetchall()
    cnx.close()

    for id in results:
        advert_ids.append(id[0])

except:
    pass