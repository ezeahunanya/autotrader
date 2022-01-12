import sys
import os

module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)

import mysql.connector
from data_preparation.autotrader_scraper.autotrader_scraper.config import mysql_details
import pandas as pd
import numpy as np
from data_preparation.data_cleaning import combine_CO2_columns, fill_trim_missing_values


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


def fill_columns_with_missing_values(df):
    '''
    Returns dataframe after inputing missing values using groupby on car make.
    '''
    
    columns = ['urban', 'extra_urban', 'boot_space_seats_up', 'fuel_tank_capacity',
       'engine_torque', 'top_speed', 'width', 'wheelbase', 'height',
       'length', 'co2_emissions', 'engine_size', 'engine_power']

    df = df.copy()
    
    for column in columns:
        if df[column].dtype == pd.Int64Dtype():
            df[column] = df.groupby(['make', 'model', 'trim','manufactured_year'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else pd.NA))
            df[column] = df.groupby(['make', 'model', 'trim'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else pd.NA))
            df[column] = df.groupby(['make', 'model'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else pd.NA))

        elif df[column].dtype == float:
            df[column] = df.groupby(['make', 'model', 'trim', 'manufactured_year'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
            df[column] = df.groupby(['make', 'model', 'trim'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
            df[column] = df.groupby(['make', 'model'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else pd.NA))
        
        else:
            df[column] = df.groupby(['make', 'model', 'trim', 'manufactured_year'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
            df[column] = df.groupby(['make', 'model', 'trim'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
            df[column] = df.groupby(['make', 'model'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else pd.NA))
    
    return df    


def fix_int_datatypes(df):
    '''
    Converts columns with Int64 datatypes into int.
    '''

    df = df.copy()
    df = df.astype(dtype={'manufactured_year': 'int', 'mileage': 'int',
                          'top_speed': 'int', 'engine_power': 'int', 'height': 'int', 'length': 'int',
                          'wheelbase': 'int', 'width': 'int', 'boot_space_seats_up': 'int',
                          'co2_emissions': 'int', 'engine_size': 'float', 'engine_torque': 'float', 'urban': 'float',
                          'extra_urban': 'float', 'fuel_tank_capacity': 'int' })
                        
    return df


def fix_formatting(df):
    '''
    Makes strings lowercase and replaces space with '_'.
    '''
    
    df['make'] = df['make'].map(lambda x: x.strip().lower().replace(' ', '-')).astype('category')
    df['model'] = df['model'].map(lambda x: x.strip().lower().replace(' ', '-')).astype('category')
    df['trim'] = df['trim'].map(lambda x: x.strip().lower().replace(' ', '-')).astype('category')

    return df


def prepare_data():
    '''Load and clean data for modelling.'''

    df = load_data_from_database()
    df = drop_columns(df)
    df = combine_CO2_columns(df)
    df = fill_columns_with_missing_values(df)
    df = fill_trim_missing_values(df)
    df = df.dropna()
    df = fix_int_datatypes(df)
    df = fix_formatting(df)
    
    return df