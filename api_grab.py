import requests
from data import conn

def fetch_valid_tickers():
    headers = {'Accept': 'application/json'}
    url = "https://api.kraken.com/0/public/Ticker"
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        result = response.json().get("result", {})
        if not result:
            print("No tickers found.")
            return []
        # print(result.keys())
        return list(result.keys())
    except requests.exceptions.RequestException as e:
        print(f"Error fetching valid tickers: {e}")
        return []

    
def fetch_and_store_ticker_data(ticker):
    url = "https://api.kraken.com/0/public/Ticker"
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers, params={'pair': ticker})
    # print("Method called")

    if response.status_code == 200:
        # print(f"API Response for {ticker}: {response.json()}")
        
        # Extract the data for the specific ticker
        data = response.json().get("result", {}).get(ticker)
        
        if data:
            # print(f"Fetched data for {ticker}: {data}")
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO Ticker (symbol, ask_price, bid_price, last_trade, wvap, trades_24h, day_low, day_high, day_open)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ''', (
                    ticker,
                    data['a'][0],  # ask price
                    data['b'][0],  # bid price
                    data['c'][0],  # last trade
                    data['p'][0],  # wvap
                    data['t'][1],  # number of trades in 24h
                    data['l'][0],  # day low
                    data['h'][0],  # day high
                    data['o']      # day open
                ))
                conn.commit()
            # print(f"Ticker {ticker} inserted.")
            return ticker
        else:
            print(f"Data not found {ticker}")
    else:
        print(f"Error fetching data: {response.status_code}")
    
    return None

def fetch_and_store_full_data(ticker):
    url = "https://api.kraken.com/0/public/Ticker"
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers, params={'pair': ticker})
    
    if response.status_code == 200:
        data = response.json().get("result", {}).get(ticker)
        
        if data:
            # Check if data already exists in Full_Data table
            with conn.cursor() as cursor:
                cursor.execute('SELECT COUNT(*) FROM Full_Data WHERE symbol = %s', (ticker,))
                count = cursor.fetchone()[0]
                
                if count == 0:
                    cursor.execute('''
                        INSERT INTO Full_Data (symbol, ask_price, bid_price, last_trade, wvap, trades_24h, day_low, day_high, day_open)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        ticker,
                        data['a'][0],  # ask price
                        data['b'][0],  # bid price
                        data['c'][0],  # last trade
                        data['p'][0],  # wvap
                        data['t'][1],  # number of trades in 24h
                        data['l'][0],  # day low
                        data['h'][0],  # day high
                        data['o']      # day open
                    ))
                    conn.commit()
                    print(f"Inserted {ticker} into Full_Data table.")
                else: 
                    print(f"{ticker} already exists.")
        else:
            print(f"Data not found for {ticker}")
    else:
        print(f"Error fetching data: {response.status_code}")
    
    return None

def fetch_and_store_Single_Stock_Data(ticker):
    url = "https://api.kraken.com/0/public/Ticker"
    headers = {'Accept': 'application/json'}
    response = requests.get(url, headers=headers, params={'pair': ticker})
    
    if response.status_code == 200:
        data = response.json().get("result", {}).get(ticker)
        
        if data:
            with conn.cursor() as cursor:
                cursor.execute('''
                    INSERT INTO Single_Stock_Data (symbol, ask_price, bid_price, last_trade, wvap)
                    VALUES (%s, %s, %s, %s, %s)
                ''', (
                    ticker,                        
                    data['a'][0],  # ask price
                    data['b'][0],  # bid price
                    data['c'][0],  # last trade
                    data['p'][0]   # wvap
                ))
                conn.commit()
                print(f"Data for {ticker} successfully stored in Single_Stock_Data.")
        else:
            print(f"Data not found for {ticker}")
    else:
        print(f"Error fetching data: {response.status_code}")
