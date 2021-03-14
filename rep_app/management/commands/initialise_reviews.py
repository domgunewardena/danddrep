from django.core.management.base import BaseCommand, CommandError
from rep_app.models import Review, Restaurant
from rep_app.scrapers import Reviews
from rep_app.restaurant_list import restaurant_dict

class Command(BaseCommand):
    
    help = 'Create review objects from all reviews in database'
    
    def handle(self, *args, **options):
        
        def get_restaurant_id(restaurant_string):
            try:
                return int(restaurant_dict[restaurant_string]['id'])
            except:
                return None
        
        try:
            reviews = Reviews()
            reviews_database = reviews.database.copy()

            reviews_database['restaurant_id'] = reviews_database['restaurant'].apply(get_restaurant_id)
            reviews_database = reviews_database[reviews_database['restaurant_id'].notnull()]

            all_reviews = [
                Review(
                    source = reviews_database.iloc[row]['source'],
                    restaurant = Restaurant.objects.filter(id=reviews_database.iloc[row]['restaurant_id'])[0],
                    title = reviews_database.iloc[row]['title'],
                    date = reviews_database.iloc[row]['date'],
                    visit_date = reviews_database.iloc[row]['visit_date'],
                    score = reviews_database.iloc[row]['score'],
                    food = reviews_database.iloc[row]['food'],
                    service = reviews_database.iloc[row]['service'],
                    value = reviews_database.iloc[row]['value'],
                    ambience = reviews_database.iloc[row]['ambience'],
                    text = reviews_database.iloc[row]['review'],
                    link = reviews_database.iloc[row]['link']
                )
                for row in range(len(reviews_database)) 
            ]

            Review.objects.bulk_create(all_reviews)
            
        except Exception as err:
            self.stdout.write(self.style.ERROR('Error when creating reviews: ' + str(err)))
            return
        
        self.stdout.write(self.style.SUCCESS('All reviews created'))
        
        return