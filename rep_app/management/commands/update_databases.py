from datetime import date, timedelta
import os

from django.core.management.base import BaseCommand, CommandError

from rep_app.models import Review, Restaurant
from rep_app.restaurant_list import restaurant_dict

from rep_app.scraping.scrapers import Google, Tripadvisor, Opentable, SevenRooms, Reviews
import rep_app.scraping.restaurant_urls as restaurant_urls

from selenium import webdriver

class Command(BaseCommand):
    
    help = 'Create review objects from new reviews in database'
    
    def handle(self, *args, **options):
        
        def open_driver():
            
            try:

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

            except Exception as err:
                
                self.stdout.write(self.style.ERROR('Error when opening driver: ' + str(err)))
                
            else:
                
                self.stdout.write(self.style.SUCCESS('Driver successfully opened'))
        
        def update_google_database(driver):
            
            try:

                self.stdout.write(self.style.SUCCESS('Google scraping started...'))

                google = Google('new', driver)
                google.update_database()

                self.stdout.write(self.style.SUCCESS('Google scraping finished'))

            except Exception as err:
                
                self.stdout.write(self.style.ERROR('Error when updating Google database: ' + str(err)))
                
            else:
                
                self.stdout.write(self.style.SUCCESS('Google database successfully updated'))
        
        def update_tripadvisor_database():
            
            try:

                self.stdout.write(self.style.SUCCESS('Tripadvisor scraping started...'))

                for restaurant in restaurant_urls.tripadvisor_urls.keys():
                    tripadvisor = Tripadvisor(restaurant, 'new')
                    tripadvisor.update_database()

                self.stdout.write(self.style.SUCCESS('Tripadvisor scraping finished'))

            except Exception as err:
                
                self.stdout.write(self.style.ERROR('Error when updating Tripadvisor database: ' + str(err)))
                
            else:
                
                self.stdout.write(self.style.SUCCESS('Tripadvisor database successfully updated'))
                
        def update_opentable_database(driver):
            
            try:

                self.stdout.write(self.style.SUCCESS('Opentable scraping started...'))

                for restaurant in restaurant_urls.opentable_urls.keys():
                    opentable = Opentable(restaurant, driver)
                    opentable.update_database()

                self.stdout.write(self.style.SUCCESS('Opentable scraping finished'))

            except Exception as err:
                
                self.stdout.write(self.style.ERROR('Error when updating Opentable database: ' + str(err)))
                
            else:
                
                self.stdout.write(self.style.SUCCESS('Opentable database successfully updated'))
                
        def update_sevenrooms_database():
            
            try:

                today_string = date.today().strftime('%Y-%m-%d')
                yesterday_string = (date.today()-timedelta(1)).strftime('%Y-%m-%d')

                self.stdout.write(self.style.SUCCESS('Sevenrooms scraping started...'))

                sr = SevenRooms(yesterday_string,today_string)
                sr.update_database()

                self.stdout.write(self.style.SUCCESS('SevenRooms scraping finished'))
                
            except Exception as err:
                
                self.stdout.write(self.style.ERROR('Error when updating SevenRooms database: ' + str(err)))
                
            else:
                
                self.stdout.write(self.style.SUCCESS('SevenRooms database successfully updated'))
                
        def update_central_database():
            
            def get_restaurant_id(restaurant_string):

                try:
                    return int(restaurant_dict[restaurant_string]['id'])
                except:
                    return None

            try:

                print('Creating Reviews scraper')
                reviews = Reviews()

                print('Getting new reviews...')
                new_reviews = reviews.get_new_reviews()

                for new_review in new_reviews:

                    restaurant_id = get_restaurant_id(new_review['restaurant'])

                    if restaurant_id:

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

                print('Updating database')
                reviews.update_database()

            except Exception as err:

                self.stdout.write(self.style.ERROR('Error when updating database: ' + str(err)))
                
            else:
                
                self.stdout.write(self.style.SUCCESS('Central database successfully updated'))
                
        driver = open_driver()
        update_google_database(driver)
        update_tripadvisor_database()
        update_opentable_database(driver)
        update_central_database()
        
        return