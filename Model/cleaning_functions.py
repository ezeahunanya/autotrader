import sys
import os

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import mysql.connector
from data_preparation.autotrader_scraper.autotrader_scraper.config import mysql_details
import pandas as pd

def load_data_from_database():
    '''
    Return full dataset with vehicle features.
    '''

    DB_NAME = 'autotrader_adverts'
    
    cnx = mysql.connector.connect(**mysql_details)
    cursor = cnx.cursor(dictionary=True)

    cursor.execute("USE {}".format(DB_NAME))
    cursor.execute('''SELECT * 
                  FROM vehicle_features 
                  ORDER BY date_scraped ASC, time_scraped ASC''')
    
    full_results = cursor.fetchall()
    cnx.close()

    return pd.DataFrame(full_results)

def drop_columns(df):
    '''
    Drops columns from dataframe.
    '''

    columns_to_drop = ['max_loading_weight', 'zero_to_sixty_two', 'gross_vehicle_weight',   
                       'price_deviation', 'price_deviation_type',  
                       'price_rating', 'price_rating_label', 'zero_to_sixty',               
                       'advert_id', 'seller_id', 'date_scraped', 'time_scraped',
                       'vehicle_location_postcode', 'page_url',
                       'ad_description', 'price_excluding_fees', 'no_admin_fees', 'manufactured_year_identifier',
                       'vehicle_registration_mark', 'derivative_id', 'car_condition', 'minimum_kerb_weight', 'average_mileage',
                       'mileage_deviation', 'mileage_deviation_type', 'number_of_photos', 
                       'body_type', 'transmission', 'fuel_type', 'doors', 'seats', 'number_of_owners', 'emission_scheme',
                       'vehicle_location_latitude', 'vehicle_location_longitude', 'imported',
                       'number_of_photos', 'tax', 'cylinders', 'valves', 'combined', 'insurance_group', 'boot_space_seats_down']

    return df.drop(columns_to_drop, axis=1)