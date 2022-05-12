from __future__ import print_function
import mysql.connector
from mysql.connector import errorcode
from autotrader_scraper.config import mysql_details
from autotrader_scraper.functions_module import get_dictionary_value as gdv

class AutotraderScraperPipeline:
    '''
    This class defines how an item from the spider is processed.
    '''

    mysql_details['raise_on_warnings'] = True
    mysql_details['use_pure'] = True
        
    DB_NAME = 'autotrader_adverts'
    TABLES = {}

    TABLES['sellers'] = (
    "CREATE TABLE `sellers` ("
    " `seller_id` INT,"
    " `seller_name` VARCHAR(255),"
    " `is_dealer_trusted` TINYINT(1),"
    " `seller_longlat` VARCHAR(255),"
    " `seller_segment` VARCHAR(255),"
    " `seller_rating` DECIMAL(2, 1),"
    " `total_reviews` INT,"
    " `region` VARCHAR(255),"
    " `county` VARCHAR(255),"
    " `town` VARCHAR(255),"
    " `country` VARCHAR(255),"
    " `seller_postcode` VARCHAR(255),"
    " `seller_address_one` VARCHAR(255),"
    " `seller_address_two` VARCHAR(255),"
    " `dealer_website` VARCHAR(255),"
    " `primary_contact_number` VARCHAR(255),"
    "  PRIMARY KEY (`seller_id`)"
    ") ENGINE=InnoDB"
    )

    TABLES['vehicle_features'] = (
    '''CREATE TABLE `vehicle_features` (
    `advert_id` BIGINT,
    `date_scraped` DATE,     
    `time_scraped` TIME,
    `make` VARCHAR(255),
    `model` VARCHAR(255),
    `trim` VARCHAR(255),
    `manufactured_year` YEAR,
    `manufactured_year_identifier` VARCHAR(255),
    `body_type` VARCHAR(255),
    `mileage` INT,
    `engine_size` DECIMAL(4, 2),
    `transmission` VARCHAR(255), 
    `fuel_type` VARCHAR(255),
    `doors` INT,
    `seats` INT,
    `number_of_owners` INT,
    `emission_scheme` VARCHAR(255),    
    `vehicle_location_postcode` VARCHAR(255), 
    `vehicle_location_latitude` DECIMAL(10, 7),
    `vehicle_location_longitude` DECIMAL(10, 7),    
    `vehicle_registration_mark` VARCHAR(255),
    `derivative_id` VARCHAR(255),
    `car_condition` VARCHAR(255),
    `imported` TINYINT(1),
    `average_mileage` INT,     
    `mileage_deviation` INT,  
    `mileage_deviation_type` VARCHAR(255),     
    `ad_description` TEXT,
    `price` INT,
    `price_excluding_fees` INT,    
    `no_admin_fees` TINYINT(1),
    `price_deviation` INT,    
    `price_deviation_type` VARCHAR(255),     
    `price_rating` VARCHAR(255),
    `price_rating_label` VARCHAR(255),
    `seller_id` INT,
    `page_url` VARCHAR(255),
    `number_of_photos` INT,
    `co2_emission` INT,
    `tax` INT,
    `zero_to_sixty` DECIMAL(3, 1),
    `zero_to_sixty_two` DECIMAL(3, 1),
    `top_speed` INT,
    `cylinders` INT,
    `valves` INT,     
    `engine_power` INT,    
    `engine_torque`  DECIMAL(6, 2), 
    `height` INT,    
    `length` INT,    
    `wheelbase` INT,    
    `width` INT,    
    `fuel_tank_capacity` DECIMAL(4, 1),
    `gross_vehicle_weight` INT,    
    `boot_space_seats_up` INT,    
    `boot_space_seats_down` INT,    
    `max_loading_weight` INT,    
    `minimum_kerb_weight` INT,
    `urban` DECIMAL(7, 2),
    `extra_urban` DECIMAL(7, 2),
    `combined` DECIMAL(7, 2),
    `co2_emissions` INT,
    `insurance_group` VARCHAR(255),
    PRIMARY KEY (`advert_id`),
    FOREIGN KEY(`seller_id`)
        REFERENCES `sellers` (`seller_id`) 
    ON DELETE CASCADE
    ) ENGINE=InnoDB'''
    )

    def __init__(self, **kwargs):
        self.cnx = self.mysql_connect()
        self.cursor = self.cnx.cursor()
        self.connect_to_database()
        self.create_tables()

    def open_spider(self, spider):
        print("spider open")
        
    def process_item(self, item, spider):
        '''
        Save items from spider into database.
        '''

        print("Saving item into db ...")
        self.save_to_db(item)
        return item
    
    def close_spider(self, spider):
        self.mysql_close()
    
    def mysql_connect(self):
        '''
        Connects to MYSQL server with credentials.
        '''

        try:
            print('Connecting to server...')
            return mysql.connector.connect(**mysql_details)
            

        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")

            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")

            else:
                print(err)

    def connect_to_database(self):
        '''
        Connects to database provided and creates if none exists.
        '''

        try:
            self.cursor.execute("USE {}".format(self.DB_NAME))
            print("Database {} connected".format(self.DB_NAME))

        except mysql.connector.Error as err:
            print("Database {} does not exists.".format(self.DB_NAME))

            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                print("Database {} created successfully.".format(self.DB_NAME))
                self.cursor.execute("USE {}".format(self.DB_NAME))
                print("Database {} selected.".format(self.DB_NAME))

            else:
                print(err)
                exit(1)
                
    def create_database(self):
        '''
        Creates database
        '''

        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'UTF8MB4'".format(self.DB_NAME))

        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    def create_tables(self):
        '''
        Create tables in database.  
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
        '''
        Save items into databse tables.
        ''' 
        insert_into_sellers = (
        '''INSERT INTO sellers
        (seller_id, seller_name, is_dealer_trusted, seller_longlat, 
        seller_segment, seller_rating, total_reviews, region, county, town, 
        country, seller_postcode, seller_address_one, seller_address_two, 
        dealer_website, primary_contact_number) 
        VALUES 
        (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
        )


        seller_values = (
        gdv(item, ['seller_id']), gdv(item, ['seller_name']), gdv(item, ['is_dealer_trusted']), gdv(item, ['seller_longlat']), 
        gdv(item, ['seller_segment']), gdv(item, ['seller_rating']), gdv(item, ['total_reviews']), gdv(item, ['region']), gdv(item, ['county']), gdv(item, ['town']), 
        gdv(item, ['country']), gdv(item, ['seller_postcode']), gdv(item, ['seller_address_one']), gdv(item, ['seller_address_two']), 
        gdv(item, ['dealer_website']), gdv(item, ['primary_contact_number'])
        )
                        
        try:
            self.cursor.execute(insert_into_sellers, seller_values)
        
        except mysql.connector.IntegrityError:
            pass
                
        insert_into_vehicle_features = (
        '''INSERT INTO vehicle_features 
        (advert_id, date_scraped, time_scraped, make, model, trim,
         manufactured_year, manufactured_year_identifier, body_type, mileage,
         engine_size, transmission, fuel_type, doors, seats, number_of_owners, 
         emission_scheme, vehicle_location_postcode, vehicle_location_latitude, 
         vehicle_location_longitude, vehicle_registration_mark, derivative_id, 
         car_condition, imported, average_mileage, mileage_deviation, 
         mileage_deviation_type, ad_description, price, price_excluding_fees, 
         no_admin_fees, price_deviation, price_deviation_type, price_rating, 
         price_rating_label, seller_id, page_url, number_of_photos, 
         co2_emission, tax, zero_to_sixty, zero_to_sixty_two, top_speed, 
         cylinders, valves, engine_power, engine_torque, height, length, 
         wheelbase, width, fuel_tank_capacity, gross_vehicle_weight, 
         boot_space_seats_up, boot_space_seats_down, max_loading_weight, 
         minimum_kerb_weight, urban, extra_urban, combined, co2_emissions, 
         insurance_group) 
         VALUES 
         (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
          %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'''
         )

        vehicle_feature_values = (
        gdv(item, ['advert_id']), gdv(item, ['date_scraped']), gdv(item, ['time_scraped']), gdv(item, ['make']), gdv(item, ['model']), gdv(item, ['trim']),
        gdv(item, ['manufactured_year']), gdv(item, ['manufactured_year_identifier']), gdv(item, ['body_type']), gdv(item, ['mileage']),
        gdv(item, ['engine_size']), gdv(item, ['transmission']), gdv(item, ['fuel_type']), gdv(item, ['doors']), gdv(item, ['seats']), gdv(item, ['number_of_owners']), 
        gdv(item, ['emission_scheme']), gdv(item, ['vehicle_location_postcode']), gdv(item, ['vehicle_location_latitude']), 
        gdv(item, ['vehicle_location_longitude']), gdv(item, ['vehicle_registration_mark']), gdv(item, ['derivative_id']), 
        gdv(item, ['condition']), gdv(item, ['imported']), gdv(item, ['average_mileage']), gdv(item, ['mileage_deviation']), 
        gdv(item, ['mileage_deviation_type']), gdv(item, ['ad_description']), gdv(item, ['price']), gdv(item, ['price_excluding_fees']), 
        gdv(item, ['no_admin_fees']), gdv(item, ['price_deviation']), gdv(item, ['price_deviation_type']), gdv(item, ['price_rating']), 
        gdv(item, ['price_rating_label']), gdv(item, ['seller_id']), gdv(item, ['page_url']), gdv(item, ['number_of_photos']), 
        gdv(item, ['co2_emission']), gdv(item, ['tax']), gdv(item, ['zero_to_sixty']), gdv(item, ['zero_to_sixty_two']), gdv(item, ['top_speed']), 
        gdv(item, ['cylinders']), gdv(item, ['valves']), gdv(item, ['engine_power']), gdv(item, ['engine_torque']), gdv(item, ['height']), gdv(item, ['length']), 
        gdv(item, ['wheelbase']), gdv(item, ['width']), gdv(item, ['fuel_tank_capacity']), gdv(item, ['gross_vehicle_weight']), 
        gdv(item, ['boot_space_seats_up']), gdv(item, ['boot_space_seats_down']), gdv(item, ['max_loading_weight']), 
        gdv(item, ['minimum_kerb_weight']), gdv(item, ['urban']), gdv(item, ['extra_urban']), gdv(item, ['combined']), gdv(item, ['co2_emissions']), 
        gdv(item, ['insurance_group'])
         )


        try:
            self.cursor.execute(insert_into_vehicle_features, vehicle_feature_values)
        
        except mysql.connector.IntegrityError:
            pass 
                
        self.cnx.commit()
        

    def mysql_close(self):
        '''
        Close MYSQL server connection.
        '''

        self.cnx.close()