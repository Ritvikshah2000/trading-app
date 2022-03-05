import sqlite3
connection = sqlite3.connect('app.db') # connect to db   

cursor = connection.cursor() # cursor is used to excute sql queries

#execute queries on db to create tables
cursor.execute("CREATE TABLE stock (id INTEGER PRIMARY KEY, symbol TEXT NOT NULL UNIQUE, name TEXT NOT NULL)")
cursor.execute("CREATE TABLE stock_price (id INTEGER PRIMARY KEY, stock_id INTEGER, date NOT NULL, open NOT NULL, high NOT NULL, low NOT NULL, close NOT NULL, volume NOT NULL, FOREIGN KEY (stock_id) REFERENCES stock (id))")

connection.commit() #commit changes to db