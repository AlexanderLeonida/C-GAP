from data import conn
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model
import numpy as np

df = pd.read_sql('SELECT * FROM BTC_Data', con=conn)
last_trade_df = df.sort_values(by='ask_price', ascending=False)


# tckerInput = input("Enter ticker containing: ")
# tcker = tckerInput.upper()
tcker = 'BTC'
print(f"Searching for symbols containing: {tcker}")

btc_df = last_trade_df[last_trade_df['symbol'].str.contains(tcker, case=False, na=False)]

btc_df = btc_df.sort_values(by='ask_price', ascending=False)

if btc_df.empty:
    print("No matching symbols found.")
else:
    sns.scatterplot(y='symbol', x='last_trade', data=btc_df)
    plt.xticks(rotation=90)
    plt.title(f'Scatterplot of Last Trades for Symbols Containing "{tcker}" (Ordered by Last Trade)')
    plt.show()
