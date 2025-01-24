import pymysql
import os
from dotenv import load_dotenv

load_dotenv()
conn = pymysql.connect( 
    host=os.environ['DATAHOST'], 
    user=os.environ['DATAUSER'],
    password=os.environ['DATAPWD'],  
    database=os.environ['DATADB']
)

# For each individual user (intended not actually yet)
# Tracks which crypto they looked up. If previously looked up, delete row and insert into top of databse to track history.
def create_table():
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Ticker (
                id INT PRIMARY KEY AUTO_INCREMENT,
                symbol VARCHAR(200) NOT NULL,
                ask_price VARCHAR(20),
                bid_price VARCHAR(20),
                last_trade VARCHAR(20),
                wvap VARCHAR(20),
                trades_24h INT,
                day_low VARCHAR(20),
                day_high VARCHAR(20),
                day_open VARCHAR(20)
            )
        ''')
        conn.commit()

# List of all info
def create_full_data_table():
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Full_Data (
                id INT PRIMARY KEY AUTO_INCREMENT,
                symbol VARCHAR(200) NOT NULL,
                ask_price VARCHAR(20),
                bid_price VARCHAR(20),
                last_trade VARCHAR(20),
                wvap VARCHAR(20),
                trades_24h INT,
                day_low VARCHAR(20),
                day_high VARCHAR(20),
                day_open VARCHAR(20)
            )
        ''')
        conn.commit()

# To track an individual stock and predict
def create_Single_Stock_table():
    with conn.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS Single_Stock_Data (
                id INT PRIMARY KEY AUTO_INCREMENT,
                symbol VARCHAR(200) NOT NULL,
                ask_price VARCHAR(20),
                bid_price VARCHAR(20),
                last_trade VARCHAR(20),
                wvap VARCHAR(20)
            )
        ''')
        conn.commit()
        