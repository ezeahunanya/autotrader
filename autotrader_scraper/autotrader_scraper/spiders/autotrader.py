import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import re
import json
from autotrader_scraper.items import AutotraderCarsItem
from scrapy.loader import ItemLoader
import numpy as np
from datetime import datetime as dt 

def get_value(dictionary, *keys):
        for key in keys:
            try:
                dictionary = dictionary[key]
            except KeyError:
                dictionary = np.nan
                break          
        return dictionary

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

        il = ItemLoader(item=AutotraderCarsItem())
        il.add_value('advert_id', get_value(car_data, 'pageData', 'ods', 'advertId'))
        il.add_value('date_scraped', dt.now().date())
        il.add_value('time_scraped', dt.now().time())
        il.add_value('make', get_value(car_data, 'vehicle', 'make'))
        il.add_value('model', get_value(car_data, 'vehicle', 'model'))
        il.add_value('trim', get_value(car_data, 'vehicle', 'trim'))
        il.add_value('manufactured_year', get_value(car_data, 'vehicle', 'keyFacts', 'manufactured-year'))
        il.add_value('manufactured_year_identifier', get_value(car_data, 'vehicle', 'keyFacts', 'manufactured-year'))
        il.add_value('body_type', get_value(car_data, 'vehicle', 'keyFacts', 'body-type'))
        il.add_value('mileage', get_value(car_data, 'vehicle', 'keyFacts', 'mileage'))
        il.add_value('engine_size', get_value(car_data, 'vehicle', 'keyFacts', 'engine-size'))
        il.add_value('transmission', get_value(car_data, 'vehicle', 'keyFacts', 'transmission'))
        il.add_value('fuel_type', get_value(car_data, 'vehicle', 'keyFacts', 'fuel-type'))
        il.add_value('doors', get_value(car_data, 'vehicle', 'keyFacts', 'doors'))
        il.add_value('seats', get_value(car_data, 'vehicle', 'keyFacts', 'seats'))
        il.add_value('number_of_owners', get_value(car_data, 'vehicle', 'keyFacts', 'owners'))
        il.add_value('emission_scheme', get_value(car_data, 'vehicle', 'keyFacts', 'emission-scheme'))
        il.add_value('vehicle_location_postcode', get_value(car_data, 'vehicle', 'vehicleLocation', 'postcode'))
        il.add_value('vehicle_location_latitude', get_value(car_data, 'vehicle', 'vehicleLocation', 'latLong'))
        il.add_value('vehicle_location_longitude', get_value(car_data, 'vehicle', 'vehicleLocation', 'latLong'))
        il.add_value('vehicle_registration_mark', get_value(car_data, 'vehicle', 'vrm'))
        il.add_value('derivative_id', get_value(car_data, 'vehicle', 'derivativeId'))
        il.add_value('condition', get_value(car_data, 'vehicle', 'condition'))
        il.add_value('imported', get_value(car_data, 'vehicle', 'imported'))
        il.add_value('average_mileage', get_value(car_data, 'vehicle', 'mileageDeviation', 'predictedMileage'))
        il.add_value('mileage_deviation', get_value(car_data, 'vehicle', 'mileageDeviation', 'deviation'))
        il.add_value('mileage_deviation_type', get_value(car_data, 'vehicle', 'mileageDeviation', 'type'))
        il.add_value('ad_description', get_value(car_data, 'advert', 'description'))
        il.add_value('price', get_value(car_data, 'advert', 'price'))
        il.add_value('price_excluding_fees', get_value(car_data, 'advert', 'priceExcludingFees'))
        il.add_value('no_admin_fees', get_value(car_data, 'advert', 'noAdminFees'))
        il.add_value('price_deviation', get_value(car_data, 'advert', 'marketAveragePriceDeviation', 'deviation'))
        il.add_value('price_deviation_type', get_value(car_data, 'advert', 'marketAveragePriceDeviation', 'type'))
        il.add_value('price_rating', get_value(car_data, 'advert', 'priceIndicator', 'rating'))
        il.add_value('price_rating_label', get_value(car_data, 'advert', 'priceIndicator', 'ratingLabel'))
        il.add_value('seller_name', get_value(car_data, 'seller', 'name'))
        il.add_value('seller_id', get_value(car_data, 'seller', 'id'))
        il.add_value('is_dealer_trusted', get_value(car_data, 'seller', 'isTrustedDealer'))
        il.add_value('seller_longlat', get_value(car_data, 'seller', 'longitude'))
        il.add_value('seller_segment', get_value(car_data, 'seller', 'segment'))
        il.add_value('seller_rating', get_value(car_data, 'seller', 'ratingStars'))
        il.add_value('total_reviews', get_value(car_data, 'seller', 'ratingTotalReviews'))
        il.add_value('seller_postcode', get_value(car_data, 'seller', 'location', 'postcode'))
        il.add_value('seller_address_one', get_value(car_data, 'seller', 'location', 'addressOne'))
        il.add_value('seller_address_two', get_value(car_data, 'seller', 'location', 'addressTwo'))
        il.add_value('page_url', get_value(car_data, 'pageData', 'canonical'))
        il.add_value('number_of_photos', get_value(car_data, 'pageData', 'tracking', 'number_of_photos'))
        il.add_value('co2_emissions', get_value(car_data, 'vehicle', 'co2Emissions'))
        il.add_value('tax', get_value(car_data, 'vehicle', 'tax'))
        
        return il.load_item()