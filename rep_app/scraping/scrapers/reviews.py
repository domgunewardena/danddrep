import pandas as pd

from ...scraping import postgresql_tables as postgresql

from .database import Database

class Reviews(Database):
    
    def __init__(self):
        
        super().__init__('reviews')
    
    
    def get_tripadvisor_reviews(self):
        
        def turn_id_to_string(df):
            
            df['id'] = df['id'].apply(str)
            return df
        
        def add_source(df):
            
            df['source'] = 'Tripadvisor'
            return df
        
        current_df = self.table_to_dataframe('tripadvisor')
        
        df = add_source(
            turn_id_to_string(
                current_df
            )
        )
        
        return df
    
    
    def get_opentable_reviews(self):
        
        def add_source(df):
            
            df['source'] = 'Opentable'
            return df
        
        def add_date(df):
            
            df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.strftime("%d %B %Y") 
            return df
        
        def rename_columns(df):
            
            rename_columns_map = postgresql.tables['to_master_database_maps']['rename_columns']['opentable']
            return df.rename(columns=rename_columns_map)
            return df
            
        def map_restaurants(df):
            
            restaurant_map = postgresql.tables['to_master_database_maps']['restaurant']['opentable']
            df['restaurant'] = df['restaurant'].map(restaurant_map)
            return df
        
        current_df = self.table_to_dataframe('opentable')
        
        df = map_restaurants(
            rename_columns(
                add_date(
                    add_source(
                        current_df
                    )
                )
            )
        )
        
        return df
    
    
    def get_google_reviews(self):
        
        def rename_columns(df):
            
            rename_columns_map = postgresql.tables['to_master_database_maps']['rename_columns']['google']
            return df.rename(columns=rename_columns_map)
        
        def add_source(df):
            
            df['source'] = 'Google'
            return df
        
        def turn_scores_to_numbers(df):
            
            score_map = {
                'FIVE':5,
                'FOUR':4,
                'THREE':3,
                'TWO':2,
                'ONE':1
            }
            
            df['score'] = df['score'].map(score_map)
            return df
        
        def format_dates(df):
            
            def remove_first_0(date_string):
                return date_string[1:] if date_string[0] == '0' else date_string
            
            df['date'] = pd.to_datetime(df['date'].str[:10]).dt.strftime('%d %B %Y').apply(str).apply(remove_first_0)
            return df
        
        def map_restaurants(df):
            
            restaurant_map = postgresql.tables['to_master_database_maps']['restaurant']['google']
            df['restaurant'] = df['restaurant'].map(restaurant_map)
            return df
        
        current_df = self.table_to_dataframe('google')
            
        df = map_restaurants(
            format_dates(
                turn_scores_to_numbers(
                    add_source(
                        rename_columns(
                            current_df
                        )
                    )
                )
            )
        )
        
        return df
    
    
    def get_sevenrooms_reviews(self):
        
        def rename_columns(df):
            
            rename_columns_map = postgresql.tables['to_master_database_maps']['rename_columns']['sevenrooms']
            return df.rename(columns=rename_columns_map)
        
        def add_source(df):
            
            df['source'] = 'SevenRooms'
            return df
            
        def map_restaurants(df):
            
            restaurant_map = postgresql.tables['to_master_database_maps']['restaurant']['sevenrooms']
            df['restaurant'] = df['restaurant'].map(restaurant_map)
            return df
        
        def format_dates(df):
            
            df['date'] = pd.to_datetime(df['date'], dayfirst=True).dt.strftime("%d %B %Y")            
            return df
        
        current_df = self.table_to_dataframe('sevenrooms')
        
        df = format_dates(
            map_restaurants(
                add_source(
                    rename_columns(
                        current_df
                    )
                )
            )
        )
        
        return df
    
        
    def get_new_database(self):
        
        print('Creating Tripadvisor reviews df')
        self.tripadvisor_df = self.get_tripadvisor_reviews()
        print('Creating Opentable reviews df')
        self.opentable_df = self.get_opentable_reviews()
        print('Creating Google reviews df')
        self.google_df = self.get_google_reviews()
        print('Creating SevenRooms reviews df')
        self.sevenrooms_df = self.get_sevenrooms_reviews()
        self.columns = postgresql.tables['columns']['reviews']
        
        print('Merging TA & OT reviews')
        tripadvisor_opentable = pd.merge(
            left = self.tripadvisor_df,
            right = self.opentable_df,
            how = 'outer'
        )
        print('Merging TAOT & GO reviews')
        tripadvisor_opentable_google_df = pd.merge(
            left = tripadvisor_opentable,
            right = self.google_df,
            how = 'outer'
        )
        
        print('Merging TAOTGO & SR reviews')
        all_df = pd.merge(
            left = tripadvisor_opentable_google_df,
            right = self.sevenrooms_df,
            how = 'outer'
        )
        
        print('Filtering reviews df by columns')
        df = all_df[self.columns]
        df['date'] = pd.to_datetime(df['date'])
        df['visit_date'] = df['visit_date'].apply(str)
        df['review'] = df['review'].fillna('')
        
        score_strings = ['score','food','service','value','ambience']
        for string in score_strings:
            df[string] = df[string].fillna(0)
        
        return df
    
    
    def get_new_reviews(self):
        
        print('Getting new database...')
        self.new_database = self.get_new_database()
        
        print('Merging new and old databases')
        df = pd.merge(
            left = self.new_database,
            right = self.database,
            how = 'left',
            indicator = True
        )
        
        print('Filtering merged databases by just new reviews')
        new_reviews_df = df[df['_merge']=='left_only'][self.columns]
        
        return new_reviews_df.to_dict('records')
    
    
    def update_database(self):
        
        self.new_reviews = self.get_new_reviews()
        if self.new_reviews:
            self.add_reviews_to_database(self.new_reviews)