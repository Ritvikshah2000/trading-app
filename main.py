import sqlite3
import os
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

#import env vars
load_dotenv()
api_key = os.getenv("api_key")
secret_api_key = os.getenv("secret_api_key")
domain = os.getenv("domain")

app = FastAPI() #create instance of class
templates = Jinja2Templates(directory="templates") #load templates from "templates" dir

@app.get("/") # all get requests to / will get route to index
def index(request: Request):
    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()

    cursor.execute("SELECT id, symbol, name FROM stock ORDER BY symbol") # select all stocks

    rows = cursor.fetchall()

    return templates.TemplateResponse("index.html", {"request": request, "stocks": rows})

@app.get("/stock/{symbol}") #all get requests to /stock/symbol will route to stock_detail
def stock_detail(request: Request, symbol):

    connection = sqlite3.connect('app.db')
    connection.row_factory = sqlite3.Row

    cursor = connection.cursor()
    cursor.execute("SELECT id, symbol, name FROM stock WHERE symbol = ?", (symbol,))

    row = cursor.fetchone()

    cursor.execute("SELECT * FROM stock_price WHERE stock_id = ? ORDER BY date DESC ", (row['id'],))

    prices = cursor.fetchall()

    return templates.TemplateResponse("stock_detail.html", {"request": request, "stock": row, "bars": prices})
