from datetime import date, timedelta
import os

from django.core.management.base import BaseCommand, CommandError

from rep_app.scrapers import Google
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
            options.add_argument('--disable-dev-shm-usage')
    
            return webdriver.Chrome(
                executable_path=CHROMEDRIVER_PATH, 
                chrome_options=options
            )

        def update_Google(driver):
            
            self.stdout.write(self.style.SUCCESS('Google scraping started...'))

            google = Google('new', driver)
            google.update_database()
            
            self.stdout.write(self.style.SUCCESS('Google scraping finished'))
            
        try:            
            driver = open_driver()
            update_Google(driver)   
            
        except Exception as err:
            self.stdout.write(self.style.ERROR('Error when updating database: ' + str(err)))
            return
        
        self.stdout.write(self.style.SUCCESS('Google database successfully updated'))
        
        return