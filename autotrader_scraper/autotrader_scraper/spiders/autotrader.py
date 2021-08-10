import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import re
import json
from autotrader_cars.items import AutotraderCarsItem
from scrapy.loader import ItemLoader
import numpy as np
from datetime import datetime as dt 

class AutotraderSpider(CrawlSpider):
    name = 'autotrader'
    allowed_domains = ['autotrader.co.uk']
    start_urls = ['''https://www.autotrader.co.uk/car-search?postcode=
                n14an&make=&include-delivery-option=on&advertising-location=at_cars&page=1''']

    rules = (
            # Extract links matching 'category.php' (but not matching 'subsection.php')
            # and follow links from them (since no callback means follow=True by default).
            Rule(LinkExtractor(allow=('/car-details/'), restrict_css=('li.search-page__result')), callback='parse_car', follow=True),
            )

    def parse_car(self, response):
        parsed_url = urlparse(response.url)
        advert_id = parsed_url.path.split('/')[-1]

        for item in response.css('script::text').getall():
            if re.search('window.AT.correlationId', item) != None:
                string = item
                partial_slug = re.search('\w+-\w+-\w+-\w+-\w+', string)[0]
                break
        
        car_details_api_endpoint = '''https://www.autotrader.co.uk/json/fpa/initial/{advert_id}?advertising
                                    -location=at_cars&guid={partial_slug}&include-delivery
                                    -option=on&onesearchad=New&onesearchad=Nearly%20New&onesearchad=Used&page=1&
                                    postcode=n14an&radius=1501&sort=relevance'''.format(advert_id=advert_id, partial_slug=partial_slug)
        
        yield scrapy.Request(car_details_api_endpoint, callback=self.parse_car_api)

    def parse_car_api(self, response):
        car_raw_data = response.text
        car_data = json.loads(car_raw_data)

        car_item = AutotraderCarsItem()
        il = ItemLoader(item=AutotraderCarsItem())

        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('date_scraped', dt.now().date())
        il.add_value('time_scraped', dt.now().time())
        il.add_value('make', car_data.get('vehicle').get('make', np.nan)
        il.add_value('model', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan)
        try:
            car_item['advert_id'] = car_data['pageData']['ods']['advertId']
        except:
            car_item['advert_id'] = np.nan
        
         
        car_item['date_scraped'] = dt.now().date()
        car_item['time_scraped'] = dt.now().time()

        try:    
            car_item['make'] = car_data['vehicle']['make']
        except:
            car_item['make'] = np.nan
            
        try:
            car_item['model'] = car_data['vehicle']['model']
        except:
            car_item['model'] = np.nan

        try:
            car_item['trim'] = car_data['vehicle']['trim']
        except:
            car_item['trim'] = np.nan

        try:    
            car_item['manufactured_year'] = re.search('\d{4}', car_data['vehicle']['keyFacts']['manufactured-year'])[0]
        except:
            car_item['manufactured_year'] = np.nan

        try:    
            car_item['manufactured_year_identifier'] = re.search('\(\d{2}', car_data['vehicle']['keyFacts']['manufactured-year'])[0].replace('(', '')
        except:
            car_item['manufactured_year_identifier'] = np.nan
        
        try:
            car_item['body_type'] = car_data['vehicle']['keyFacts']['body-type']
        except:
            car_item['body_type'] = np.nan
        
        try:
            car_item['mileage'] = car_data['vehicle']['keyFacts']['mileage'].replace(' miles', '').replace(',', '')
        except:
            car_item['mileage'] = np.nan

        try:
            car_item['engine_size'] = car_data['vehicle']['keyFacts']['engine-size'].replace('L', '')
        except:
            car_item['engine_size'] = np.nan
        
        try:
            car_item['transmission'] = car_data['vehicle']['keyFacts']['transmission']
        except:
            car_item['transmission'] = np.nan

        try:
            car_item['fuel_type'] = car_data['vehicle']['keyFacts']['fuel-type']
        except:
            car_item['fuel_type'] = np.nan

        try:
            car_item['doors'] = car_data['vehicle']['keyFacts']['doors'].replace(' doors', '')
        except:
            car_item['doors'] = np.nan

        try:
            car_item['seats'] = car_data['vehicle']['keyFacts']['seats'].replace(' seats', '')
        except:
            car_item['seats'] = np.nan

        try:
            car_item['number_of_owners'] = re.search('\d+', car_data['vehicle']['keyFacts']['owners'])[0]
        except:
            car_item['number_of_owners'] = np.nan

        try:
            car_item['emission_scheme'] = car_data['vehicle']['keyFacts']['emission-scheme']
        except:
            car_item['emission_scheme'] = np.nan

        try:
            car_item['vehicle_location_postcode'] = car_data['vehicle']['vehicleLocation']['postcode']
        except:
            car_item['vehicle_location_postcode'] = np.nan

        try:
            car_item['vehicle_location_latitude'] = car_data['vehicle']['vehicleLocation']['latLong'].split(',')[0]
        except:
            car_item['vehicle_location_latitude'] = np.nan

        try:
            car_item['vehicle_location_longitude'] = car_data['vehicle']['vehicleLocation']['latLong'].split(',')[1]
        except:
            car_item['vehicle_location_longitude'] = np.nan

        try:
            car_item['vehicle_registration_mark'] = car_data['vehicle']['vrm']
        except:
            car_item['vehicle_registration_mark'] = np.nan

        try:
            car_item['derivative_id'] = car_data['vehicle']['derivativeId']
        except:
            car_item['derivative_id'] = np.nan

        try:
            car_item['condition'] = car_data['vehicle']['condition']
        except:
            car_item['condition'] = np.nan

        try:
            car_item['imported'] = car_data['vehicle']['imported']
        except:
            car_item['imported'] = np.nan

        try:
            car_item['average_mileage'] = car_data['vehicle']['mileageDeviation']['predictedMileage']
        except:
            car_item['average_mileage'] = np.nan

        try:
            car_item['mileage_deviation'] = car_data['vehicle']['mileageDeviation']['deviation']
        except:
            car_item['mileage_deviation'] = np.nan

        try:
            car_item['mileage_deviation_type'] = car_data['vehicle']['mileageDeviation']['type']
        except:
            car_item['mileage_deviation_type'] = np.nan

        try:
            car_item['ad_description'] = car_data['advert']['description']
        except:
            car_item['ad_description'] = np.nan

        try:
            car_item['price'] = car_data['advert']['price'].replace('£', '').replace(',', '')
        except:
            car_item['price'] = np.nan

        try:
            car_item['price_excluding_fees'] = car_data['advert']['priceExcludingFees'].replace('£', '').replace(',', '')
        except:
            car_item['price_excluding_fees'] = np.nan

        try:
            car_item['no_admin_fees'] = car_data['advert']['noAdminFees']
        except:
            car_item['no_admin_fees'] = np.nan

        try:
            car_item['price_deviation'] = car_data['advert']['marketAveragePriceDeviation']['deviation']
        except:
            car_item['price_deviation'] = np.nan 
        
        try:
            car_item['price_deviation_type'] = car_data['advert']['marketAveragePriceDeviation']['type']
        except:
            car_item['price_deviation_type'] = np.nan

        try:
            car_item['price_rating'] = car_data['advert']['priceIndicator']['rating']
        except:
            car_item['price_rating'] = np.nan

        try:
            car_item['price_rating_label'] = car_data['advert']['priceIndicator']['ratingLabel']
        except:
            car_item['price_rating_label'] = np.nan
            
        try:
            car_item['seller_name'] = car_data['seller']['name']
        except:
            car_item['seller_name'] = np.nan
        
        try:
            car_item['seller_id'] = car_data['seller']['id']
        except:
            car_item['seller_id'] = np.nan

        try:
            car_item['is_dealer_trusted'] = car_data['seller']['isTrustedDealer']
        except:
            car_item['is_dealer_trusted'] = np.nan

        try:
            car_item['seller_longlat'] = car_data['seller']['longitude']
        except:
            car_item['seller_longlat'] = np.nan

        try:
            car_item['seller_segment'] = car_data['seller']['segment']
        except:
            car_item['seller_segment'] = np.nan
        
        try:
            car_item['seller_rating'] = car_data['seller']['ratingStars']
        except:
            car_item['seller_rating'] = np.nan

        try:
            car_item['total_reviews'] = car_data['seller']['ratingTotalReviews']
        except:
            car_item['total_reviews'] = np.nan

        try:
            car_item['seller_postcode'] = car_data['seller']['location']['postcode']
        except:
            car_item['seller_postcode'] = np.nan
        
        try:
            car_item['seller_address_one'] = car_data['seller']['location']['addressOne']
        except:
            car_item['seller_address_one'] = np.nan
        
        try:
            car_item['seller_address_two'] = car_data['seller']['location']['addressTwo']
        except:
            car_item['seller_address_two'] = np.nan

        try:
            car_item['page_url'] = car_data['pageData']['canonical']
        except:
            car_item['page_url'] = np.nan
        
        try:
            car_item['number_of_photos'] = car_data['pageData']['tracking']['number_of_photos']
        except:
            car_item['number_of_photos'] = np.nan
        
        try:
            car_item['co2_emissions'] = car_data['vehicle']['co2Emissions'].replace('g/km', '')
        except:
            car_item['co2_emissions'] = np.nan

        try:
            car_item['tax'] = car_data['vehicle']['tax']
        except:
            car_item['tax'] = np.nan

        return(car_item) 