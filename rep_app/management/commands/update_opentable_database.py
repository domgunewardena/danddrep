from datetime import date, timedelta
import os

from django.core.management.base import BaseCommand, CommandError

import rep_app.scraping.restaurant_urls as restaurant_urls

from rep_app.scraping.scrapers import Opentable

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
            options.add_argument('--disable-dev-shm-usage')
    
            return webdriver.Chrome(
                executable_path=CHROMEDRIVER_PATH, 
                chrome_options=options
            )

        def update_Opentable(driver):

            self.stdout.write(self.style.SUCCESS('Opentable scraping started...'))

            for restaurant in restaurant_urls.opentable_urls.keys():
                opentable = Opentable(restaurant, driver)
                opentable.update_database()

            self.stdout.write(self.style.SUCCESS('Opentable scraping finished'))
            
        try:            
            driver = open_driver()
            update_Opentable(driver)
            
        except Exception as err:
            self.stdout.write(self.style.ERROR('Error when updating Opentable database: ' + str(err)))
            return
        
        self.stdout.write(self.style.SUCCESS('Opentable database successfully updated'))
        
        return