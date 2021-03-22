from datetime import date, timedelta

from django.core.management.base import BaseCommand, CommandError
from rep_app.models import Review, Restaurant
from rep_app.scraping.scrapers import Reviews
from rep_app.restaurant_list import restaurant_dict

class Command(BaseCommand):
    
    help = 'Create review objects from all reviews in database'
    
    def handle(self, *args, **options):
        
        def monday(date):
            return date - timedelta(date.weekday())

        def months_ago(date, n):
            return date - timedelta(28*n)

        def one_year_ago(date):
            return date - timedelta(364)

        today = one_year_ago(date.today())
        upper_bound = months_ago(monday(today), 4)
        
        try:
            old_reviews = Review.objects.filter(date__lt = upper_bound)
            old_reviews.delete()
            
        except Exception as err:
            self.stdout.write(self.style.ERROR('Error when deleting old reviews: ' + str(err)))
            return
        
        self.stdout.write(self.style.SUCCESS('Old reviews deleted'))
        
        return