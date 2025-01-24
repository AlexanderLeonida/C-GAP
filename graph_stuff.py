import io
import base64
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
from data import conn

# Set the Matplotlib backend to 'Agg'
matplotlib.use('Agg')

# Function to retrieve BTC data from the database
def get_btc_data_from_db():
    with conn.cursor() as cursor:
        cursor.execute('SELECT ask_price, bid_price FROM BTC_Data WHERE symbol = "TBTCUSD"')
        return cursor.fetchall()  # Returns a list of tuples containing the data

# Function to generate and return the graph as a base64-encoded string
def generate_btc_data_graph():
    # Retrieve data from the database
    data = get_btc_data_from_db()

    # Check if there is enough data to plot
    if not data or len(data) < 2:
        print("Not enough data to generate the graph.")
        return None

    ask_price = [row[0] for row in data]
    bid_price = [row[1] for row in data]

    # Get the last two data points for y-axis labels
    last_ask_price = ask_price[-2:]
    last_bid_price = bid_price[-2:]

    # Create a seaborn plot
    plt.figure(figsize=(10, 6))
    line1 = sns.lineplot(data=ask_price, label='Ask Price', color='blue')
    line2 = sns.lineplot(data=bid_price, label='Bid Price', color='red')

    plt.title('BTC Data - Price and Trades over Time')
    plt.xlabel('Time (Seconds)')
    plt.ylabel('Value')
    plt.legend()
    plt.tight_layout()

    # Set y-axis ticks to only show the last two values
    y_ticks = sorted(set(last_ask_price + last_bid_price))
    plt.yticks(y_ticks)

    # Save the plot to a BytesIO object and then encode it to base64
    # https://docs.python.org/3/library/base64.html
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')
    
    plt.close()

    return img_base64