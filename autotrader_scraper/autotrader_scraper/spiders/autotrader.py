import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlparse
import re
import json
from autotrader_scraper.items import AutotraderCarsItem
from scrapy.loader import ItemLoader
from datetime import datetime as dt 
from autotrader_scraper.functions_module import get_dictionary_value as gdv

class AutotraderSpider(CrawlSpider):
    '''
    Represent a spider object which will crawl autotrader webpages.

    Attributes
    ----------
    name: str
        name of the spider object
    allowed_domains: list, optional
        list of url strings which spider is allowed to crawl
    start_urls: list of str
        urls to make initial requests
    rules: list
        rule objects to define how spider crawls the web
    '''
    
    # start on autotrader.co.uk and get makes
    #request each of them 
    # if page count is lower than 100 proceed
    #if not get models and repeat
    # if page number higher than 100 get price range 
    
    name = 'autotrader'
    allowed_domains = ['autotrader.co.uk']
    start_urls = ['''https://www.autotrader.co.uk/car-search?postcode=n14an&make=&include-delivery-option=on&advertising-location=at_cars&page=1''']

    #def parse(self, repsonse):
    #makes = response.css('optgroup')[1]
    #response.css('optgroup')[1]
    #response.css('optgroup')[1].css('option')
    # response.css('optgroup')[1].css('option')[7].attrib['value']
    # 'https://www.autotrader.co.uk/car-search?postcode=n14an&make={VAUXHALL}&include-delivery-option=on&advertising-location=at_cars&page=1'
    #pagecount response.css('li.paginationMini__count')
    #total page count response.css('li.paginationMini__count').css('strong::text')[1].get()

    #iincluse why this function exist
    #if page_count > 100:
    #    find models...

    # model items response.css('div.sf-flyout__options.js-flyout-options')
    # each model response.css('div.sf-flyout__options.js-flyout-options').css('button').attrib['data-selected-value']
    # index after .css('button') so loop and reqeust
    # 'https://www.autotrader.co.uk/car-search?sort=relevance&postcode=n14an&radius=1500&make={VAUXHALL}&model={ADAM}&include-delivery-option=on'
    # same logic as before with pages counts above 100
    # if above>
    #





    rules = (
            Rule(LinkExtractor(allow = ('/car-details/'), 
            restrict_css = ('li.search-page__result')), 
            callback = 'parse_car', follow=True),

            Rule(LinkExtractor(restrict_css = ('a.paginationMini--right__active')), follow=True),
            )

    def parse_car(self, response):
        '''
        Yields a request for the api endpoint of an individual car 
        advertisement.
        '''
        
        parsed_url = urlparse(response.url)
        advert_id = parsed_url.path.split('/')[-1]

        for item in response.css('script::text').getall():
            if re.search('window.AT.correlationId', item) != None:
                string = item
                break
            
        correlation_id = re.search('\w+-\w+-\w+-\w+-\w+', string)[0]
        
        car_details_api_endpoint = '''https://www.autotrader.co.uk/json/fpa/initial/{advert_id}?advertising-location=at_cars&guid={correlation_id}&include-delivery-option=on&onesearchad=New&onesearchad=Nearly%20New&onesearchad=Used&page=1&postcode=n14an&radius=1501&sort=relevance'''\
                                    .format(advert_id=advert_id, correlation_id=correlation_id)
        
        yield scrapy.Request(car_details_api_endpoint, 
                             callback=self.parse_car_api)

    def parse_car_api(self, response):
        '''
        Returns a scrapy request for extra car specifications.
        '''

        car_raw_data = response.text
        car_data = json.loads(car_raw_data)

        il = ItemLoader(item=AutotraderCarsItem())
        il.add_value('advert_id', gdv(car_data, ['pageData', 
                                                       'ods', 'advertId']))
                                                       
        il.add_value('time_scraped', dt.now().time())
        
        il.add_value('date_scraped', dt.now().date())
        
        il.add_value('make', gdv(car_data, ['vehicle', 'make']))
        
        il.add_value('model', gdv(car_data, ['vehicle', 'model']))
        
        il.add_value('trim', gdv(car_data, ['vehicle', 'trim']))
        
        il.add_value('manufactured_year', 
                     gdv(car_data, ['vehicle', 'keyFacts', 
                                         'manufactured-year']))
        
        il.add_value('manufactured_year_identifier', 
                     gdv(car_data, ['vehicle', 'keyFacts', 
                                          'manufactured-year']))
        
        il.add_value('body_type', gdv(car_data, ['vehicle', 'keyFacts', 
                                                 'body-type']))
        
        il.add_value('mileage', gdv(car_data, ['vehicle', 'keyFacts', 
                                               'mileage']))
        
        il.add_value('engine_size', gdv(car_data, ['vehicle', 'keyFacts', 
                                                   'engine-size']))
        
        il.add_value('transmission', gdv(car_data, ['vehicle', 'keyFacts', 
                                          'transmission']))
        
        il.add_value('fuel_type', gdv(car_data, ['vehicle', 'keyFacts', 
                                          'fuel-type']))
        
        il.add_value('doors', gdv(car_data, ['vehicle', 'keyFacts', 'doors']))
        
        il.add_value('seats', gdv(car_data, ['vehicle', 'keyFacts', 'seats']))
        
        il.add_value('number_of_owners', gdv(car_data, ['vehicle', 'keyFacts', 
                                                        'owners']))
        
        il.add_value('emission_scheme', gdv(car_data, ['vehicle', 'keyFacts', 
                                                       'emission-scheme']))
        
        il.add_value('vehicle_location_postcode', 
                     gdv(car_data, ['vehicle', 'vehicleLocation', 'postcode']))
        
        il.add_value('vehicle_location_latitude', 
                     gdv(car_data, ['vehicle', 'vehicleLocation', 'latLong']))
        
        il.add_value('vehicle_location_longitude', 
                     gdv(car_data, ['vehicle', 'vehicleLocation', 'latLong']))
        
        il.add_value('vehicle_registration_mark', gdv(car_data, ['vehicle', 'vrm']))
        
        il.add_value('derivative_id', gdv(car_data, ['vehicle', 'derivativeId']))
        
        il.add_value('condition', gdv(car_data, ['vehicle', 'condition']))
        
        il.add_value('imported', gdv(car_data, ['vehicle', 'imported']))
        
        il.add_value('average_mileage', 
                     gdv(car_data, ['vehicle', 'mileageDeviation', 
                                    'predictedMileage']))
        
        il.add_value('mileage_deviation', 
                     gdv(car_data, ['vehicle', 'mileageDeviation', 'deviation']))
        
        il.add_value('mileage_deviation_type', 
                     gdv(car_data, ['vehicle', 'mileageDeviation', 'type']))
        
        il.add_value('ad_description', gdv(car_data, ['advert', 'description']))
        
        il.add_value('price', gdv(car_data, ['advert', 'price']))
        
        il.add_value('price_excluding_fees', 
                     gdv(car_data, ['advert', 'priceExcludingFees']))
        
        il.add_value('no_admin_fees', gdv(car_data, ['advert', 'noAdminFees']))
        
        il.add_value('price_deviation', 
                     gdv(car_data, ['advert', 'marketAveragePriceDeviation', 
                                    'deviation']))
        
        il.add_value('price_deviation_type', 
                     gdv(car_data, ['advert', 'marketAveragePriceDeviation', 
                                    'type']))
        
        il.add_value('price_rating', 
                     gdv(car_data, ['advert', 'priceIndicator', 'rating']))
        
        il.add_value('price_rating_label', 
                     gdv(car_data, ['advert', 'priceIndicator', 'ratingLabel']))
        
        il.add_value('seller_name', gdv(car_data, ['seller', 'name']))
        
        il.add_value('seller_id', gdv(car_data, ['seller', 'id']))
        
        il.add_value('is_dealer_trusted', 
                     gdv(car_data, ['seller', 'isTrustedDealer']))
        
        il.add_value('seller_longlat', gdv(car_data, ['seller', 'longitude']))
        
        il.add_value('seller_segment', gdv(car_data, ['seller', 'segment']))
        
        il.add_value('seller_rating', gdv(car_data, ['seller', 'ratingStars']))
        
        il.add_value('total_reviews', 
                     gdv(car_data, ['seller', 'ratingTotalReviews']))

        il.add_value('region', gdv(car_data, ['seller', 'location', 'region']))

        il.add_value('county', gdv(car_data, ['seller', 'location', 'county']))

        il.add_value('town', gdv(car_data, ['seller', 'location', 'town']))

        il.add_value('country', gdv(car_data, ['seller', 'location', 'country']))

        il.add_value('seller_postcode', 
                     gdv(car_data, ['seller', 'location', 'postcode']))
        
        il.add_value('seller_address_one', 
                     gdv(car_data, ['seller', 'location', 'addressOne']))
        
        il.add_value('seller_address_two', 
                     gdv(car_data, ['seller', 'location', 'addressTwo']))

        il.add_value('dealer_website', gdv(car_data, ['seller', 'dealerWebsite']))

        il.add_value('primary_contact_number', 
                     gdv(car_data, ['seller', 'primaryContactNumber']))
        
        il.add_value('page_url', gdv(car_data, ['pageData', 'canonical']))
        
        il.add_value('number_of_photos', 
                     gdv(car_data, ['pageData', 'tracking', 'number_of_photos']))
        
        il.add_value('co2_emission', gdv(car_data, ['vehicle', 'co2Emissions']))
        
        il.add_value('tax', gdv(car_data, ['vehicle', 'tax']))
        
        item = il.load_item()
        
        car_full_spec_api_endpoint = 'https://www.autotrader.co.uk/json/taxonomy/technical-specification?derivative={derivative_id}&channel=cars'\
                                     .format(derivative_id=gdv(item, ['derivative_id']) )

        yield scrapy.Request(car_full_spec_api_endpoint, 
                                 callback=self.parse_car_spec_api, 
                                 meta={'item': item})


    def parse_car_spec_api(self, response):
        '''
        Returns a car item for each advertisment with all the features
        '''
        
        car_specs_raw_data = response.text
        car_specs_data = json.loads(car_specs_raw_data)

        il2 = ItemLoader(item=response.meta['item'])
        
        dic = {}
        
        if car_specs_data != {}:
            for item in car_specs_data['techSpecs']:
                if item['specName'] == 'Performance':
                    for i in item['specs']:
                        name = str(i['name']).replace('0 - 60 mph', 'zero_to_sixty').replace('0 - 62 mph', 'zero_to_sixty_two').lower().replace(' ', '_')
                        value = i['value']
                        dic[name] = value

                elif item['specName'] == 'Dimensions':
                    for i in item['specs']:
                        name = str(i['name']).lower().replace(' ', '_').replace('(', '').replace(')', '')
                        value = i['value']
                        dic[name] = value

                elif item['specName'] == 'Running costs':
                    for i in item['specs']:
                        name = str(i['name']).lower().replace(' ', '_').replace('₂', '2')
                        value = i['value']
                        dic[name] = value

        
        il2.add_value('zero_to_sixty', gdv(dic, ['zero_to_sixty']))
        
        il2.add_value('zero_to_sixty_two', gdv(dic, ['zero_to_sixty_two']))
        
        il2.add_value('top_speed', gdv(dic, ['top_speed']))
        
        il2.add_value('cylinders', gdv(dic, ['cylinders']))
        
        il2.add_value('valves', gdv(dic, ['valves']))
        
        il2.add_value('engine_power', gdv(dic, ['engine_power']))
        
        il2.add_value('engine_torque', gdv(dic, ['engine_torque']))
        
        il2.add_value('height', gdv(dic, ['height']))
        
        il2.add_value('length', gdv(dic, ['length']))
        
        il2.add_value('wheelbase', gdv(dic, ['wheelbase']))
        
        il2.add_value('width', gdv(dic, ['width']))
        
        il2.add_value('fuel_tank_capacity', gdv(dic, ['fuel_tank_capacity']))
        
        il2.add_value('gross_vehicle_weight', gdv(dic, ['gross_vehicle_weight']))
        
        il2.add_value('boot_space_seats_up', gdv(dic, ['boot_space_seats_up']))
        
        il2.add_value('boot_space_seats_down', gdv(dic, ['boot_space_seats_down']))
        
        il2.add_value('max_loading_weight', gdv(dic, ['max_loading_weight']))
        
        il2.add_value('minimum_kerb_weight', gdv(dic, ['minimum_kerb_weight']))

        il2.add_value('urban', gdv(dic, ['urban']))

        il2.add_value('extra_urban', gdv(dic, ['extra_urban']))

        il2.add_value('combined', gdv(dic, ['combined']))

        il2.add_value('co2_emissions', gdv(dic, ['co2_emissions']))
        
        il2.add_value('insurance_group', gdv(dic, ['insurance_group']))
        
        item = il2.load_item()

        return item