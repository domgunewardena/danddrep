from datetime import date, timedelta
import os

from django.core.management.base import BaseCommand, CommandError
from rep_app.models import Review, Restaurant

from rep_app.scrapers import Reviews
from rep_app.restaurant_list import restaurant_dict

from selenium import webdriver

class Command(BaseCommand):
    
    help = 'Create review objects from new reviews in database'
    
    def handle(self, *args, **options):
            
        def get_restaurant_id(restaurant_string):
            
            try:
                return int(restaurant_dict[restaurant_string]['id'])
            except:
                return None
            
        try:
            
            reviews = Reviews()
            new_reviews = reviews.get_new_reviews()
            
            for new_review in new_reviews:
                
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
                
            reviews.update_database()
            
        except Exception as err:
            
            self.stdout.write(self.style.ERROR('Error when updating database: ' + str(err)))
            
            return
        
        self.stdout.write(self.style.SUCCESS('Database successfully updated'))
        
        return