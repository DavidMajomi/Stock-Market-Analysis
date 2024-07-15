import yfinance as yf
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from get_stock_data import get_list_of_tickers_in_db
import path_constants

PATH_TO_DB_WITH_YF_NEWS = path_constants.PATH_TO_DB_WITH_YF_NEWS
PATH_TO_DB_PRICE_DATA = path_constants.PATH_TO_DB_PRICE_DATA

def get_all_s_and_p_news_from_yfinance():
    list_of_tickers = get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)
    
    for ticker in list_of_tickers:
            data = yf.Ticker(ticker)
            
            df = pd.DataFrame.from_dict(data.news)
            
            columns = ["thumbnail"]
            
            df = df.drop(columns, axis=1)
            
            df["relatedTickers"] = df["relatedTickers"].astype(str)
            
            engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_YF_NEWS, echo=False)
            
            df.to_sql(ticker, con=engine, if_exists="replace", index=True)
            
            engine.dispose()
            
        
        
get_all_s_and_p_news_from_yfinance()