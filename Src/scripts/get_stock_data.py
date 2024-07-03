import os
import pandas as pd
import yfinance as yf
import path_constants
import sqlite3
from sqlalchemy import create_engine

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH_TO_DB_DIR = path_constants.PATH_TO_DB_DIR
PATH_TO_DB_PRICE_DATA = path_constants.PATH_TO_DB_PRICE_DATA
PATH_TO_CSV_WITH_S_AND_P_DATA = path_constants.PATH_TO_CSV_WITH_S_AND_P_DATA
PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS = path_constants.PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS
PATH_TO_DB_PRICE_DATA = path_constants.PATH_TO_DB_PRICE_DATA
PATH_TO_DB_WITH_MOST_ACTIVE_STOCKS = path_constants.PATH_TO_DB_WITH_MOST_ACTIVE_STOCKS
MOST_ACTIVE_STOCKS_TABLE_NAME = path_constants.MOST_ACTIVE_STOCKS_TABLE_NAME

def get_S_and_p_ticker_and_listing_data_as_dataframe() -> pd.DataFrame:
        
    columns = ["Symbol", "Date added"]
    
    df = pd.read_csv(PATH_TO_CSV_WITH_S_AND_P_DATA, usecols=columns)

    return df


def get_most_active_stocks_as_dataframe() -> pd.DataFrame:
        
    columns = [
        "symbol",
        "Name",
        "price",
        "change",
        "percent_change",
        "Volume",
        "avg_vol_3_month",
        "mkt_cap",
        "pe_ratio"
    ]

    
    df = pd.read_csv(PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS, usecols=columns)

    return df


def get_price_data_and_populate_db(ticker_listing_data):
    
    for index in ticker_listing_data.index:
  
        symbol = ticker_listing_data["Symbol"][index]

        symbolInfo = yf.Ticker(symbol)
        price_data = symbolInfo.history(period="max")

        engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)
        
        price_data.to_sql(symbol, con=engine, if_exists="replace", index=True)
        
        engine.dispose()
        

def populate_db_with_most_active_stocks():
    df = get_most_active_stocks_as_dataframe()
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_MOST_ACTIVE_STOCKS, echo=False)
    
    df.to_sql(MOST_ACTIVE_STOCKS_TABLE_NAME, con=engine, if_exists="replace", index=True)
    
    engine.dispose()
    
    
    
def get_list_of_tickers_in_db(path_to_db) -> list:
    query = """SELECT name FROM sqlite_master 
    WHERE type='table';"""
    
    conn = sqlite3.connect(path_to_db)
    cur = conn.cursor()
    cur.execute(query)
    
    data = (cur.fetchall())
    
    # Convert list of tuples to list of ticker values as str
    for i in range(len(data)):
        data[i] = data[i][0]
        
    return data
    
    
def get_table_matching_ticker(ticker: str) -> pd.DataFrame:
    
    query = "SELECT * FROM " + ticker
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)
    
    price_data = pd.read_sql(query, engine)
    
    return price_data
    

def get_date_and_close_price_data_macthing_ticker(ticker: str) -> pd.DataFrame:
    
    query = "SELECT Date, Close FROM " + ticker
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)
    
    price_data = pd.read_sql(query, engine)
    
    return price_data
