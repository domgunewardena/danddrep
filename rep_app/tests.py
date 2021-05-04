from django.test import TestCase

from datetime import date, timedelta
import os

from rep_app.models import Review, Restaurant
from rep_app.restaurant_list import restaurant_dict

from rep_app.scraping.scrapers import Google, Tripadvisor, Opentable, SevenRooms, Reviews
import rep_app.scraping.restaurant_urls as restaurant_urls

from selenium import webdriver

# Create your tests here.
        
def open_driver():
    
    CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
    chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_bin
    options.add_argument(' — disable-gpu')
    options.add_argument(' — no-sandbox')
    options.add_argument(' — headless')
    options.add_argument('--disable-dev-shm-usage')

    return webdriver.Chrome(
        executable_path=CHROMEDRIVER_PATH, 
        chrome_options=options
    )

driver = open_driver()

class GoogleTests(TestCase):
    
    google = Google('new', driver)
    bluebird_location_dict = test_results.google_location_dicts[0]
    bluebird_reviews_url = 'https://mybusiness.googleapis.com/v4/accounts/111855729671132001333/locations/8494375825452078058/reviews'
    bluebird_location_name = 'Bluebird Chelsea'
    3
    
#   TEST DATABASE
    
    def test_database_columns(self):
        
        database_columns = [
            'location',
            'name',
            'review_id',
            'reviewer_display_name',
            'star_rating',
            'comment',
            'create_time',
            'update_time',
            'link'
        ]
        
        result = list(self.google.database.columns)
        
        self.assertEqual(result, database_columns)
        
    def test_database_length(self):
        
        result = len(self.google.database)
        
        self.assertGreater(result,0)
        
#   TEST INFO FUNCTIONS
    
    def test_get_account_id(self):
        
        result = self.google.get_account_id()
        account_id = '111855729671132001333'
        
        self.assertEqual(result, account_id)
        
    def test_get_location_dicts(self):
        
        location_dict_keys = [
            'name',
            'storeCode',
            'locationName',
            'primaryPhone',
            'primaryCategory',
            'additionalCategories',
            'websiteUrl',
            'regularHours',
            'locationKey',
            'additionalPhones',
            'latlng',
            'openInfo',
            'locationState',
            'attributes',
            'metadata',
            'languageCode',
            'address',
            'profile'
        ]
        
        result = list(self.google.get_location_dicts()[0])
        
        self.assertEqual(result, location_dict_keys)
        
#   TEST REVIEW FUNCTIONS
        
    def test_check_empty_restaurant(self):
        
        empty_restaurant = 'Almeida'
        full_restaurant = 'Skylon'
        
        result1 = self.google.check_empty_restaurant(empty_restaurant)
        result2 = self.google.check_empty_restaurant(full_restaurant)
        
        self.assertTrue(result1)
        self.assertFalse(result2)
        
    def test_get_reviews_url(self):
        
        result = self.google.get_reviews_url(self.bluebird_location_dict)
        
        self.assertEqual(result, self.bluebird_reviews_url)
        
    def test_get_first_response(self):
        
        response_keys = [
            'reviews', 
            'averageRating', 
            'totalReviewCount', 
            'nextPageToken'
        ]
        
        result = list(self.google.get_first_response(self.bluebird_reviews_url).keys())
        
        self.assertEqual(result, response_keys)
        
    def test_get_first_response_returns_reviews_dict(self):
        
        reviews_dict_keys = [
            'reviewId',
             'reviewer',
             'starRating',
             'comment',
             'createTime',
             'updateTime',
             'name'
        ]
        
        result = list(self.google.get_first_response(self.bluebird_reviews_url)['reviews'][0].keys())
        
        self.assertEqual(result, reviews_dict_keys)
    
    