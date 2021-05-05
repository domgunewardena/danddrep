from datetime import date, timedelta
import os

from django.core.management.base import BaseCommand, CommandError

import rep_app.restaurant_urls as restaurant_urls

from rep_app.scraping.scrapers.tripadvisor import Tripadvisor

class Command(BaseCommand):
    
    help = 'Create review objects from all reviews in database'
    
    def handle(self, *args, **options):

        def update_Tripadvisor():

            self.stdout.write(self.style.SUCCESS('Tripadvisor scraping started...'))

            for restaurant in restaurant_urls.tripadvisor_urls.keys():
                tripadvisor = Tripadvisor(restaurant, 'new')
                tripadvisor.update_database()

            self.stdout.write(self.style.SUCCESS('Tripadvisor scraping finished'))
            
        try: 
            update_Tripadvisor()
            
        except Exception as err:
            self.stdout.write(self.style.ERROR('Error when updating Tripadvisor database: ' + str(err)))
            return
        
        self.stdout.write(self.style.SUCCESS('Tripadvisor database successfully updated'))
        
        return