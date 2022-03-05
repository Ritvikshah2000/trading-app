import sqlite3

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

#delete tables
cursor.execute("DROP TABLE stock_price")
cursor.execute("DROP TABLE stock")

connection.commit()