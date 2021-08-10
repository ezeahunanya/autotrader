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

        il.add_value('advert_id', car_data.get('pageData').get('ods').get('advertId', np.nan))
        il.add_value('date_scraped', dt.now().date())
        il.add_value('time_scraped', dt.now().time())
        il.add_value('make', car_data.get('vehicle').get('make', np.nan))
        il.add_value('model', car_data.get('vehicle').get('model', np.nan))
        il.add_value('trim', car_data.get('vehicle').get('trim', np.nan))
        il.add_value('manufactured_year', car_data.get('vehicle').get('keyFacts').get('manufactured-year', np.nan))
        il.add_value('manufactured_year_identifier', car_data.get('vehicle').get('keyFacts').get('manufactured-year', np.nan))
        il.add_value('body_type', car_data.get('vehicle').get('keyFacts').get('body-type', np.nan))
        il.add_value('mileage', car_data.get('vehicle').get('keyFacts').get('mileage', np.nan))
        il.add_value('engine_size', car_data.get('vehicle').get('keyFacts').get('engine-size', np.nan))
        il.add_value('transmission', car_data.get('vehicle').get('keyFacts').get('transmission', np.nan))
        il.add_value('fuel_type', car_data.get('vehicle').get('keyFacts').get('fuel-type', np.nan))
        il.add_value('doors', car_data.get('vehicle').get('keyFacts').get('doors', np.nan))
        il.add_value('seats', car_data.get('vehicle').get('keyFacts').get('seats', np.nan))
        il.add_value('number_of_owners', car_data.get('vehicle').get('keyFacts').get('owners', np.nan))
        il.add_value('emission_scheme', car_data.get('vehicle').get('keyFacts').get('emission-scheme', np.nan))
        il.add_value('vehicle_location_postcode', car_data.get('vehicle').get('vehicleLocation', np.nan).get('postcode', np.nan))
        il.add_value('vehicle_location_latitude', car_data.get('vehicle').get('vehicleLocation', np.nan).get('latLong', np.nan))
        il.add_value('vehicle_location_longitude', car_data.get('vehicle').get('vehicleLocation', np.nan).get('latLong', np.nan))
        il.add_value('vehicle_registration_mark', car_data.get('vehicle').get('vrm', np.nan))
        il.add_value('derivative_id', car_data.get('vehicle').get('derivativeId', np.nan))
        il.add_value('condition', car_data.get('vehicle').get('condition', np.nan))
        il.add_value('imported', car_data.get('pageData').get('imported', np.nan))
        il.add_value('average_mileage', car_data.get('vehicle').get('mileageDeviation', np.nan).get('predictedMileage', np.nan))
        il.add_value('mileage_deviation', car_data.get('vehicle').get('mileageDeviation', np.nan).get('deviation', np.nan))
        il.add_value('mileage_deviation_type', car_data.get('vehicle').get('mileageDeviation', np.nan).get('type', np.nan))
        il.add_value('ad_description', car_data.get('advert').get('description', np.nan))
        il.add_value('price', car_data.get('advert').get('price', np.nan))
        il.add_value('price_excluding_fees', car_data.get('advert').get('priceExcludingFees', np.nan))
        il.add_value('no_admin_fees', car_data.get('advert').get('noAdminFees', np.nan))
        il.add_value('price_deviation', car_data.get('advert').get('marketAveragePriceDeviation', np.nan).get('deviation', np.nan))
        il.add_value('price_deviation_type', car_data.get('advert').get('marketAveragePriceDeviation', np.nan).get('type', np.nan))
        il.add_value('price_rating', car_data.get('advert').get('priceIndicator', np.nan).get('rating', np.nan))
        il.add_value('price_rating_label', car_data.get('advert').get('priceIndicator', np.nan).get('ratingLabel', np.nan))
        il.add_value('seller_name', car_data.get('seller').get('name', np.nan))
        il.add_value('seller_id', car_data.get('seller').get('id', np.nan))
        il.add_value('is_dealer_trusted', car_data.get('seller').get('isTrustedDealer', np.nan))
        il.add_value('seller_longlat', car_data.get('seller').get('longitude', np.nan))
        il.add_value('seller_segment', car_data.get('seller').get('segment', np.nan))
        il.add_value('seller_rating', car_data.get('seller').get('ratingStars', np.nan))
        il.add_value('total_reviews', car_data.get('seller').get('ratingTotalReviews', np.nan))
        il.add_value('seller_postcode', car_data.get('seller').get('location', np.nan).get('postcode', np.nan))
        il.add_value('seller_address_one', car_data.get('seller').get('location', np.nan).get('addressOne', np.nan))
        il.add_value('seller_address_two', car_data.get('seller').get('location', np.nan).get('addressTwo', np.nan))
        il.add_value('page_url', car_data.get('pageData').get('canonical', np.nan))
        il.add_value('number_of_photos', car_data.get('pageData').get('tracking').get('number_of_photos', np.nan))
        il.add_value('co2_emissions', car_data.get('vehicle').get('co2Emissions', np.nan))
        il.add_value('tax', car_data.get('vehicle').get('tax', np.nan))
        
        return il.load_item()