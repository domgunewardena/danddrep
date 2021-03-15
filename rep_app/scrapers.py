import os
import math
import requests
import time
from datetime import datetime, date, timedelta

import json
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException

import rep_app.restaurant_urls as restaurant_urls
import rep_app.postgresql as postgresql

class Database():
    
    def __init__(self, table):
        
        self.postgres_host = os.environ['POSTGRESQL_HOST']
        self.postgres_database = os.environ['POSTGRESQL_DATABASE']
        self.postgres_user = os.environ['POSTGRESQL_USER']
        self.postgres_password = os.environ['POSTGRESQL_PASSWORD']
    
        self.table = table
        self.create_query = postgresql.tables['create_query'][table]
        self.select_query = 'SELECT * FROM ' + table
        self.column_names = postgresql.tables['columns'][table]
        self.database = self.to_dataframe()
#         self.csv = pd.read_csv(table.capitalize() + '.csv')
    
    def connect_to_database(self):
        
        return psycopg2.connect(
            host=self.postgres_host,
            database=self.postgres_database,
            user=self.postgres_user,
            password=self.postgres_password
        )
    
    def execute_query(self, query, commit_boolean):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute(query)
        
        if commit_boolean:
            conn.commit()

        cur.close()
        conn.close()
        
    def execute_query_with_value(self, query, value, commit_boolean):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute(query, value)
        
        if commit_boolean:
            conn.commit()

        cur.close()
        conn.close()
        
        
    def create(self):
        
        self.execute_query(self.create_query, True)
        
    def to_dataframe(self):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        
        cur.execute(self.select_query)
        tuples = cur.fetchall()
        cur.close()
        conn.close()
        
        return pd.DataFrame(tuples, columns=self.column_names)
    
    def upload_to_database(self, dataframe):
        
        engine_string = 'postgresql://' + self.postgres_user + ':' + self.postgres_password + '@' + self.postgres_host + '/' + self.postgres_database

        engine = create_engine(engine_string)
        con = engine.connect()

        dataframe.to_sql(
            self.table,
            con=con,
            index=False,
            if_exists='replace'
        )

        con.close()
        
    def add_reviews_to_database(self, new_reviews):
        
        for review in new_reviews:
            
            keys = review.keys()
            table = self.table
            columns = ', '.join(keys)
            values = ', '.join(['%({})s'.format(k) for k in keys])
            insert_query = 'INSERT INTO {0} ({1}) VALUES ({2});'.format(table, columns, values)
            
            self.execute_query_with_value(insert_query, review, True)
        

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
        
        try:
            iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.TAG_NAME, iframe_tag))
            )
            driver.switch_to.frame(iframe)
            
        except:
            pass
            
        try:
            agree_to_cookies_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, agree_to_cookies_button_id))
            )
            agree_to_cookies_button.click()
        except:
            pass
        
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
                print('Clicking sort button...')
                sort_button.click()
                
            except TimeoutException as err:
                error = str(err)
                
            if error:
                print("Exception has been thrown when trying to assign the sort button: " + error)
            else:
                break
        
        for _ in range(10):
            
            try:
                error = False
                print('Assigning newest button...')
                newest_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, newest_button_path)))
                print('Clicking newest button...')
                newest_button.click()
                
            except TimeoutException as err:
                error = str(err)
                
            if error:
                print("Exception has been thrown when trying to assign the newest button: " + error)
            else:
                break
                
        for _ in range(10):
            
            try:
                error = False
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
    
    
class Tripadvisor(Database):
    
    def __init__(self, restaurant, method):
        
        super().__init__('tripadvisor')
        
        self.method = method
        self.name = restaurant
        self.restaurant_urls = restaurant_urls.tripadvisor_urls
        self.current_ids = list(self.database['id'])
        
        self.home_url = self.restaurant_urls[self.name]
        self.home_soup = self.get_soup(self.home_url)
        
        
    def __str__(self):
        
        print(self.name + ' Tripadvisor')
        
        
    def get_current_ids(self):
        
        df = self.database
        return list(df[df['restaurant']==self.name]['id'])
    
    
    def get_soup(self, url):
        
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')
    
    
    def get_final_page(self, home_soup):
                
        return int(home_soup.select('.pageNum.last ')[0].text)
    
    
    def get_home_url_list(self, home_url, final_page):
        
        review_numbers_list = [x*10 for x in range(1,final_page)]
        home_url_split = home_url.split('Reviews-')
        
        first_half_url = home_url_split[0] + 'Reviews-'
        second_half_url = home_url_split[1]

        urls = [home_url]
        for num in review_numbers_list:
            full_url = first_half_url + 'or' + str(num) + '-' + second_half_url
            urls.append(full_url)

        return urls
    
#   GET REVIEW URLS 

#   'INNER' FUNCTIONS
    
    def get_reviews(self, soup):
        return soup.select('.reviewSelector')

    def get_id(self, review):
        return int(review['data-reviewid'])

    def get_review_url(self, review):

        def get_title(review):
            return review.select('.quote')[0]

        def get_anchor_text(title):
            return title.select('a')[0]

        def get_href(anchor):
            return anchor.get('href')

        slug = get_href(get_anchor_text(get_title(review)))
        link = 'https://www.tripadvisor.co.uk' + slug

        return link

    def add_review_urls_to_master_list(self, soup, review_urls):

        reviews = self.get_reviews(soup)
        for review in reviews:
#           Conditional logic for skipping review if already in current database when collecting new reviews
            if self.method == 'new':
                review_id = self.get_id(review)
                if review_id in self.current_ids:
                    continue
            link = self.get_review_url(review)
            review_urls.append(link)
    
#   END OF 'INNER' FUNCTIONS

    def get_review_urls(self):
                
        review_urls = []
        
        if self.method == 'all':
            for home_url in self.home_urls:
                soup = self.get_soup(home_url)
                self.add_review_urls_to_master_list(soup, review_urls)
        else:
            soup = self.home_soup
            self.add_review_urls_to_master_list(soup, review_urls)
            
        return review_urls
    
    
#   GENERATE REVIEW DICT 

#   'INNER' FUNCTIONS

    def get_id(self, review):
        return int(review['data-reviewid'])

    def get_link(self, review):
        href = review.select('.title')[0].get('href')
        return 'https://www.tripadvisor.co.uk' + href

    def get_title(self, review):
        title_string_class = '.noQuotes'
        return review.select(title_string_class)[0].text

    def get_date(self, review):
        dates_class = '.ratingDate'
        return review.select(dates_class)[0]['title']

    def get_visit_date(self, review):
        visit_date_class = '.prw_reviews_stay_date_hsx'
        return review.select(visit_date_class)[0].text[15:]

    def get_entry(self, review):
        text_class = '.entry'
        return review.select(text_class)[0].text.replace(' Show less', '')

    def get_scores(self, review):

        def get_scores_list(review):
            score_class = '.ui_bubble_rating'
            return review.select(score_class)

        def get_score(score):
            return int(score['class'][1][7])

        def get_sub_scores_list(review):
            sub_score_div_class = '.recommend-answer'
            return review.select(sub_score_div_class)

        def get_sub_score_name(sub_score_div):
            return sub_score_div.text

        def get_sub_score(sub_score_div):
            return get_score(get_scores_list(sub_score_div)[0])

        scores_list = get_scores_list(review)
        sub_scores_list = get_sub_scores_list(review)

        overall = get_score(scores_list[0])
        value = None
        service = None
        food = None

        for sub_score_div in sub_scores_list:

            sub_score_name = get_sub_score_name(sub_score_div)
            sub_score = get_sub_score(sub_score_div)

            if sub_score_name == 'Value':
                value = sub_score
            elif sub_score_name == 'Service':
                service = sub_score
            elif sub_score_name == 'Food':
                food = sub_score

        return overall, value, service, food

    def get_manager_response(self, review):

        response_class = '.mgrRspnInline'
        response_div = review.select(response_class)

        def get_response_text(response_div):

            response = ''
            for line in response_div[0].p.contents:
                if str(line) == '<br/>':
                    response += '\n'
                else:
                    response += line

            return response

        if response_div:
            return get_response_text(response_div)
        else:
            return None
        
#   END OF 'INNER' FUNCTIONS
    
    def generate_review_dict(self, review, url):

        review_id = self.get_id(review)
        review_title = self.get_title(review)
        review_date = self.get_date(review)
        visit_date = self.get_visit_date(review)
        review_entry = self.get_entry(review)
        score, value, service, food = self.get_scores(review)
        manager_response = self.get_manager_response(review)

        if url == 'home_url':
            review_link = self.get_link(review)
        else:
            review_link = url

        return {
            'id':review_id,
            'link':review_link,
            'restaurant':self.name,
            'title':review_title,
            'date':review_date,
            'visit_date':visit_date,
            'review':review_entry,
            'score':score,
            'value':value,
            'service':service,
            'food':food,
            'response':manager_response,
        }
    
    
#   GETTING REVIEWS
    
    def get_new_reviews(self):
        
        self.review_urls = self.get_review_urls()
        new_reviews = []  
        
        for review_url in self.review_urls:
            soup = self.get_soup(review_url)
            try:
                review = soup.select('.reviewSelector')[0]
            except:
                continue
            else:
                review_dict = self.generate_review_dict(review,review_url)
                new_reviews.append(review_dict)

        
        return new_reviews
    
    
#     UPDATING DATABASES
    
    def update_database(self):
        
        print(self.name + "'s Tripadvisor scraping started...")
        
        self.new_reviews = self.get_new_reviews()

        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)
            
        print(self.name + "'s Tripadvisor scraping finished.")
        
        
    def add_reviews_to_csv(self, new_reviews):
        
        new_reviews_df = pd.DataFrame(new_reviews)[self.column_names]
        new_database = self.database[self.column_names].append(new_reviews_df).drop_duplicates()
            
        new_database.to_csv('Tripadvisor.csv', index=False)
        
        return new_database
    
    

class Opentable(Database):
    
    def __init__(self,restaurant,driver):
        
        super().__init__('opentable')
        
        self.name = restaurant
        self.restaurant_urls = restaurant_urls.opentable_urls
        self.home_url = self.restaurant_urls[self.name]
        self.driver = driver
        
        self.current_ids = list(self.database['id'])
        
        self.home_soup = self.get_home_soup()
        self.open_home_soup = self.get_opened_home_soup()
        
    
    def get_home_soup(self):
        
        print('Getting home soup...')
        
        response = requests.get(self.home_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        return soup
    
    
    def get_final_page(self):
        
        print('Getting final page...')
        
        def get_page_buttons(soup):
            
            page_button_class = '.oc-reviews-b0c77e5f'
            
            return soup.select(page_button_class)[1:-1]
        
        def get_page_numbers(page_buttons):
            
            page_numbers = [int(page_button.text) for page_button in page_buttons]
            
            return page_numbers
        
        def get_final_page(page_numbers):
            
            return min(max(page_numbers),20)
        
        page_buttons = get_page_buttons(self.home_soup)
        page_numbers = get_page_numbers(page_buttons)
        try:
            final_page = get_final_page(page_numbers)
        except:
            final_page = 1

        return final_page
    
    
    def get_all_urls(self):
        
        print('Getting all urls...')
        
        self.final_page = self.get_final_page()
        
        base_url = self.home_url + '?page='
        page_nums = [x for x in range(1, self.final_page+1)]
        urls = [base_url + str(page_num) for page_num in page_nums]
        
        return urls

  
    def get_opened_soup(self,url):
        
        print('Getting opened soup...')
        
        def clear_cookies(driver, attempts):
            
            print('Clearing cookies...')
                
            cookie_button_id = 'onetrust-accept-btn-handler'
            
            for i in range(attempts):
            
                try:
                    error = False
                    cookie_button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, cookie_button_id)))
                    time.sleep(1)
                    cookie_button.click()

                except (TimeoutException,ElementClickInterceptedException) as err:
                    error = str(err)

                if error:
                    print('Exception has been thrown when trying to clear cookies on attempt ' + str(i+1) + ': '   + error)
                else:
                    break
            
        def click_read_more_buttons(driver):
            
            print('Clicking read more buttons...')
            
            more_buttons_class = 'reviewReadMore'
            displayed_style = 'display: block;'
            
            for i in range(10):
                try:
                    error = False
                    more_buttons = driver.find_elements_by_class_name('reviewReadMore')
                    for more_button in more_buttons:
                        style = more_button.get_attribute('style')
                        if style == displayed_style:
                            more_button.click()
                            
                except (StaleElementReferenceException,ElementNotInteractableException) as err:
                    error = str(err)
                    
                except ElementClickInterceptedException as err:
                    error = str(err)
                    print('Exception has been thrown when trying to click read more buttons on attempt ' + str(i+1) + ': '   + error)
                    clear_cookies(driver, 2)
                    
                if error:
                    time.sleep(1)
                else:
                    break
                    
        self.driver.get(url)            
        
        if self.name == '100 Wardour Street Club':
            clear_cookies(self.driver, 10)
        
        click_read_more_buttons(self.driver)
        
        page_source = self.driver.page_source
        soup = BeautifulSoup(page_source, 'lxml')
        
        return soup
    
    
    def get_all_opened_soups(self):
        
        soups = []
        self.urls = self.get_all_urls()
        for url in self.urls:
            soup = self.get_opened_soup(url)
            soups.append(soup)
            
        return soups
    
    
    def get_opened_home_soup(self):
        
        soup = self.get_opened_soup(self.home_url)
        
        return soup
        
        
    def get_review_containers(self, soup):
        
        print('Getting review containers...')

        review_container_class = '.reviewListItem'
        review_containers = soup.select(review_container_class)
        return review_containers
    
    
#   GET REVIEW DICT

#   INNER FUNCTIONS
    
    def get_name(self,review_container):

        name_div_class = '.oc-reviews-954a6007'
        name_div = review_container.select(name_div_class)
        name = name_div[0].text

        return name                

    def get_scores(self,review_container):

        def get_scores_div(review_container):

            scores_div_class = '.oc-reviews-0d90fee7'
            scores_div = review_container.select(scores_div_class)[0]

            return scores_div

        def get_score_spans(scores_div):

            score_span_class = '.oc-reviews-e3e61235'
            score_spans = scores_div.select(score_span_class)

            return score_spans

        def get_score(score_span):

            return int(score_span.text)

        scores_div = get_scores_div(review_container)
        score_spans = get_score_spans(scores_div)

        overall_score = get_score(score_spans[0])
        food_score = get_score(score_spans[1])
        service_score = get_score(score_spans[2])
        ambience_score = get_score(score_spans[3])

        return overall_score, food_score, service_score, ambience_score

    def get_dined_date(self,review_container):

        def get_date_span(review_container):

            date_span_class = '.oc-reviews-47b8de40'
            date_span = review_container.select(date_span_class)[0]

            return date_span

        def get_date(date_span):

            date = date_span.text.replace('Dined on ', '')
            return date

        date_span = get_date_span(review_container)
        date = get_date(date_span)

        return date

    def get_review_text(self,review_container):

        review_div_class = '.reviewBodyContainer'
        review_text = review_container.select(review_div_class)[0].text

        return review_text
    
#   END OF REVIEW DICT INNER FUNCTIONS
    
    def get_review_dict(self, review_container):
        
        yesterday = date.today()-timedelta(1)
        yesterday_string = yesterday.strftime('%Y-%m-%d')
        
        name = self.get_name(review_container)
        overall,food,service,ambience = self.get_scores(review_container)
        dined_date = self.get_dined_date(review_container)
        review_text = self.get_review_text(review_container)

        review_dict = {
            'restaurant': self.name,
            'name': name,
            'overall_score': overall,
            'food_score': food,
            'service_score': service,
            'ambience_score': ambience,
            'date': yesterday,
            'dined_date': dined_date,
            'review_text': review_text,
            'id': self.name + '_' + name + '_' + dined_date,
            'link':self.home_url
        }

        return review_dict
    
    
#   GET REVIEWS
    
    def get_all_reviews(self):
        
        soups = self.get_all_opened_soups()
        reviews = []
        
        for soup in soups:            
            review_containers = self.get_review_containers(soup)            
            for review_container in review_containers:
                print('Getting review dicts...')
                review_dict = self.get_review_dict(review_container)
                reviews.append(review_dict)
                    
        return reviews
    
    
    def get_first_page_reviews(self):
        
        reviews = []
        review_containers = self.get_review_containers(self.open_home_soup)  
        
        for review_container in review_containers:                
            review_dict = self.get_review_dict(review_container)
            reviews.append(review_dict)
            
        return reviews
    
    
    def get_new_reviews(self):
        
        reviews = []
        review_containers = self.get_review_containers(self.open_home_soup)  
        
        for review_container in review_containers:                
            review_dict = self.get_review_dict(review_container)
            if review_dict['id'] not in self.current_ids:
                reviews.append(review_dict)
            
        return reviews
    
    
#     UPDATING DATABASES

    def update_database(self):
        
        print(self.name + "'s Opentable scraping started...")
        
        self.new_reviews = self.get_new_reviews()
        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)
        
        print(self.name + "'s Opentable scraping finished.")
        

    
    def add_new_reviews_to_csv(self, new_reviews):
        
        new_database = pd.concat([self.database[self.column_names],new_reviews[self.column_names]], ignore_index=True)
        new_database.to_csv('Opentable.csv', index=False)
        
        
class SevenRooms(Database):
    
    def __init__(self, start_date, end_date):
        
        super().__init__('sevenrooms')
        
        self.start_date = start_date
        self.end_date = end_date
    
        self.client_id = os.environ['SR_CLIENT_ID']
        self.client_secret = os.environ['SR_CLIENT_SECRET']
        self.venue_group_id = os.environ['SR_VENUE_GROUP_ID']
    
    def get_token(self):

        url = "https://api.sevenrooms.com/2_2/auth"
        headers = {'Content-type': 'application/json'}

        parameters = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        r = requests.post(
            url,
            headers=headers,
            params=parameters
        )

        return r.json()['data']['token']

    def get_venue_ids(self):
        
        self.token = self.get_token()

        url = "https://api.sevenrooms.com/2_2/venues"
        headers = {'authorization': self.token}

        parameters = {
            'venue_group_id' : self.venue_group_id,
            'limit':100
        }

        r = requests.get(
            url,
            headers=headers,
            params=parameters
        )

        restaurant_ids_df = pd.DataFrame(r.json()["data"]["results"])[["id","name"]]
        restaurant_ids_df.columns = ["venue_id","restaurant"]

        return restaurant_ids_df
    
    def get_reviews(self):
        
        def americanise_date(date_string):
            return date_string[3:5] + '-' + date_string[:2] + '-' + date_string[6:]
        
        def generate_reservation_url(restaurant_id, americanised_reservation_date, reservation_id):
            return 'https://www.sevenrooms.com/manager/' + restaurant_id + '/reservations/day/' + americanised_reservation_date +  '?actual_id=' +  reservation_id
        
        def numericize_scores(review):
            
            score_strings = ['overall','food','service','ambience']
            for score_string in score_strings:
                review[score_string] = int(review[score_string])
            
            return review
        
        self.restaurant_ids_df = self.get_venue_ids()
        venue_ids = list(self.restaurant_ids_df['venue_id'])
        reviews = []
        
        for venue_id in venue_ids:

            mask = self.restaurant_ids_df['venue_id'] == venue_id
            restaurant = list(self.restaurant_ids_df[mask]['restaurant'])[0]
            
            if restaurant == 'The Secret Garden':
                continue
            
            print('Getting ' + restaurant + "'s reviews")
            url = "https://api.sevenrooms.com/2_2/venues/" + venue_id + '/feedback'

            headers = {'authorization':self.token}

            parameters = {
                'start_date': self.start_date,
                'end_date': self.end_date,
            }

            r = requests.get(
                url,
                headers = headers,
                params = parameters
            )

            try:
                review_dicts = r.json()['data']['reservation_feedback']
            except:
                continue
            else:
                for review in review_dicts:
                    
                    link_date_string = americanise_date(review['reservation_date'])
                    reservation_id = review['reservation_id']
                    restaurant_id = restaurant_urls.sevenrooms_url_restaurant_ids[restaurant]
                    reservation_url = generate_reservation_url(restaurant_id, link_date_string, reservation_id)
                    
                    review['link'] = reservation_url
                    review['restaurant'] = restaurant
                    review['restaurant_id'] = venue_id
                    review = numericize_scores(review)
                    
                    reviews.append(review)
                    
        return reviews
    
    
#     UPDATING DATABASES
    
    def update_database(self):
    
        print('Fetching SevenRooms reviews...')
        
        self.new_reviews = self.get_reviews()

        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)
    
        print('SevenRooms finished')
            
            
            
class Reviews(Database):
    
    def __init__(self):
        
        super().__init__('reviews')
       
        
    def table_to_dataframe(self,table):
        
        select_query = 'SELECT * FROM ' + table
        columns = postgresql.tables['columns'][table]
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        
        cur.execute(select_query)
        tuples = cur.fetchall()
        cur.close()
        conn.close()
        
        return pd.DataFrame(tuples, columns=columns)
    
    
    def get_tripadvisor_reviews(self):
        
        def turn_id_to_string(df):
            
            df['id'] = df['id'].apply(str)
            return df
        
        def add_source(df):
            
            df['source'] = 'Tripadvisor'
            return df
        
        current_df = self.table_to_dataframe('tripadvisor')
        
        df = add_source(
            turn_id_to_string(
                current_df
            )
        )
        
        return df
    
    
    def get_opentable_reviews(self):
        
        def add_source(df):
            
            df['source'] = 'Opentable'
            return df
        
        def add_date(df):
            
            df['date'] = df['dined_date']
            return df
        
        def rename_columns(df):
            
            rename_columns_map = postgresql.tables['to_master_database_maps']['rename_columns']['opentable']
            return df.rename(columns=rename_columns_map)
            return df
            
        def map_restaurants(df):
            
            restaurant_map = postgresql.tables['to_master_database_maps']['restaurant']['opentable']
            df['restaurant'] = df['restaurant'].map(restaurant_map)
            return df
        
        current_df = self.table_to_dataframe('opentable')
        
        df = map_restaurants(
            rename_columns(
                add_date(
                    add_source(
                        current_df
                    )
                )
            )
        )
        
        return df
    
    
    def get_google_reviews(self):
        
        def rename_columns(df):
            
            rename_columns_map = postgresql.tables['to_master_database_maps']['rename_columns']['google']
            return df.rename(columns=rename_columns_map)
        
        def add_source(df):
            
            df['source'] = 'Google'
            return df
        
        def turn_scores_to_numbers(df):
            
            score_map = {
                'FIVE':5,
                'FOUR':4,
                'THREE':3,
                'TWO':2,
                'ONE':1
            }
            
            df['score'] = df['score'].map(score_map)
            return df
        
        def format_dates(df):
            
            def remove_first_0(date_string):
                return date_string[1:] if date_string[0] == '0' else date_string
            
            df['date'] = pd.to_datetime(df['date'].str[:10]).dt.strftime('%d %B %Y').apply(str).apply(remove_first_0)
            return df
        
        def map_restaurants(df):
            
            restaurant_map = postgresql.tables['to_master_database_maps']['restaurant']['google']
            df['restaurant'] = df['restaurant'].map(restaurant_map)
            return df
        
        current_df = self.table_to_dataframe('google')
            
        df = map_restaurants(
            format_dates(
                turn_scores_to_numbers(
                    add_source(
                        rename_columns(
                            current_df
                        )
                    )
                )
            )
        )
        
        return df
    
    
    def get_sevenrooms_reviews(self):
        
        def rename_columns(df):
            
            rename_columns_map = postgresql.tables['to_master_database_maps']['rename_columns']['sevenrooms']
            return df.rename(columns=rename_columns_map)
        
        def add_source(df):
            
            df['source'] = 'SevenRooms'
            return df
            
        def map_restaurants(df):
            
            restaurant_map = postgresql.tables['to_master_database_maps']['restaurant']['sevenrooms']
            df['restaurant'] = df['restaurant'].map(restaurant_map)
            return df
        
        current_df = self.table_to_dataframe('sevenrooms')
        
        df = map_restaurants(
            add_source(
                rename_columns(
                    current_df
                )
            )
        )
        
        return df
    
        
    def get_new_database(self):
        
        self.tripadvisor_df = self.get_tripadvisor_reviews()
        self.opentable_df = self.get_opentable_reviews()
        self.google_df = self.get_google_reviews()
        self.sevenrooms_df = self.get_sevenrooms_reviews()
        self.columns = postgresql.tables['columns']['reviews']
        
        tripadvisor_opentable = pd.merge(
            left = self.tripadvisor_df,
            right = self.opentable_df,
            how = 'outer'
        )
        
        tripadvisor_opentable_google_df = pd.merge(
            left = tripadvisor_opentable,
            right = self.google_df,
            how = 'outer'
        )
        
        all_df = pd.merge(
            left = tripadvisor_opentable_google_df,
            right = self.sevenrooms_df,
            how = 'outer'
        )
        
        df = all_df[self.columns]
        
        df['date'] = pd.to_datetime(df['date'])
        df['review'] = df['review'].fillna('')
        
        score_strings = ['score','food','service','value','ambience']
        for string in score_strings:
            df[string] = df[string].fillna(0)
        
        return df
    
    
    def get_new_reviews(self):
        
        self.new_database = self.get_new_database()
        
        df = pd.merge(
            left = self.new_database,
            right = self.database,
            how = 'left',
            indicator = True
        )
        
        new_reviews_df = df[df['_merge']=='left_only'][self.columns]
        
        return new_reviews_df.to_dict('records')
    
    
    def update_database(self):
        
        self.new_reviews = self.get_new_reviews()
        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)