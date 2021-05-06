import os
import pandas as pd
import psycopg2
from sqlalchemy import create_engine

from ...scraping import postgresql_tables as postgresql

class Database():
    
    def __init__(self, table):
        
        self.postgres_host = os.environ['POSTGRESQL_HOST']
        self.postgres_database = os.environ['POSTGRESQL_DATABASE']
        self.postgres_user = os.environ['POSTGRESQL_USER']
        self.postgres_password = os.environ['POSTGRESQL_PASSWORD']
    
        self.table = table
        self.create_query = postgresql.tables['create_query'][table]
        self.select_query = 'SELECT * FROM ' + table
        self.column_names = postgresql.tables['columns'][table]
        self.database = self.to_dataframe()
    
    def connect_to_database(self):
        
        return psycopg2.connect(
            host=self.postgres_host,
            database=self.postgres_database,
            user=self.postgres_user,
            password=self.postgres_password
        )
    
    def execute_query(self, query, commit_boolean):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute(query)
        
        if commit_boolean:
            conn.commit()

        cur.close()
        conn.close()
        
    def execute_query_with_dic(self, query, dic, commit_boolean):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        cur.execute(query, dic)
        
        if commit_boolean:
            conn.commit()

        cur.close()
        conn.close()
        
        
    def create(self):
        
        self.execute_query(self.create_query, True)   
        
    def select_query_to_dataframe(self, select_query, columns):
        
        conn = self.connect_to_database()
        cur = conn.cursor()
        
        cur.execute(select_query)
        tuples = cur.fetchall()
        cur.close()
        conn.close()
        
        return pd.DataFrame(tuples, columns=columns)
        
    def to_dataframe(self):
        
        query = self.select_query
        columns = self.column_names
        
        return self.select_query_to_dataframe(query, columns) 
        
    def table_to_dataframe(self,table):
        
        query = 'SELECT * FROM ' + table
        columns = postgresql.tables['columns'][table]
        
        return self.select_query_to_dataframe(query, columns) 
    
    def upload_to_database(self, dataframe):
        
        engine_string = 'postgresql://' + self.postgres_user + ':' + self.postgres_password + '@' + self.postgres_host + '/' + self.postgres_database

        engine = create_engine(engine_string)
        con = engine.connect()

        dataframe.to_sql(
            self.table,
            con=con,
            index=False,
            if_exists='replace'
        )

        con.close()
        
    def upload_to_other_database(self, table, dataframe):
        
        engine_string = 'postgresql://' + self.postgres_user + ':' + self.postgres_password + '@' + self.postgres_host + '/' + self.postgres_database

        engine = create_engine(engine_string)
        con = engine.connect()

        dataframe.to_sql(
            table,
            con=con,
            index=False,
            if_exists='replace'
        )

        con.close()
        
    def add_reviews_to_database(self, new_reviews):
        
        for review in new_reviews:
            
            keys = review.keys()
            table = self.table
            columns = ', '.join(keys)
            values = ', '.join(['%({})s'.format(k) for k in keys])
            insert_query = 'INSERT INTO {0} ({1}) VALUES ({2});'.format(table, columns, values)
            
            self.execute_query_with_dic(insert_query, review, True)