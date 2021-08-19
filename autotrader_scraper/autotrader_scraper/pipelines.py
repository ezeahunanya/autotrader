from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from autotrader_scraper.functions_module import get_dictionary_value as gdv
from autotrader_scraper.config import *


class AutotraderScraperPipeline:

    '''
    This class defines how an item from the spider is processed.
    '''

    config['raise_on_warnings'] = True
    config['use_pure'] = True
        
    DB_NAME = 'autotrader_adverts'
    TABLES = {}

    TABLES['vehicle_features'] = (
    "CREATE TABLE `vehicle_features` ("
    "  `advert_id` BIGINT,"
    "  `emission_scheme` text,"
    "  PRIMARY KEY (`advert_id`)"
    ") ENGINE=InnoDB")

    TABLES['sellers'] = (
    "CREATE TABLE `sellers` ("
    "  `advert_id` BIGINT,"
    seller_name
    seller_id
    is_dealer_trusted
    seller_longlat
    seller_segment
    seller_rating
    total_reviews
    seller_postcode
    seller_address_one
    seller_address_two
    "  `emission_scheme` text,"
    "  PRIMARY KEY (`advert_id`)"
    ") ENGINE=InnoDB")

    def __init__(self, **kwargs):
        self.cnx = self.mysql_connect()
        self.cursor = self.cnx.cursor()
        self.connect_to_database()
        self.create_tables()

    def open_spider(self, spider):
        print("spider open")
        
    def process_item(self, item, spider):
        print("Saving item into db ...")
        self.save_to_db(item)
        return item
    
    def close_spider(self, spider):
        self.mysql_close()
    
    def mysql_connect(self):
        '''
        
        '''

        try:
            print('Connecting to server...')
            return mysql.connector.connect(**config)
            

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def connect_to_database(self):
        '''
        
        '''

        try:
            self.cursor.execute("USE {}".format(self.DB_NAME))
            print("Database {} connected".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.DB_NAME))
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(self.cursor)
                print("Database {} created successfully.".format(self.DB_NAME))
                self.cursor.execute("USE {}".format(self.DB_NAME))
                print("Database {} selected.".format(self.DB_NAME))

            else:
                print(err)
                exit(1)
                
    def create_database(self):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'UTF8MB4'".format(self.DB_NAME))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_tables(self):
        '''
            
        '''

        for table in self.TABLES:
            table_description = self.TABLES[table]
            try:
                print("Creating table {}: ".format(table), end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")

   
    def save_to_db(self, item): 

        create_query = ("INSERT INTO autotrader_cars (advert_id, emission_scheme) VALUES (%s, %s)")
        
        val = (item['advert_id'], gdv(item, ['emission_scheme']))
        
        
        # Insert new row
        self.cursor.execute(create_query, val)
       

        # Make sure data is committed to the database
        self.cnx.commit()
        #print("Item saved with ID: {}" . format(lastRecordId)) 

    def mysql_close(self):
        self.cnx.close()

    #    '''CREATE TABLE autotrader_cars(
    #        advert_id int, date_scraped date
    #time_scraped = scrapy.Field()
    #make = scrapy.Field()
    #model = scrapy.Field()
    #trim = scrapy.Field()
    #manufactured_year = scrapy.Field()
    #manufactured_year_identifier = scrapy.Field()
    #body_type = scrapy.Field()
    #mileage = scrapy.Field()
    #engine_size = scrapy.Field()
    #transmission = scrapy.Field()
    #fuel_type = scrapy.Field()
    #doors = scrapy.Field()
    #seats = scrapy.Field()
    #number_of_owners = scrapy.Field()
    #emission_scheme = scrapy.Field()
    #vehicle_location_postcode = scrapy.Field()
    #vehicle_location_latitude = scrapy.Field()
    #vehicle_location_longitude = scrapy.Field()
    #vehicle_registration_mark = scrapy.Field()
    #derivative_id = scrapy.Field()
    #condition = scrapy.Field()
    #imported = scrapy.Field()
    #average_mileage = scrapy.Field()
    #mileage_deviation = scrapy.Field()
    #mileage_deviation_type = scrapy.Field()
    #ad_description = scrapy.Field()
    #price = scrapy.Field()
    #price_excluding_fees = scrapy.Field()
    #no_admin_fees = scrapy.Field()
    #price_deviation = scrapy.Field()
    #price_deviation_type = scrapy.Field()
    #price_rating = scrapy.Field()
    #price_rating_label = scrapy.Field()
    #seller_name = scrapy.Field()
    #seller_id = scrapy.Field()
    #is_dealer_trusted = scrapy.Field()
    #seller_longlat = scrapy.Field()
    #seller_segment = scrapy.Field()
    #seller_rating = scrapy.Field()
    #total_reviews = scrapy.Field()
    #seller_postcode = scrapy.Field()
    #seller_address_one = scrapy.Field()
    #seller_address_two = scrapy.Field()
    #page_url = scrapy.Field()
    #number_of_photos = scrapy.Field()
    #co2_emissions = scrapy.Field()
    #tax = scrapy.Field()
#
    #  `emp_no` int(11) NOT NULL AUTO_INCREMENT,
    #  `birth_date` date NOT NULL,
    # `first_name` varchar(14) NOT NULL,
    # `last_name` varchar(16) NOT NULL,
    #  `gender` enum('M','F') NOT NULL,
    # `hire_date` date NOT NULL,
    # PRIMARY KEY (`emp_no`)
    #) ENGINE=InnoDB")