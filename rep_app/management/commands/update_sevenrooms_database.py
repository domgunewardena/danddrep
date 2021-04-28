from datetime import date, timedelta
import os

from django.core.management.base import BaseCommand, CommandError

import rep_app.scraping.restaurant_urls as restaurant_urls

from rep_app.scraping.scrapers import SevenRooms

from selenium import webdriver

class Command(BaseCommand):
    
    help = 'Update SevenRooms database'
    
    def handle(self, *args, **options):

        def update_SevenRooms():

            today_string = date.today().strftime('%Y-%m-%d')
            yesterday_string = (date.today()-timedelta(1)).strftime('%Y-%m-%d')
            
            self.stdout.write(self.style.SUCCESS('Sevenrooms scraping started...'))

            sr = SevenRooms(yesterday_string,today_string)
            sr.update_database()
            
            self.stdout.write(self.style.SUCCESS('SevenRooms scraping finished'))
            
        try:
            
            update_SevenRooms()
         
        except Exception as err:
            
            self.stdout.write(self.style.ERROR('Error when updating SevenRooms database: ' + str(err)))
            
            return
        
        self.stdout.write(self.style.SUCCESS('SevenRooms database successfully updated'))
        
        return