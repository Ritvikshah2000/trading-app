import os
import sqlite3
import alpaca_trade_api as tradeapi

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

cursor.execute("SELECT symbol, company FROM stock")

rows = cursor.fetchall()
for row in rows:
    print(row)

#connect to api
api = tradeapi.REST(os.environ.get("api_key"),os.environ.get("secret_api_key"), base_url=os.environ.get("domain"))
assets = api.list_assets() #get list of symbols

for asset in assets: #loop through and print all assets 
    try:
        if asset.status == 'active' and asset.tradable:
            cursor.execute("INSERT INTO stock (symbol, company) VALUES (?, ?)", (asset.symbol, asset.name))
    except Exception as e:
        print(asset.symbol)
        print(e)

connection.commit()