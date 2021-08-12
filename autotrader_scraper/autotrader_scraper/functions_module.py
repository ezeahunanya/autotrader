import numpy as np
import re


def get_dictionary_value(dictionary, keys):
    '''
    Gets value from nested dictionary.

    Parameters
    ----------
    dictionary: dict
        Dictionary to search in.
    keys: list
        Keys to search the dictionary with. 

    Returns
    -------
    dictionary: int or str or bool or dict or nan
        int or str or bool if bottom-level of dictionary 
        dict if not bottom-level of dictionary
        numpy nan value if KeyError is raised
    '''

    for key in keys:
            
        try:
            dictionary = dictionary[key]

        except KeyError:
            dictionary = np.nan
            break   

    return dictionary


def strip_currency(value):
    '''
    Strips pound(£) symbol from string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.replace('£', '')

    return value


def clean_big_number(value):
    '''
    Strips comma from big number string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.replace(',', '')

    return value


def clean_mileage(value):
    '''
    Strips 'miles' str from mileage.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.replace(' miles', '')

    return value


def clean_engine_size(value):
    '''
    Strips 'L' str from engine size.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.replace('L', '')

    return value


def strip_doors(value):
    '''
    Strips 'door' str from number of doors.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.replace(' doors', '')

    return value


def strip_seats(value):
    '''
    Strips 'seats' str from number of seats.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.replace(' seats', '')
        
    return value


def get_owners(value):
    '''
    Extracts number of owners in string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = re.search('\d+', value)[0]

    return value


def get_latitude(value):
    '''
    Extracts latitude from latitude/longitude string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.split(',')[0]

    return value


def get_longitude(value):
    '''
    Extracts longitude from latitude/longitude string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.split(',')[1]

    return value


def clean_co2(value):
    '''
    Strips 'g/km' str from CO2 emmisions.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = value.replace('g/km', '')

    return value


def get_manufactured_year(value):
    '''
    Extracts year from string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = re.search('\d{4}', value)[0]
        
    return value


def get_manufactured_year_identifier(value):
    '''
    Extracts registration indentifier from string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or nan
        str if string provided 
        numpy nan if nan provided
    '''

    if value is np.nan:
        value = value

    else:
        value = re.search('\(\w+', value)[0].replace('(', '')

    return value