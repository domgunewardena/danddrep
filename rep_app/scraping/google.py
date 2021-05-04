import os
import math
import requests
import json

import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import rep_app.scraping.restaurant_urls as restaurant_urls
import rep_app.scraping.postgresql as postgresql

from database import Database

class Google(Database):
    
    def __init__(self, method, driver):

        super().__init__('google')
        
        self.method = method
        self.driver = self.navigate_driver_to_google_maps(driver)
        
#       Authentication passwords
        self.refresh_token = os.environ['GMB_REFRESH_TOKEN']
        self.client_id = os.environ['GMB_CLIENT_ID']
        self.client_secret = os.environ['GMB_CLIENT_SECRET']
        self.redirect_uri = os.environ['GMB_REDIRECT_URI']
        
#       Database Variables
        self.current_ids = list(self.database['review_id'])
        
#       Authentication Variables  
        self.access_token = self.get_access_token()
        self.authentication_header = {'Authorization' : 'Bearer ' + self.access_token}
        self.account_id = '111855729671132001333'
        
        
    def get_access_token(self):
        
        url = 'https://www.googleapis.com/oauth2/v4/token'
        
        params = {
            'refresh_token' : self.refresh_token,
            'client_id': self.client_id,
            'client_secret' : self.client_secret,
            'redirect_uri' : self.redirect_uri,
            'grant_type' : 'refresh_token'
        }
        
        r = requests.post(
            url = url,
            params = params,
        )
        
        access_token = r.json()['access_token']
        
        return access_token
    
    
    def get_account_id(self):
        
        url = 'https://mybusiness.googleapis.com/v4/accounts'

        r = requests.get(
            url = url,
            headers = self.authentication_header,
        )
        
        account_id = r.json()['accounts'][0]['name'].replace('accounts/', '')

        return r.json()['accounts'][0]['name'].replace('accounts/', '')
    
    
    
    def get_location_dicts(self):
        
        url = 'https://mybusiness.googleapis.com/v4/accounts/' + self.account_id + '/locations'         
        
        r = requests.get(
            url = url,
            headers = self.authentication_header,
        )

        response = r.json()
        
        location_dicts = response['locations'].copy()        
    
        return location_dicts
    
    
    def navigate_driver_to_google_maps(self, driver):
        
        url = 'https://www.google.com/maps/'
        iframe_tag = 'iframe'
        agree_to_cookies_button_id = 'introAgreeButton'
        
        driver.get(url)
        
#         try:
#             iframe = WebDriverWait(driver, 10).until(
#                 EC.presence_of_element_located((By.TAG_NAME, iframe_tag))
#             )
#             driver.switch_to.frame(iframe)
            
#         except:
#             pass
            
#         try:
#             agree_to_cookies_button = WebDriverWait(driver, 10).until(
#                 EC.element_to_be_clickable((By.ID, agree_to_cookies_button_id))
#             )
#             agree_to_cookies_button.click()
#         except:
#             pass
        
        return driver
    
    
    def get_location_soup(self, driver, location_name):
        
        url = restaurant_urls.google_review_urls[location_name]
        sort_button_path = "//button[@data-value='Sort']"
        newest_button_path = '//li[@role=\'menuitemradio\'][2]'
        review_titles_class = 'section-review-titles'
        
        for _ in range(10):
            
            try:
                error = False
                print('Driver opening URL...')
                driver.get(url)
                print('Assigning sort button...')
                sort_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, sort_button_path)))
                
            except TimeoutException as err:
                error = str(err)
                
            if error:
                print("Exception has been thrown when trying to assign the sort button: " + error)
            else:
                break
        
        for _ in range(10):
            
            try:
                error = False
                print('Clicking sort button...')
                sort_button.click()
                print('Assigning newest button...')
                newest_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, newest_button_path)))
                
            except TimeoutException as err:
                error = str(err)
                
            if error:
                print("Exception has been thrown when trying to assign the newest button: " + error)
            else:
                break
                
        for _ in range(10):
            
            try:
                error = False
                print('Clicking newest button...')
                newest_button.click()
                print('Waiting for sorted reviews to load')
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, review_titles_class)))
                print('Saving soup...')
                soup = BeautifulSoup(driver.page_source, 'lxml')
                
            except TimeoutException as err:
                error = str(err)
                
            if error:
                print("Exception has been thrown when trying to load the sorted reviews: " + error)
            else:
                break
        
        return soup
    

    
#   'INNER' FUNCTIONS FOR GET REVIEWS
    
    def check_empty_restaurant(self, location_name):
            
        empty_restaurants = [
            'Almeida', 
            'Sauterelle',
            'Issho', 
            'Le Pont de La Tour Wine Merchant'
        ]

        return location_name in empty_restaurants

    def get_reviews_url(self, location_dict):

        location_reference = location_dict['name']
        url = 'https://mybusiness.googleapis.com/v4/' + location_reference + '/reviews'

        return url

    def get_first_response(self, url):

        r = requests.get(
            url = url,
            headers = self.authentication_header,
        )

        response = r.json()

        return response

    def get_later_response(self, url, next_page_token):

        r = requests.get(
            url = url,
            headers = self.authentication_header,
            params = {'pageToken':next_page_token}
        )

        response = r.json()

        return response

    def get_review_counts(self, response):

        reviews_count = response['totalReviewCount']
        pages_count = math.ceil(reviews_count/50)

        return reviews_count, pages_count
    
    def get_review_link(self, review, location_dict, location_soup):
        
        name_string = review['reviewer']['displayName']
        place_id = location_dict['locationKey']['placeId']
        contributor_link = [anchor_text.get('href') for anchor_text in location_soup.select('a') if name_string in anchor_text.text][0].split('reviews')[0]

        return contributor_link + 'place/' + place_id + '/'

    def add_reviews_to_master_list(self, response, location_dict, location_soup, new_reviews):

        reviews = response['reviews'].copy()
        location_name = location_dict['locationName']
        
        for review in reviews:

#           Conditional logic to skip review if it's in current database when collecting new reviews
            if self.method == 'new':
                review_id = review['reviewId']
                if review_id in self.current_ids:
                    continue

            review['location'] = location_name
            review['reviewer_display_name'] = review['reviewer']['displayName']
            
            try:
                review_link = self.get_review_link(review, location_dict, location_soup)
            except IndexError:
                review['link'] = restaurant_urls.google_review_urls[location_name]
            else:
                review['link'] = review_link
                
            try:
                del(review['reviewReply'])
            except:
                pass
            
            del(review['reviewer'])
            for key, value in postgresql.tables['rename_columns'][self.table].items():
                review[value] = review.pop(key)
                
            new_reviews.append(review)
    
#   END OF 'INNER' FUNCTIONS FOR GET REVIEWS  
    
    def get_reviews(self):
        
        self.location_dicts = self.get_location_dicts()
        master_list = []
        
        for location_dict in self.location_dicts:
            
            print('Getting ' + location_dict['locationName'] + "'s reviews...")
        
            url = self.get_reviews_url(location_dict)
            location_name = location_dict['locationName']
            location_soup = self.get_location_soup(self.driver, location_name)

            empty_restaurant = self.check_empty_restaurant(location_name)

            if empty_restaurant:
                continue

            response = self.get_first_response(url)
            reviews_count, pages_count = self.get_review_counts(response)
            self.add_reviews_to_master_list(response, location_dict, location_soup, master_list)

    #           Looping through review pages when collecting all reviews
            if self.method == 'all':
                while True:
                    try:
                        next_page_token = response['nextPageToken']
                    except KeyError:
                        break
                    else:
                        response = self.get_later_response(url, next_page_token)
                        self.add_reviews_to_master_list(response, location_dict, location_soup, master_list)

        return master_list    
    
    
#     UPDATING DATABASES
    
    def update_database(self):
        
        print('Google scraping started...')
        
        self.new_reviews = self.get_reviews()

        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)
        
        print('Google scraping finished')

    
    def add_reviews_to_csv(self, new_reviews):
        
        df = pd.DataFrame(new_reviews)
        
        try:
            df['comment']
        except KeyError:
            df['comment'] = None
            
        new_database = pd.concat(
            [
                self.database[self.column_names], 
                df[self.column_names]
            ], 
            ignore_index=True)
        
        new_database.to_csv('Google.csv', index=False)