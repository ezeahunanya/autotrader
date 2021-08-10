# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose

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
        value = re.search('\(\d{2}', value)[0].replace('(', '')
    return value

class AutotraderCarsItem(scrapy.Item):
    # define the fields for your item here like:
    advert_id = scrapy.Field()
    date_scraped = scrapy.Field()
    time_scraped = scrapy.Field()
    make = scrapy.Field()
    model = scrapy.Field()
    trim = scrapy.Field()
    manufactured_year = scrapy.Field(input_processor = MapCompose(get_manufactured_year), output_processor = TakeFirst())
    manufactured_year_identifier = scrapy.Field(input_processor = MapCompose(get_manufactured_year_identifier), output_processor = TakeFirst())
    body_type = scrapy.Field()
    mileage = scrapy.Field(input_processor = MapCompose(clean_mileage, clean_big_number), output_processor = TakeFirst())
    engine_size = scrapy.Field(input_processor = MapCompose(clean_engine_size), output_processor = TakeFirst())
    transmission = scrapy.Field()
    fuel_type = scrapy.Field()
    doors = scrapy.Field(input_processor = MapCompose(strip_doors), output_processor = TakeFirst())
    seats = scrapy.Field(input_processor = MapCompose(strip_seats), output_processor = TakeFirst())
    number_of_owners = scrapy.Field(input_processor = MapCompose(get_owners), output_processor = TakeFirst())
    emission_scheme = scrapy.Field()
    vehicle_location_postcode = scrapy.Field()
    vehicle_location_latitude = scrapy.Field(input_processor = MapCompose(get_latitude), output_processor = TakeFirst())
    vehicle_location_longitude = scrapy.Field(input_processor = MapCompose(get_longitude), output_processor = TakeFirst())
    vehicle_registration_mark = scrapy.Field()
    derivative_id = scrapy.Field()
    condition = scrapy.Field()
    imported = scrapy.Field()
    average_mileage = scrapy.Field()
    mileage_deviation = scrapy.Field()
    mileage_deviation_type = scrapy.Field()
    ad_description = scrapy.Field()
    price = scrapy.Field(input_processor = MapCompose(strip_currency, clean_big_number), output_processor = TakeFirst())
    price_excluding_fees = scrapy.Field(input_processor = MapCompose(strip_currency, clean_big_number), output_processor = TakeFirst())
    no_admin_fees = scrapy.Field()
    price_deviation = scrapy.Field()
    price_deviation_type = scrapy.Field()
    price_rating = scrapy.Field()
    price_rating_label = scrapy.Field()
    seller_name = scrapy.Field()
    seller_id = scrapy.Field()
    is_dealer_trusted = scrapy.Field()
    seller_longlat = scrapy.Field()
    seller_segment = scrapy.Field()
    seller_rating = scrapy.Field()
    total_reviews = scrapy.Field()
    seller_postcode = scrapy.Field()
    seller_address_one = scrapy.Field()
    seller_address_two = scrapy.Field()
    page_url = scrapy.Field()
    number_of_photos = scrapy.Field()
    co2_emissions = scrapy.Field(input_processor = MapCompose(clean_co2), output_processor = TakeFirst())
    tax = scrapy.Field()