import os
import sqlite3
import alpaca_trade_api as tradeapi

from dotenv import load_dotenv

#import env vars
load_dotenv()
api_key = os.getenv("api_key")
secret_api_key = os.getenv("secret_api_key")
domain = os.getenv("domain")

connection = sqlite3.connect('app.db')

connection.row_factory = sqlite3.Row
cursor = connection.cursor()
cursor.execute("SELECT id, symbol, name FROM stock")

rows = cursor.fetchall() #fetch price data

symbols = []
stock_dict = {}
for row in rows:
    symbol = row['symbol']
    symbols.append(symbol)
    stock_dict[symbol] = row['id']

api = tradeapi.REST(api_key,secret_api_key, base_url=domain)

chunk_size = 200 #loop in terms of chunks of 200
for i in range(0,len(symbols), chunk_size): #loop through all symbols in steps of 200
    symbol_chunk = symbols[i:i+chunk_size] #increment by chunksize

    barsets = api.get_barset(symbol_chunk, 'day') #get barsets for each chunk by day
 
    for symbol in barsets:
        print(f"processing symbol {symbol}")    
        for bar in barsets[symbol]:
            stock_id = stock_dict[symbol] #insert data into db
            cursor.execute("INSERT INTO stock_price (stock_id, date, open, high, low, close, volume) VALUES (?,?,?,?,?,?,?)", (stock_id, bar.t.date(), bar.o, bar.h, bar.l, bar.c, bar.v))

connection.commit()