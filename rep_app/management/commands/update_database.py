from datetime import date, timedelta
import os

from django.core.management.base import BaseCommand, CommandError
from rep_app.models import Review, Restaurant

from rep_app.scrapers import Google, Tripadvisor, Opentable, SevenRooms, Reviews
from rep_app.restaurant_list import restaurant_dict
import rep_app.restaurant_urls as restaurant_urls

from selenium import webdriver

class Command(BaseCommand):
    
    help = 'Create review objects from all reviews in database'
    
    def handle(self, *args, **options):
        
        def open_driver():
            
            CHROMEDRIVER_PATH = '/app/.chromedriver/bin/chromedriver'
            chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
            options = webdriver.ChromeOptions()
            options.binary_location = chrome_bin
            options.add_argument(' — disable-gpu')
            options.add_argument(' — no-sandbox')
            options.add_argument(' — headless')
    
            return webdriver.Chrome(
                executable_path=CHROMEDRIVER_PATH, 
                chrome_options=options
            )

        def update_Google(driver):
            
            self.stdout.write(self.style.SUCCESS('Google scraping started...'))

            google = Google('new', driver)
            google.update_database()
            
            self.stdout.write(self.style.SUCCESS('Google scraping finished'))

        def update_Tripadvisor():

            self.stdout.write(self.style.SUCCESS('Tripadvisor scraping started...'))

            for restaurant in restaurant_urls.tripadvisor_urls.keys():
                tripadvisor = Tripadvisor(restaurant, 'new')
                tripadvisor.update_database()

            self.stdout.write(self.style.SUCCESS('Tripadvisor scraping finished'))

        def update_Opentable(driver):

            self.stdout.write(self.style.SUCCESS('Opentable scraping started...'))

            for restaurant in restaurant_urls.opentable_urls.keys():
                opentable = Opentable(restaurant, driver)
                opentable.update_database()

            self.stdout.write(self.style.SUCCESS('Opentable scraping finished'))

        def update_SevenRooms():

            today_string = date.today().strftime('%Y-%m-%d')
            yesterday_string = (date.today()-timedelta(1)).strftime('%Y-%m-%d')
            
            self.stdout.write(self.style.SUCCESS('Sevenrooms scraping started...'))

            sr = SevenRooms(yesterday_string,today_string)
            sr.update_database()
            
            self.stdout.write(self.style.SUCCESS('SevenRooms scraping finished'))
            
        def get_restaurant_id(restaurant_string):
            
            try:
                return int(restaurant_dict[restaurant_string]['id'])
            except:
                return None
            
        try:            
            driver = open_driver()
            update_Google(driver)
            update_Tripadvisor()
            update_Opentable(driver)
            update_SevenRooms()
            
            reviews = Reviews()
            reviews.update_database()
            
            for new_review in reviews.new_reviews:
                
                restaurant_id = get_restaurant_id(new_review['restaurant'])
                
                new_review_object = Review(
                    source = new_review['source'],
                    restaurant = Restaurant.objects.filter(id=restaurant_id)[0],
                    title = new_review['title'][:50],
                    date = new_review['date'],
                    visit_date = new_review['visit_date'],
                    score = new_review['score'],
                    food = new_review['food'],
                    service = new_review['service'],
                    value = new_review['value'],
                    ambience = new_review['ambience'],
                    text = new_review['review'][:10000],
                    link = new_review['link']
                )
                    
                new_review_object.save()
                    
                self.stdout.write(self.style.SUCCESS('Review successfully created'))
                
            
        except Exception as err:
            self.stdout.write(self.style.ERROR('Error when updating database: ' + str(err)))
            return
        
        self.stdout.write(self.style.SUCCESS('Database successfully updated'))
        
        return