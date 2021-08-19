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
    dictionary: int or str or bool or dict or none
        int or str or bool if bottom-level of dictionary 
        dict if not bottom-level of dictionary
        none value if KeyError is raised
    '''

    for key in keys:
            
        try:
            dictionary = dictionary[key]

        except KeyError:
            dictionary = None
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
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
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
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
        value = value

    else:
        value = value.replace(',', '')

    return value


def get_latitude(value):
    '''
    Extracts latitude from latitude/longitude string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
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
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
        value = value

    else:
        value = value.split(',')[1]

    return value


def get_manufactured_year(value):
    '''
    Extracts year from string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
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
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
        value = value

    else:
        value = re.search('\(\w+', value)[0].replace('(', '')

    return value

def get_number(value):
    '''
    Extracts number from string.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
        value = value

    else:
        value = re.search('\d+\.?\d*', value)[0]

    return value


def clean_phone_number(value):
    '''
    Returns clean phone number.

    Parameters
    ----------
    value: str
        
    Returns
    -------
    str or none
        str if string provided 
        none if none provided
    '''

    if value is None:
        value = value

    else:
        value = value.replace('(', '').replace(')', '').replace(' ', '')

    return value