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

PATH_TO_DB_WITH_MODEL_PRED = path_constants.PATH_TO_DB_WITH_MODEL_PREDICTIONS

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

    try:
        
        df = pd.read_csv(PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS, usecols=columns)
    except FileNotFoundError:
        print("Most Active Stock Data File Not Found try fixing the data sourcing and storage function.")
        raise FileNotFoundError

    return df

# Start with microsoft stock as base stock and use it to populate price data fo all other stocks
# If Microsoft data in invalid format, update the base stock with that of the current stock being populated and store the data
# This solution not meant to be comprehensive as some data loss for the test mode is tolerable.
def generate_price_data_and_populate_db(ticker_listing_data):
    stock_with_data = "MSFT"
    symbolInfo = yf.Ticker(stock_with_data)
    
    price_data = symbolInfo.history(period="max")
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)

    for index in ticker_listing_data.index:
        symbol = ticker_listing_data["Symbol"][index]
          
        if len(price_data)  > 1:
            
            price_data.to_sql(symbol, con=engine, if_exists="replace", index=True)
            
        else:
            symbolInfo = yf.Ticker(symbol)
            price_data = symbolInfo.history(period="max")
            
            
            price_data.to_sql(symbol, con=engine, if_exists="replace", index=True)
            
        
    engine.dispose()


def add_single_stock_price_data_to_db(ticker_listing_data, index):
    symbol = ticker_listing_data["Symbol"][index]

    symbolInfo = yf.Ticker(symbol)
    price_data = symbolInfo.history(period="max")
    
    if len(price_data)  > 1:
        engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)
        
        price_data.to_sql(symbol, con=engine, if_exists="replace", index=True)
        
        engine.dispose()


def get_price_data_and_populate_db(ticker_listing_data):
   
    for index in ticker_listing_data.index:
            add_single_stock_price_data_to_db(ticker_listing_data, index)

        

def populate_db_with_most_active_stocks():
    df = get_most_active_stocks_as_dataframe()
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_MOST_ACTIVE_STOCKS, echo=False)
    
    df.to_sql(MOST_ACTIVE_STOCKS_TABLE_NAME, con=engine, if_exists="replace", index=False)
    
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


def get_tickers_as_associative_container(path_to_db) -> dict:
    ticker_dict = {}
    tickers = get_list_of_tickers_in_db(path_to_db)
    
    for ticker in tickers:
        ticker_dict[ticker] = ticker
        
    return ticker_dict
    
    
    
def get_table_matching_ticker(ticker: str) -> pd.DataFrame:
    
    query = "SELECT * FROM " + f"'{ticker}'"
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)
    
    price_data = pd.read_sql(query, engine)
    
    return price_data
    

def get_date_and_close_price_data_macthing_ticker(ticker: str) -> pd.DataFrame:
    
    query = "SELECT Date, Close FROM " + f"'{ticker}'"
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)
    
    price_data = pd.read_sql(query, engine)
    
    return price_data


def get_all_price_data_mapped_to_ticker() -> dict:
    ticker_price_data_map = {}
    
    all_tickers = get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)
    
    for ticker in all_tickers:
        ticker_price_data_map[ticker] = get_table_matching_ticker(ticker)
        
    return ticker_price_data_map


def get_most_recent_price(ticker: str) -> pd.DataFrame:
    
    query = f"SELECT CLOSE FROM '{ticker}' order by rowid DESC LIMIT 1"
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_PRICE_DATA, echo=False)
    
    price_data = pd.read_sql(query, engine)

    return price_data["Close"][0]
        

def get_price_pred(ticker):
    query = f"SELECT todays_predicted_close_price, price_prediction_date, price_prediction_mean_absolute_percentage_error FROM predictions WHERE ticker = '{ticker}'"
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_MODEL_PRED, echo=False)
    
    price_data = pd.read_sql(query, engine)
    
    return [price_data["todays_predicted_close_price"][0]], price_data["price_prediction_date"][0], price_data["price_prediction_mean_absolute_percentage_error"][0]


def get_adj_pred_close_price(ticker):
    query = f"SELECT adjusted_close_price_based_on_sentiment FROM predictions WHERE ticker = '{ticker}'"
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_MODEL_PRED, echo=False)
    
    price_data = pd.read_sql(query, engine)
    
    return price_data["adjusted_close_price_based_on_sentiment"][0]


def get_pred_price_mov_score(ticker):
    query = f"SELECT predicted_price_movement_score FROM predictions WHERE ticker = '{ticker}'"
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_MODEL_PRED, echo=False)
    
    price_data = pd.read_sql(query, engine)
    
    return price_data["predicted_price_movement_score"][0]



    
if __name__ == "__main__":
    a = get_price_pred("MSFT")
    b = get_adj_pred_close_price("MSFT")
    c = get_pred_price_mov_score("MSFT")
    
    print(a, b, c)