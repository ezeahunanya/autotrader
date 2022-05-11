import sys
import os

module_path = os.path.abspath(os.path.join('..'))
print(module_path)
print(sys.path)
if module_path not in sys.path:
    sys.path.append(module_path)

# import mysql.connector
# from data_preparation.autotrader_scraper.autotrader_scraper.config import mysql_details
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np
from collections import defaultdict

# def get_data_from_database() -> pd.DataFrame:
#     '''
#     Return full dataset with vehicle features and seller information joined
#     in one table.
#     '''

#     DB_NAME = 'autotrader_adverts'
    
#     cnx = mysql.connector.connect(**mysql_details)
#     cursor = cnx.cursor(dictionary=True)

#     cursor.execute("USE {}".format(DB_NAME))
#     cursor.execute('''SELECT * 
#                   FROM vehicle_features as vf
#                   LEFT JOIN sellers as s
#                   ON vf.seller_id=s.seller_id
#                   ORDER BY date_scraped ASC, time_scraped ASC''')
    
#     full_results = cursor.fetchall()
#     cnx.close()

#     return pd.DataFrame(full_results)


def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Drops columns from dataframe.
    '''

    columns_to_drop = ['max_loading_weight', 'zero_to_sixty_two', 'gross_vehicle_weight',   
                       'seller_address_two', 'price_deviation', 'price_deviation_type',  
                       'price_rating', 'price_rating_label', 'zero_to_sixty', 'dealer_website',               
                       'primary_contact_number', 'seller_name', 'seller_id', 'advert_id', 'date_scraped', 'time_scraped',
                       'vehicle_location_postcode', 'seller_postcode', 'seller_address_one', 'page_url', 'country',
                       'ad_description', 'price_excluding_fees', 'no_admin_fees', 'is_dealer_trusted', 'manufactured_year_identifier',
                       'vehicle_registration_mark', 'derivative_id', 'car_condition', 'minimum_kerb_weight', 'average_mileage',
                       'mileage_deviation', 'mileage_deviation_type']

    return df.drop(columns_to_drop, axis=1)


def combine_latitudes_and_longitudes(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Combine latitudes and longitudes into one column.
    '''

    df = df.copy()
    latitudes = df[(df.vehicle_location_longitude.isnull()) & (~df.seller_longlat.isnull())].seller_longlat.map(lambda x: x.split(',')[0])
    longitudes = df[(df.vehicle_location_longitude.isnull()) & (~df.seller_longlat.isnull())].seller_longlat.map(lambda x: x.split(',')[1])

    for index, value in latitudes.items():
        df.loc[index, 'vehicle_location_latitude'] = value

    for index, value in longitudes.items():
        df.loc[index, 'vehicle_location_longitude'] = value

    df.drop('seller_longlat', axis=1, inplace=True)

    return df

def combine_CO2_columns(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Combine CO2 columns into one.
    '''

    df = df.copy()
    co2_emissions = df[(df.co2_emissions.isnull()) & (~df.co2_emission.isnull())].co2_emission
    

    for index, value in co2_emissions.items():
        df.loc[index, 'co2_emissions'] = value

    df.drop('co2_emission', axis=1, inplace=True)

    return df

def ulez_boolean(x: str) -> int:
    '''
    Returns a 1 if 'ULEZ' string is given or a 0 if not.
    '''
    return 1 if x == 'ULEZ' else 0

def convert_emission_scheme_to_boolean(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Convert emission scheme column to boolean column.
    '''
    
    df = df.copy()
    df['ulez'] = df['emission_scheme'].map(ulez_boolean)
    df.drop('emission_scheme', axis=1, inplace=True)

    return df

def clean_round1(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Fixes dtypes for floats and ints. Also makes strings lowercase and replaces
    space with '_'.
    '''

    df = df.astype(dtype={'manufactured_year': 'Int64', 'mileage': 'Int64',
                        'doors': 'Int64', 'seats': 'Int64',
                        'number_of_owners': 'Int64', 'tax': 'Int64',
                        'top_speed': 'Int64', 'cylinders': 'Int64',
                        'valves': 'Int64', 'engine_power': 'Int64',
                        'height': 'Int64', 'length': 'Int64',
                        'wheelbase': 'Int64', 'width': 'Int64',
                        'boot_space_seats_up': 'Int64', 'boot_space_seats_down': 'Int64',
                        'co2_emissions': 'Int64', 'total_reviews': 'Int64',
                        'engine_size': 'float', 'vehicle_location_latitude': 'float',
                        'vehicle_location_longitude': 'float', 'engine_torque': 'float',
                        'fuel_tank_capacity': 'float', 'urban': 'float', 'extra_urban': 'float',
                        'combined': 'float', 'seller_rating': 'float'
                        })

    cols = ['make','model','trim','body_type','transmission','fuel_type','insurance_group','seller_segment','region','county','town']
    sep = defaultdict(lambda:'_', {'make':'-', 'model':'-', 'trim':'-'})
    mapper_params = lambda sep: {'arg': lambda x: x.strip().lower().replace(' ', sep), 'na_action': 'ignore'}
    for col in cols:
        df[col] = df[col].map(**mapper_params(sep[col]))
        if col!='trim':
            df[col] = df[col].astype('category')

    return df

def combine_make_model_trim(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Combines make, model and trim columns.
    '''
    
    df = df.copy()
    df['make_model_trim'] = df.make + '_' + df.model + '_' + df.trim.fillna('')
    df['make_model_trim'] = df['make_model_trim'].apply(lambda x: x.strip('_')).astype('category')

    df = df[['make_model_trim', 'manufactured_year', 'body_type', 'mileage', 'engine_size',
       'transmission', 'fuel_type', 'doors', 'seats', 'number_of_owners',
       'vehicle_location_latitude', 'vehicle_location_longitude', 'imported',
       'price', 'number_of_photos', 'tax', 'top_speed', 'cylinders', 'valves',
       'engine_power', 'engine_torque', 'height', 'length', 'wheelbase',
       'width', 'fuel_tank_capacity', 'boot_space_seats_up',
       'boot_space_seats_down', 'urban', 'extra_urban', 'combined',
       'co2_emissions', 'insurance_group', 'seller_segment', 'seller_rating',
       'total_reviews', 'region', 'county', 'town', 'ulez']]

    return df

def get_percentage_nulls(df: pd.DataFrame) -> pd.Series:
    '''
    Returns percentage of nulls in each coumn in decreasing order.
    '''
    
    return (df.isnull().sum()*100/len(df)).sort_values(ascending=False)


def drop_rows_with_small_percentage_of_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns dataframe after rows in columns with less than 0.1% of missing values are dropped.
    '''
    
    df = df.copy()
    columns=[]
    for index, percentage in get_percentage_nulls(df).items():
        if percentage < 0.1:
            columns.append(index)
    
    return df.dropna(subset=columns)


def fill_columns_with_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Returns dataframe after inputing missing values using groupby on car make.
    '''
    
    columns = ['boot_space_seats_down', 'urban', 'extra_urban',
     'boot_space_seats_up', 'fuel_tank_capacity', 'combined', 'tax',
     'engine_torque', 'insurance_group', 'top_speed', 'width', 'wheelbase',
     'height', 'length', 'seats', 'co2_emissions', 'engine_size', 'mileage',
     'doors']

    df = df.copy()
    
    for column in columns:
        if df[column].dtype == pd.Int64Dtype():
            df[column] = df.groupby(['make', 'model', 'trim','manufactured_year'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else pd.NA))
            df[column] = df.groupby(['make', 'model', 'trim'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else pd.NA))

        elif df[column].dtype == float:
            df[column] = df.groupby(['make', 'model', 'trim', 'manufactured_year'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
            df[column] = df.groupby(['make', 'model', 'trim'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
        
        else:
            df[column] = df.groupby(['make', 'model', 'trim', 'manufactured_year'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
            df[column] = df.groupby(['make', 'model', 'trim'])[column].transform(lambda x: x.fillna(x.mode()[0] if not x.mode().empty else np.nan))
    
    return df

def train_no_of_owners_model(df: pd.DataFrame) -> np.ndarray:
    '''
    Trains regression model which predicts missing values for number of owners using numerical columns with no missing values.     
    '''
    data = df.loc[:, ['mileage', 'manufactured_year', 'engine_power', 'valves', 'cylinders', 'number_of_owners']]



def predict_no_of_owners(df: pd.DataFrame) -> np.ndarray:
    '''
    Predicts missing values for number of owners using numerical columns with no missing values.
    '''
    
    data = df.loc[:, ['mileage', 'manufactured_year', 'engine_power', 'valves', 'cylinders', 'number_of_owners']]

    test_data = data[data.number_of_owners.isnull()]
    data.dropna(inplace=True)

    y_train = data.number_of_owners
    X_train = data.drop("number_of_owners", axis=1)
    X_test = test_data.drop("number_of_owners", axis=1)

    model = LinearRegression()
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    y_pred = np.around(y_pred).astype(int)
    
    return y_pred

def fill_number_of_owners_with_predictions(df):
    '''
    Fills number of owners using predictions made.
    '''
    
    df = df.copy()
    number_of_owners_predictions = pd.Series(predict_no_of_owners(df), index=df[df.number_of_owners.isnull()].index)
    df.number_of_owners = df.number_of_owners.fillna(number_of_owners_predictions)
    
    return df    

def fill_trim_missing_values(df):
    '''
    Fill missing values in trim column.
    '''

    df = df.copy()
    df.trim = df.trim.fillna('base').astype('category')

    return df


def fix_int_datatypes(df):
    '''
    Converts columns with Int64 datatypes into int.
    '''

    df = df.copy()
    df = df.astype(dtype={'manufactured_year': 'int', 'mileage': 'int',
                        'doors': 'int', 'seats': 'int',
                        'number_of_owners': 'int', 'tax': 'int',
                        'top_speed': 'int', 'cylinders': 'int',
                        'valves': 'int', 'engine_power': 'int',
                        'height': 'int', 'length': 'int',
                        'wheelbase': 'int', 'width': 'int',
                        'boot_space_seats_up': 'int', 'boot_space_seats_down': 'int',
                        'co2_emissions': 'int', 'total_reviews': 'int'})
                        
    return df


if __name__ == '__main__':
    df = pd.read_csv('/Users/brook/downloads/data.csv')
    print(df.head())
    print(df.shape)

