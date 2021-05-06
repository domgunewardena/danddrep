import requests
import pandas as pd

from bs4 import BeautifulSoup

import ..restaurant_urls

from .database import Database

class Tripadvisor(Database):
    
    def __init__(self, restaurant, method):
        
        super().__init__('tripadvisor')
        
        self.method = method
        self.name = restaurant
        self.restaurant_urls = restaurant_urls.tripadvisor_urls
        self.current_ids = list(self.database['id'])
        
        self.home_url = self.restaurant_urls[self.name]
        self.home_soup = self.get_soup(self.home_url)
        
        
    def __str__(self):
        
        print(self.name + ' Tripadvisor')
        
        
    def get_current_ids(self):
        
        df = self.database
        return list(df[df['restaurant']==self.name]['id'])
    
    
    def get_soup(self, url):
        
        response = requests.get(url)
        return BeautifulSoup(response.text, 'html.parser')
    
    
    def get_final_page(self, home_soup):
                
        return int(home_soup.select('.pageNum.last ')[0].text)
    
    
    def get_home_url_list(self, home_url, final_page):
        
        review_numbers_list = [x*10 for x in range(1,final_page)]
        home_url_split = home_url.split('Reviews-')
        
        first_half_url = home_url_split[0] + 'Reviews-'
        second_half_url = home_url_split[1]

        urls = [home_url]
        for num in review_numbers_list:
            full_url = first_half_url + 'or' + str(num) + '-' + second_half_url
            urls.append(full_url)

        return urls
    
#   GET REVIEW URLS 

#   'INNER' FUNCTIONS
    
    def get_reviews(self, soup):
        return soup.select('.reviewSelector')

    def get_id(self, review):
        return int(review['data-reviewid'])

    def get_review_url(self, review):

        def get_title(review):
            return review.select('.quote')[0]

        def get_anchor_text(title):
            return title.select('a')[0]

        def get_href(anchor):
            return anchor.get('href')

        slug = get_href(get_anchor_text(get_title(review)))
        link = 'https://www.tripadvisor.co.uk' + slug

        return link

    def add_review_urls_to_master_list(self, soup, review_urls):

        reviews = self.get_reviews(soup)
        for review in reviews:
#           Conditional logic for skipping review if already in current database when collecting new reviews
            if self.method == 'new':
                review_id = self.get_id(review)
                if review_id in self.current_ids:
                    continue
            link = self.get_review_url(review)
            review_urls.append(link)
    
#   END OF 'INNER' FUNCTIONS

    def get_review_urls(self):
                
        review_urls = []
        
        if self.method == 'all':
            
            self.final_page = self.get_final_page(self.home_soup)
            self.home_urls = self.get_home_url_list(self.home_url, self.final_page)
            
            for home_url in self.home_urls:
                soup = self.get_soup(home_url)
                self.add_review_urls_to_master_list(soup, review_urls)
        else:
            soup = self.home_soup
            self.add_review_urls_to_master_list(soup, review_urls)
            
        return review_urls
    
    
#   GENERATE REVIEW DICT 

#   'INNER' FUNCTIONS

    def get_id(self, review):
        return int(review['data-reviewid'])

    def get_link(self, review):
        href = review.select('.title')[0].get('href')
        return 'https://www.tripadvisor.co.uk' + href

    def get_title(self, review):
        title_string_class = '.noQuotes'
        return review.select(title_string_class)[0].text

    def get_date(self, review):
        dates_class = '.ratingDate'
        return review.select(dates_class)[0]['title']

    def get_visit_date(self, review):
        visit_date_class = '.prw_reviews_stay_date_hsx'
        return review.select(visit_date_class)[0].text[15:]

    def get_entry(self, review):
        text_class = '.entry'
        return review.select(text_class)[0].text.replace(' Show less', '')

    def get_scores(self, review):

        def get_scores_list(review):
            score_class = '.ui_bubble_rating'
            return review.select(score_class)

        def get_score(score):
            return int(score['class'][1][7])

        def get_sub_scores_list(review):
            sub_score_div_class = '.recommend-answer'
            return review.select(sub_score_div_class)

        def get_sub_score_name(sub_score_div):
            return sub_score_div.text

        def get_sub_score(sub_score_div):
            return get_score(get_scores_list(sub_score_div)[0])

        scores_list = get_scores_list(review)
        sub_scores_list = get_sub_scores_list(review)

        overall = get_score(scores_list[0])
        value = None
        service = None
        food = None

        for sub_score_div in sub_scores_list:

            sub_score_name = get_sub_score_name(sub_score_div)
            sub_score = get_sub_score(sub_score_div)

            if sub_score_name == 'Value':
                value = sub_score
            elif sub_score_name == 'Service':
                service = sub_score
            elif sub_score_name == 'Food':
                food = sub_score

        return overall, value, service, food

    def get_manager_response(self, review):

        response_class = '.mgrRspnInline'
        response_div = review.select(response_class)

        def get_response_text(response_div):

            response = ''
            for line in response_div[0].p.contents:
                if str(line) == '<br/>':
                    response += '\n'
                else:
                    response += line

            return response

        if response_div:
            return get_response_text(response_div)
        else:
            return None
        
#   END OF 'INNER' FUNCTIONS
    
    def generate_review_dict(self, review, url):

        review_id = self.get_id(review)
        review_title = self.get_title(review)
        review_date = self.get_date(review)
        visit_date = self.get_visit_date(review)
        review_entry = self.get_entry(review)
        score, value, service, food = self.get_scores(review)
        manager_response = self.get_manager_response(review)

        if url == 'home_url':
            review_link = self.get_link(review)
        else:
            review_link = url

        return {
            'id':review_id,
            'link':review_link,
            'restaurant':self.name,
            'title':review_title,
            'date':review_date,
            'visit_date':visit_date,
            'review':review_entry,
            'score':score,
            'value':value,
            'service':service,
            'food':food,
            'response':manager_response,
        }
    
    
#   GETTING REVIEWS
    
    def get_new_reviews(self):
        
        self.review_urls = self.get_review_urls()
        new_reviews = []  
        
        for review_url in self.review_urls:
            soup = self.get_soup(review_url)
            try:
                review = soup.select('.reviewSelector')[0]
            except:
                continue
            else:
                review_dict = self.generate_review_dict(review,review_url)
                new_reviews.append(review_dict)

        
        return new_reviews
    
    
#     UPDATING DATABASES
    
    def update_database(self):
        
        print(self.name + "'s Tripadvisor scraping started...")
        
        self.new_reviews = self.get_new_reviews()

        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)
            
        print(self.name + "'s Tripadvisor scraping finished.")
        
        
    def add_reviews_to_csv(self, new_reviews):
        
        new_reviews_df = pd.DataFrame(new_reviews)[self.column_names]
        new_database = self.database[self.column_names].append(new_reviews_df).drop_duplicates()
            
        new_database.to_csv('Tripadvisor.csv', index=False)
        
        return new_database