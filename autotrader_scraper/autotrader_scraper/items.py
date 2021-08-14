import scrapy
from itemloaders.processors import TakeFirst, MapCompose
import numpy as np
import re
from autotrader_scraper.functions_module import *


class AutotraderCarsItem(scrapy.Item):
    '''
    Represent an item object to save scraped data in after processing. 
    '''

    advert_id = scrapy.Field(output_processor = TakeFirst())
    
    date_scraped = scrapy.Field(output_processor = TakeFirst())
    
    time_scraped = scrapy.Field(output_processor = TakeFirst())
    
    make = scrapy.Field(output_processor = TakeFirst())
    
    model = scrapy.Field(output_processor = TakeFirst())
    
    trim = scrapy.Field(output_processor = TakeFirst())
    
    manufactured_year = scrapy.Field(input_processor = 
                                     MapCompose(get_manufactured_year), 
                                     output_processor = TakeFirst())
    
    manufactured_year_identifier = scrapy.Field(input_processor = 
                                                MapCompose(get_manufactured_year_identifier), 
                                                output_processor = TakeFirst())
    
    body_type = scrapy.Field(output_processor = TakeFirst())
    
    mileage = scrapy.Field(input_processor = MapCompose(clean_big_number, 
                                                        get_number), 
                           output_processor = TakeFirst())
    
    engine_size = scrapy.Field(input_processor = MapCompose(get_number), 
                               output_processor = TakeFirst())
    
    transmission = scrapy.Field(output_processor = TakeFirst())
    
    fuel_type = scrapy.Field(output_processor = TakeFirst())
    
    doors = scrapy.Field(input_processor = MapCompose(get_number), 
                         output_processor = TakeFirst())
    
    seats = scrapy.Field(input_processor = MapCompose(get_number), 
                         output_processor = TakeFirst())
    
    number_of_owners = scrapy.Field(input_processor = MapCompose(get_number), 
                                    output_processor = TakeFirst())
    
    emission_scheme = scrapy.Field(output_processor = TakeFirst())
    
    vehicle_location_postcode = scrapy.Field(output_processor = TakeFirst())
    
    vehicle_location_latitude = scrapy.Field(input_processor = 
                                             MapCompose(get_latitude), 
                                             output_processor = TakeFirst())
    
    vehicle_location_longitude = scrapy.Field(input_processor = 
                                              MapCompose(get_longitude), 
                                              output_processor = TakeFirst())
    
    vehicle_registration_mark = scrapy.Field(output_processor = TakeFirst())
    
    derivative_id = scrapy.Field(output_processor = TakeFirst())
    
    condition = scrapy.Field(output_processor = TakeFirst())
    
    imported = scrapy.Field(output_processor = TakeFirst())
    
    average_mileage = scrapy.Field(output_processor = TakeFirst())
    
    mileage_deviation = scrapy.Field(output_processor = TakeFirst())
    
    mileage_deviation_type = scrapy.Field(output_processor = TakeFirst())
    
    ad_description = scrapy.Field(output_processor = TakeFirst())
    
    price = scrapy.Field(input_processor = MapCompose(strip_currency, 
                                                      clean_big_number), 
                                                      output_processor = 
                                                      TakeFirst())
    
    price_excluding_fees = scrapy.Field(input_processor = 
                                        MapCompose(strip_currency, 
                                                   clean_big_number), 
                                        output_processor = TakeFirst())
    
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
    
    co2_emission = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    tax = scrapy.Field(output_processor = TakeFirst())

    zero_to_sixty = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())

    zero_to_sixty_two = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())

    top_speed = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    cylinders = scrapy.Field(output_processor = TakeFirst())
    
    valves = scrapy.Field(output_processor = TakeFirst())
    
    engine_power = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    engine_torque = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    height = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    length = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    wheelbase = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    width = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    fuel_tank_capacity = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    gross_vehicle_weight = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    boot_space_seats_up = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    boot_space_seats_down = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    max_loading_weight = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    minimum_kerb_weight = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())

    urban = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    extra_urban = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    combined = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    co2_emissions = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    annual_tax = scrapy.Field(input_processor = MapCompose(get_number), 
                                 output_processor = TakeFirst())
    
    insurance_group = scrapy.Field(output_processor = TakeFirst())