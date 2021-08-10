# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose
import numpy as np
import re

def strip_currency(value):
    if value is np.nan:
        value = value
    else:
        value = value.replace('£', '')
    return value

def clean_big_number(value):
    if value is np.nan:
        value = value
    else:
        value = value.replace(',', '')
    return value

def clean_mileage(value):
    if value is np.nan:
        value = value
    else:
        value = value.replace(' miles', '')
    return value

def clean_engine_size(value):
    if value is np.nan:
        value = value
    else:
        value = value.replace('L', '')
    return value

def strip_doors(value):
    if value is np.nan:
        value = value
    else:
        value = value.replace(' doors', '')
    return value

def strip_seats(value):
    if value is np.nan:
        value = value
    else:
        value = value.replace(' seats', '')
    return value

def get_owners(value):
    if value is np.nan:
        value = value
    else:
        value = re.search('\d+', value)[0]
    return value

def get_latitude(value):
    if value is np.nan:
        value = value
    else:
        value = value.split(',')[0]
    return value

def get_longitude(value):
    if value is np.nan:
        value = value
    else:
        value = value.split(',')[1]
    return value

def clean_co2(value):
    if value is np.nan:
        value = value
    else:
        value = value.replace('g/km', '')
    return value

def get_manufactured_year(value):
    if value is np.nan:
        value = value
    else:
        value = re.search('\d{4}', value)[0]
    return value

def get_manufactured_year_identifier(value):
    if value is np.nan:
        value = value
    else:
        value = re.search('\(\w+', value)[0].replace('(', '')
    return value

class AutotraderCarsItem(scrapy.Item):
    # define the fields for your item here like:
    advert_id = scrapy.Field(output_processor = TakeFirst())
    date_scraped = scrapy.Field(output_processor = TakeFirst())
    time_scraped = scrapy.Field(output_processor = TakeFirst())
    make = scrapy.Field(output_processor = TakeFirst())
    model = scrapy.Field(output_processor = TakeFirst())
    trim = scrapy.Field(output_processor = TakeFirst())
    manufactured_year = scrapy.Field(input_processor = MapCompose(get_manufactured_year), output_processor = TakeFirst())
    manufactured_year_identifier = scrapy.Field(input_processor = MapCompose(get_manufactured_year_identifier), output_processor = TakeFirst())
    body_type = scrapy.Field(output_processor = TakeFirst())
    mileage = scrapy.Field(input_processor = MapCompose(clean_mileage, clean_big_number), output_processor = TakeFirst())
    engine_size = scrapy.Field(input_processor = MapCompose(clean_engine_size), output_processor = TakeFirst())
    transmission = scrapy.Field(output_processor = TakeFirst())
    fuel_type = scrapy.Field(output_processor = TakeFirst())
    doors = scrapy.Field(input_processor = MapCompose(strip_doors), output_processor = TakeFirst())
    seats = scrapy.Field(input_processor = MapCompose(strip_seats), output_processor = TakeFirst())
    number_of_owners = scrapy.Field(input_processor = MapCompose(get_owners), output_processor = TakeFirst())
    emission_scheme = scrapy.Field(output_processor = TakeFirst())
    vehicle_location_postcode = scrapy.Field(output_processor = TakeFirst())
    vehicle_location_latitude = scrapy.Field(input_processor = MapCompose(get_latitude), output_processor = TakeFirst())
    vehicle_location_longitude = scrapy.Field(input_processor = MapCompose(get_longitude), output_processor = TakeFirst())
    vehicle_registration_mark = scrapy.Field(output_processor = TakeFirst())
    derivative_id = scrapy.Field(output_processor = TakeFirst())
    condition = scrapy.Field(output_processor = TakeFirst())
    imported = scrapy.Field(output_processor = TakeFirst())
    average_mileage = scrapy.Field(output_processor = TakeFirst())
    mileage_deviation = scrapy.Field(output_processor = TakeFirst())
    mileage_deviation_type = scrapy.Field(output_processor = TakeFirst())
    ad_description = scrapy.Field(output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(strip_currency, clean_big_number), output_processor = TakeFirst())
    price_excluding_fees = scrapy.Field(input_processor = MapCompose(strip_currency, clean_big_number), output_processor = TakeFirst())
    no_admin_fees = scrapy.Field(output_processor = TakeFirst())
    price_deviation = scrapy.Field(output_processor = TakeFirst())
    price_deviation_type = scrapy.Field(output_processor = TakeFirst())
    price_rating = scrapy.Field(output_processor = TakeFirst())
    price_rating_label = scrapy.Field(output_processor = TakeFirst())
    seller_name = scrapy.Field(output_processor = TakeFirst())
    seller_id = scrapy.Field(output_processor = TakeFirst())
    is_dealer_trusted = scrapy.Field(output_processor = TakeFirst())
    seller_longlat = scrapy.Field(output_processor = TakeFirst())
    seller_segment = scrapy.Field(output_processor = TakeFirst())
    seller_rating = scrapy.Field(output_processor = TakeFirst())
    total_reviews = scrapy.Field(output_processor = TakeFirst())
    seller_postcode = scrapy.Field(output_processor = TakeFirst())
    seller_address_one = scrapy.Field(output_processor = TakeFirst())
    seller_address_two = scrapy.Field(output_processor = TakeFirst())
    page_url = scrapy.Field(output_processor = TakeFirst())
    number_of_photos = scrapy.Field(output_processor = TakeFirst())
    co2_emissions = scrapy.Field(input_processor = MapCompose(clean_co2), output_processor = TakeFirst())
    tax = scrapy.Field(output_processor = TakeFirst())