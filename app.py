from flask import Flask, request, jsonify, render_template
from data import conn, create_table, create_full_data_table, create_BTC_table
from apiGrab import fetch_and_store_ticker_data, fetch_and_store_btc_data
from fuzzywuzzy import process  # to guide users in finding a specific stock
from apscheduler.schedulers.background import BackgroundScheduler #update btc database
import atexit # delete btc database every time server closes


app = Flask(__name__)
scheduler = BackgroundScheduler()

@app.route('/')
def main():
    return render_template('home.html')

# Function to retrieve ticker data from the database
def get_ticker_from_db(symbol):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Ticker WHERE symbol = %s', (symbol,))
        return cursor.fetchone()  # Returns None if ticker is not found

# Function to render the ticker data on the page
def render_ticker_page(row):
    return render_template('index.html', symbol=row[1], ask_price=row[2], bid_price=row[3],
                           last_trade=row[4], wvap=row[5], trades_24h=row[6], day_low=row[7],
                           day_high=row[8], day_open=row[9])

# Function to handle fetching and storing ticker data if not found in the database
def handle_new_ticker(symbol):
    ticker_data = fetch_and_store_ticker_data(symbol)
    
    if ticker_data:
        print(f"Data for {symbol} successfully fetched and stored.")
        row = get_ticker_from_db(symbol)
        return render_ticker_page(row)
    else:
        print(f"Failed to fetch or store data for {symbol}.") 
        return None  # Return None if it fails to fetch data

# Function to suggest similar tickers using fuzzywuzzy
def get_similar_tickers(symbol):
    with conn.cursor() as cursor:
        cursor.execute('SELECT symbol FROM Ticker')
        available_tickers = [row[0] for row in cursor.fetchall()]

    # Use fuzzywuzzy to find close matches
    similar_tickers = process.extract(symbol, available_tickers, limit=5)  # Get top 5 matches
    return [ticker[0] for ticker in similar_tickers]  # Return only the ticker symbols

def update_btc_data_periodically():
    valid_tickers = ['TBTCUSD']
    for ticker in valid_tickers:
        fetch_and_store_btc_data(ticker)

# Function to start the background scheduler for periodic BTC data update
def start_btc_data_scheduler():
    scheduler = BackgroundScheduler()
    # The API updates every minute I think
    scheduler.add_job(update_btc_data_periodically, 'interval', seconds=60)

    scheduler.start()
    return scheduler

def delete_btc_data_table():
    try:
        cursor = conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS BTC_Data')
        conn.commit()
        cursor.close()
        conn.close()
        print("BTC_Data table deleted successfully!")
    except Exception as e:
        print(f"Error deleting table: {e}")

@app.route('/get_ticker', methods=['GET', 'POST'])
def get_ticker():
    if request.method == 'POST':
        symbol = request.form.get('symbol')
        if not symbol:
            return render_template('index.html', error="No symbol entered")

        row = get_ticker_from_db(symbol)
        
        if row:
            return render_ticker_page(row)
        else:
            similar_tickers = get_similar_tickers(symbol)
            # print("Similar tickers are:", similar_tickers)
            # print("Symbol entered:", symbol)

            ticker_page = handle_new_ticker(symbol)
            if ticker_page:
                return ticker_page  
            else:
                error_message = f"Ticker '{symbol}' not found. Did you mean one of these: {', '.join(similar_tickers)}?"
                print(f"Error: {error_message}") 
                return render_template('index.html', error=error_message)
           
    return render_template('index.html')

@app.route('/get_list')
def view_full_data():
    # valid_tickers = fetch_valid_tickers() 
    # This only needs to run the very first time in order to populate the database.
    # If we want to update the values again, we'd need to rerun this. 
    """
    for ticker in valid_tickers:
        fetch_and_store_full_data(ticker)
    """

    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM Full_Data')
        rows = cursor.fetchall()

    return render_template('list.html', tickers=rows)

if __name__ == '__main__':
    create_table()
    create_full_data_table()

    create_BTC_table()
    scheduler = start_btc_data_scheduler()
    atexit.register(delete_btc_data_table)
    app.run(debug=True, host='0.0.0.0', port=5000)
