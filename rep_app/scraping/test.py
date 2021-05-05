import unittest
import test_results

from scrapers.google import Google
from scrapers.tripadvisor import Tripadvisor
from scrapers.opentable import Opentable
from scrapers.sevenrooms import SevenRooms
from scrapers.reviews import Reviews

from selenium.webdriver import Chrome

class TestGoogle(unittest.TestCase):
    
    google = Google('new')
    bluebird_location_dict = test_results.google_location_dicts[0]
    bluebird_reviews_url = 'https://mybusiness.googleapis.com/v4/accounts/111855729671132001333/locations/8494375825452078058/reviews'
    bluebird_location_name = 'Bluebird Chelsea'
    3
    
#   TEST DATABASE
    
    def test_database_columns(self):
        
        database_columns = [
            'location',
            'name',
            'review_id',
            'reviewer_display_name',
            'star_rating',
            'comment',
            'create_time',
            'update_time',
            'link'
        ]
        
        result = list(self.google.database.columns)
        
        self.assertEqual(result, database_columns)
        
    def test_database_length(self):
        
        result = len(self.google.database)
        
        self.assertGreater(result,0)
        
#   TEST INFO FUNCTIONS
    
    def test_get_account_id(self):
        
        result = self.google.get_account_id()
        account_id = '111855729671132001333'
        
        self.assertEqual(result, account_id)
        
    def test_get_location_dicts(self):
        
        location_dict_keys = [
            'name',
            'storeCode',
            'locationName',
            'primaryPhone',
            'primaryCategory',
            'additionalCategories',
            'websiteUrl',
            'regularHours',
            'locationKey',
            'additionalPhones',
            'latlng',
            'openInfo',
            'locationState',
            'attributes',
            'metadata',
            'languageCode',
            'address',
            'profile'
        ]
        
        result = list(self.google.get_location_dicts()[0])
        
        self.assertEqual(result, location_dict_keys)
        
#   TEST REVIEW FUNCTIONS
        
    def test_check_empty_restaurant(self):
        
        empty_restaurant = 'Almeida'
        full_restaurant = 'Skylon'
        
        result1 = self.google.check_empty_restaurant(empty_restaurant)
        result2 = self.google.check_empty_restaurant(full_restaurant)
        
        self.assertTrue(result1)
        self.assertFalse(result2)
        
    def test_get_reviews_url(self):
        
        result = self.google.get_reviews_url(self.bluebird_location_dict)
        
        self.assertEqual(result, self.bluebird_reviews_url)
        
    def test_get_first_response(self):
        
        response_keys = [
            'reviews', 
            'averageRating', 
            'totalReviewCount', 
            'nextPageToken'
        ]
        
        result = list(self.google.get_first_response(self.bluebird_reviews_url).keys())
        
        self.assertEqual(result, response_keys)
        
    def test_get_first_response_returns_reviews_dict(self):
        
        reviews_dict_keys = [
            'reviewId',
             'reviewer',
             'starRating',
             'comment',
             'createTime',
             'updateTime',
             'name'
        ]
        
        result = list(self.google.get_first_response(self.bluebird_reviews_url)['reviews'][0].keys())
        
        self.assertEqual(result, reviews_dict_keys)
        
        
        
class TestTripadvisor(unittest.TestCase):
    
    def setUp(self):
    
        self.tripadvisor = Tripadvisor('100 Wardour Street','new')

        self.test_home_review_object = self.tripadvisor.get_reviews(self.tripadvisor.home_soup)[0]

        self.review_url = 'https://www.tripadvisor.co.uk/ShowUserReviews-g186338-d9582978-r779135247-100_Wardour_St-London_England.html'
        self.soup = self.tripadvisor.get_soup(self.review_url)
        self.review_object = self.soup.select('.reviewSelector')[0]

        self.scores_url = 'https://www.tripadvisor.co.uk/ShowUserReviews-g186338-d9582978-r767902348-100_Wardour_St-London_England.html'
        self.soup = self.tripadvisor.get_soup(self.scores_url)
        self.scores_review_object = self.soup.select('.reviewSelector')[0]
        
#   TEST DATABASE
        
    def test_database_columns(self):
        
        database_columns = [
            'id',
            'link',
            'restaurant',
            'title',
            'date',
            'visit_date',
            'review',
            'score',
            'value',
            'service',
            'food',
            'response'
        ]
        
        result = list(self.tripadvisor.database.columns)
        
        self.assertEqual(result, database_columns)
        
    def test_database_length(self):
        
        result = len(self.tripadvisor.database)
        
        self.assertGreater(result,0)
    
#   TEST GETTING REVIEW URLS
    
    def test_get_home_review_id(self):
        
        result = self.tripadvisor.get_id(self.test_home_review_object)
        
        self.assertIsInstance(result,int)
        
    def test_get_home_review_url(self):
        
        result = self.tripadvisor.get_review_url(self.test_home_review_object)
        sample_url = 'https://www.tripadvisor.co.uk/ShowUserReviews-g186338-d9582978-r779135247-100_Wardour_St-London_England.html'
        
        self.assertEqual(result[:63],sample_url[:63])
        
#   TEST GENERATING REVIEW DICTIONARIES

    def test_get_review_id(self):
        
        result = self.tripadvisor.get_id(self.review_object)
        review_id = 779135247
        
        self.assertEqual(result, review_id)
        
    def test_get_review_title(self):
        
        result = self.tripadvisor.get_title(self.review_object)
        review_title = 'Best service ever!! Thank you ♥️'
        
        self.assertEqual(result, review_title)
        
    def test_get_review_date(self):
        
        result = self.tripadvisor.get_date(self.review_object)
        review_date = '13 December 2020'
        
        self.assertEqual(result, review_date)
        
    def test_get_visit_date(self):
        
        result = self.tripadvisor.get_visit_date(self.review_object)
        visit_date = 'December 2020'
        
        self.assertEqual(result, visit_date)
        
    def test_get_entry(self):
        
        result = self.tripadvisor.get_entry(self.review_object)
        review_entry = 'We had the best time with the most amazing waiter he was ACE!!!! So friendly, so welcoming and overall outstanding customer service, we wish every waiter was like you Antonio!!!!! Thank you Antonio have a wonderful Christmas you special treasure ♥️♥️♥️'
        
        self.assertEqual(result, review_entry)
        
    def test_get_scores(self):
        
        result_none = self.tripadvisor.get_scores(self.review_object)
        result_all = self.tripadvisor.get_scores(self.scores_review_object)
        
        review_scores_none = (5, None, None, None)
        review_scores_all = (2, 3, 2, 4)
        
        self.assertEqual(result_none, review_scores_none)
        self.assertEqual(result_all, review_scores_all)
        
    def test_get_manager_response(self):
        
        result = self.tripadvisor.get_manager_response(self.review_object)
        manager_response = 'Dear Katie P,\n\nThank you so much for your kind review!\n\nWe hope it won’t be too long before your next visit as we would love to welcome you back soon.\n\nKind regards,\n\nAnthony B\n\nDeputy General Manager\nanthonyb@danddlondon.com'
        
        self.assertEqual(result, manager_response)
        
    def test_generate_review_dict(self):
        
        result = self.tripadvisor.generate_review_dict(self.review_object, self.review_url)
        
        self.assertEqual(result, test_results.tripadvisor_review_dict)

        
class OpentableTest(unittest.TestCase):
    
    opentable = Opentable('100 Wardour Street Club', driver)
        
#   TEST DATABASE
        
    def test_database_columns(self):
        
        database_columns = [
            'restaurant',
            'name',
            'date',
            'dined_date',
            'overall_score',
            'food_score',
            'service_score',
            'ambience_score',
            'review_text',
            'id',
            'link'
        ]
        
        result = list(self.opentable.database.columns)
        
        self.assertEqual(result, database_columns)
        
    def test_database_length(self):
        
        result = len(self.opentable.database)
        
        self.assertGreater(result,0)
        
#   TEST GETTING REVIEWS
        
    def test_get_first_page_reviews(self):
        
        result = self.opentable.get_first_page_reviews()
        
        self.assertEqual(len(result), 40)
        
        self.assertEqual(result[0]['restaurant'], '100 Wardour Street Club')
        
        self.assertIsInstance(result[0]['name'], str)
        self.assertNotEqual(len(result[0]['name']), 0)
        
        self.assertIsInstance(result[0]['overall_score'], int)
        
        self.assertIsInstance(result[0]['food_score'], int)
        
        self.assertIsInstance(result[0]['service_score'], int)
        
        self.assertIsInstance(result[0]['ambience_score'], int)
        
        self.assertIsInstance(result[0]['dined_date'], str)
        self.assertNotEqual(len(result[0]['dined_date']), 0)   
        
#     def tearDown(self):
        
#         self.driver.quit()
        
        
class SevenRoomsTest(unittest.TestCase):
    
    sevenrooms = SevenRooms('2021-01-01','2021-01-02')
    test_review = test_results.sevenrooms_review
    
#     def setUp(self):
        
#         self.sevenrooms = SevenRooms('2021-01-01','2021-01-02')
#         self.test_review = test_results.sevenrooms_review
        
#   TEST DATABASE
        
    def test_database(self):
        
        database_columns = [
            'reservation_id',
            'restaurant',
            'received_date',
            'reservation_date',
            'overall',
            'food',
            'service',
            'ambience',
            'recommend_to_friend',
            'notes',
            'link'
        ]
        
        result = list(self.sevenrooms.database.columns)
        
        self.assertEqual(result, database_columns)
        
    def test_database_length(self):
        
        result = len(self.sevenrooms.database)
        
        self.assertGreater(result,0)
        
#   TEST GETTING REVIEWS
        
    def test_get_reviews(self):
        
        result = self.sevenrooms.get_reviews()
        
        self.assertEqual(result,self.test_review)
        
        
        
class ReviewsTest(unittest.TestCase):
    
    def setUp(self):
        
        self.reviews = Reviews()
    
    def test_tripadvisor_database(self):
        
        database_columns = [
            'id',
            'link',
            'restaurant',
            'title',
            'date',
            'visit_date',
            'review',
            'score',
            'value',
            'service',
            'food',
            'response',
            'source'
        ]
        
        tripadvisor = self.reviews.get_tripadvisor_reviews()
        result = list(tripadvisor.columns)
        
        self.assertEqual(result, database_columns)
    
    def test_opentable_database(self):
        
        database_columns = [
            'restaurant',
            'title',
            'date',
            'visit_date',
            'score',
            'food',
            'service',
            'ambience',
            'review',
            'id',
            'link',
            'source'
        ]
        
        opentable = self.reviews.get_opentable_reviews()
        result = list(opentable.columns)
        
        self.assertEqual(result, database_columns)
    
    def test_google_database(self):
        
        database_columns = [
            'restaurant',
            'name',
            'id',
            'title',
            'score',
            'review',
            'date',
            'update_time',
            'link',
            'source'
        ]
        
        google = self.reviews.get_google_reviews()
        result = list(google.columns)
        
        self.assertEqual(result, database_columns)
    
    def test_sevenrooms_database(self):
        
        database_columns = [
            'title',
            'restaurant',
            'date',
            'visit_date',
            'score',
            'food',
            'service',
            'ambience',
            'recommend_to_friend',
            'review',
            'link',
            'source'
        ]
        
        sevenrooms = self.reviews.get_sevenrooms_reviews()
        result = list(sevenrooms.columns)
        
        self.assertEqual(result, database_columns)
    
    def test_new_database(self):
        
        database_columns = [
            'source',
            'restaurant',
            'title',
            'date',
            'visit_date',
            'score',
            'food',
            'service',
            'value',
            'ambience',
            'review',
            'link'
        ]
        
        new_database = self.reviews.get_new_database()
        result = list(new_database.columns)
        
        self.assertEqual(result, database_columns)
        

if __name__ == '__main__':
    
    try:
        driver = Chrome('./chromedriver')
        unittest.main()
    finally:
        driver.quit()    