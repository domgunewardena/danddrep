import os
import requests
import json
import pandas as pd

import ..restaurant_urls

from .database import Database

class SevenRooms(Database):
    
    def __init__(self, start_date, end_date):
        
        super().__init__('sevenrooms')
        
        self.start_date = start_date
        self.end_date = end_date
    
        self.client_id = os.environ['SR_CLIENT_ID']
        self.client_secret = os.environ['SR_CLIENT_SECRET']
        self.venue_group_id = os.environ['SR_VENUE_GROUP_ID']
    
    def get_token(self):

        url = "https://api.sevenrooms.com/2_2/auth"
        headers = {'Content-type': 'application/json'}

        parameters = {
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        r = requests.post(
            url,
            headers=headers,
            params=parameters
        )

        return r.json()['data']['token']

    def get_venue_ids(self):
        
        self.token = self.get_token()

        url = "https://api.sevenrooms.com/2_2/venues"
        headers = {'authorization': self.token}

        parameters = {
            'venue_group_id' : self.venue_group_id,
            'limit':100
        }

        r = requests.get(
            url,
            headers=headers,
            params=parameters
        )

        restaurant_ids_df = pd.DataFrame(r.json()["data"]["results"])[["id","name"]]
        restaurant_ids_df.columns = ["venue_id","restaurant"]

        return restaurant_ids_df
    
    def get_reviews(self):
        
        def americanise_date(date_string):
            return date_string[3:5] + '-' + date_string[:2] + '-' + date_string[6:]
        
        def generate_reservation_url(restaurant_id, americanised_reservation_date, reservation_id):
            return 'https://www.sevenrooms.com/manager/' + restaurant_id + '/reservations/day/' + americanised_reservation_date +  '?actual_id=' +  reservation_id
        
        def numericize_scores(review):
            
            score_strings = ['overall','food','service','ambience']
            for score_string in score_strings:
                review[score_string] = int(review[score_string])
            
            return review
        
        self.restaurant_ids_df = self.get_venue_ids()
        venue_ids = list(self.restaurant_ids_df['venue_id'])
        reviews = []
        
        for venue_id in venue_ids:

            mask = self.restaurant_ids_df['venue_id'] == venue_id
            restaurant = list(self.restaurant_ids_df[mask]['restaurant'])[0]
            
            if restaurant == 'The Secret Garden':
                continue
            
            print('Getting ' + restaurant + "'s reviews")
            url = "https://api.sevenrooms.com/2_2/venues/" + venue_id + '/feedback'

            headers = {'authorization':self.token}

            parameters = {
                'start_date': self.start_date,
                'end_date': self.end_date,
            }

            r = requests.get(
                url,
                headers = headers,
                params = parameters
            )

            try:
                review_dicts = r.json()['data']['reservation_feedback']
            except:
                continue
            else:
                for review in review_dicts:
                    
                    link_date_string = americanise_date(review['reservation_date'])
                    reservation_id = review['reservation_id']
                    restaurant_id = restaurant_urls.sevenrooms_url_restaurant_ids[restaurant]
                    reservation_url = generate_reservation_url(restaurant_id, link_date_string, reservation_id)
                    
                    review['link'] = reservation_url
                    review['restaurant'] = restaurant
                    review = numericize_scores(review)
                    
                    reviews.append(review)
                    
        return reviews
    
    
#     UPDATING DATABASES
    
    def update_database(self):
    
        print('Fetching SevenRooms reviews...')
        
        self.new_reviews = self.get_reviews()

        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)
    
        print('SevenRooms finished')