import requests
import time
from datetime import date, timedelta

import pandas as pd

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException, ElementClickInterceptedException

from ...scraping import restaurant_urls

from .database import Database

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
        
#         if self.name == '100 Wardour Street Club':
#             clear_cookies(self.driver, 10)
        
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
            
            text = date_span.text
            
            if 'days ago' in text:
                days_ago = int(text.replace('Dined ','').replace(' days ago',''))
                dined_date = (date.today()-timedelta(days_ago)).strftime('%d %B %Y')
            else:
                dined_date = text.replace('Dined on ', '')
                
            return dined_date

        date_span = get_date_span(review_container)
        dined_date = get_date(date_span)

        return dined_date

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
            'id': self.name + '_' + name + '_' + review_text,
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
            try:
                review_dict = self.get_review_dict(review_container)
                if review_dict['id'] not in self.current_ids:
                    reviews.append(review_dict)
            except Exception as err:
                print('ERROR WHEN RETRIEVING REVIEW DICT: ' + str(err))
            
        return reviews
    
    
#     UPDATING DATABASES

    def update_database(self):
        
        print(self.name + "'s Opentable scraping started...")
        
        self.new_reviews = self.get_new_reviews()
        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)
        
        print(self.name + "'s Opentable scraping finished.")
        
        
    def create_database(self):
        
        print(self.name + "'s Opentable scraping started...")
        
        self.all_reviews = self.get_all_reviews()
        self.add_reviews_to_database(self.all_reviews)
        
        print(self.name + "'s Opentable scraping finished.")
        
    
    def add_new_reviews_to_csv(self, new_reviews):
        
        new_database = pd.concat([self.database[self.column_names],new_reviews[self.column_names]], ignore_index=True)
        new_database.to_csv('Opentable.csv', index=False)