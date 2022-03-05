import os
import sqlite3
import alpaca_trade_api as tradeapi

from dotenv import load_dotenv

#scheduling command: 58 15 * * * /Users/ritvikshah/Downloads/Code/trading-app/populate_db.py >> populate.log 2>&1

#import env vars
load_dotenv()
api_key = os.getenv("api_key")
secret_api_key = os.getenv("secret_api_key")
domain = os.getenv("domain")

connection = sqlite3.connect('app.db')
connection.row_factory = sqlite3.Row

cursor = connection.cursor()

cursor.execute("SELECT symbol, name FROM stock") # select all stocks

rows = cursor.fetchall()
symbols = [row['symbol'] for row in rows] # get a list of all symbols

#connect to api
api = tradeapi.REST(api_key,secret_api_key, base_url=domain)
assets = api.list_assets() #get list of symbols (from tradeAPI)

for asset in assets: #loop through and add all assets to db 
    try:
        if asset.status == 'active' and asset.tradable and asset.symbol not in symbols: #only use stocks that are active and tradable
            print(f"Added a new stock {asset.symbol} {asset.name}")
            cursor.execute("INSERT INTO stock (symbol, name) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e: #if there is an issue when trying to add a stock
        print(asset.symbol)
        print(e)

connection.commit()