import mysql.connector
from autotrader_scraper.autotrader_scraper.config import mysql_details
import pandas as pd

def get_data():
    '''
    Return full dataset with vehicle features and seller information joined
    in one table.
    '''
    
    DB_NAME = 'autotrader_adverts'
    
    cnx = mysql.connector.connect(**mysql_details)
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute('''SELECT * 
                  FROM vehicle_features as vf
                  LEFT JOIN sellers as s
                  ON vf.seller_id=s.seller_id
                  ORDER BY date_scraped ASC, time_scraped ASC''')
    
    full_results = cursor.fetchall()
    cnx.close()

    return pd.DataFrame(full_results)