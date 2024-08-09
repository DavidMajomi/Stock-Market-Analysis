import os
import requests
import yfinance as yf
import pandas as pd
import sqlite3
from sqlalchemy import create_engine
from get_stock_data import get_list_of_tickers_in_db
import path_constants
import time


PATH_TO_DB_WITH_YF_NEWS = path_constants.PATH_TO_DB_WITH_YF_NEWS
PATH_TO_DB_PRICE_DATA = path_constants.PATH_TO_DB_PRICE_DATA
PATH_TO_DB_WITH_NEWS_API_ORG_NEWS = path_constants.PATH_TO_DB_WITH_NEWS_API_ORG_NEWS

PATH_TO_NEWS_API_ORG_API_KEY = path_constants.PATH_TO_NEWS_API_ORG_API_KEY
NEWS_API_TOP_BUSINESS_HEADLINES_TABLE_NAME = path_constants.NEWS_API_TOP_BUSINESS_HEADLINES_TABLE_NAME


def read_api_key_from_file(path_to_file : str) -> str:
    if os.path.exists(path_to_file):
        with open(path_to_file, "r") as file:
            api_key = file.readline()
    else:
        raise Exception("File with api key does not exist")
    
    return api_key 


def get_and_store_all_s_and_p_news_from_yfinance_in_DB():
    list_of_tickers = get_list_of_tickers_in_db(PATH_TO_DB_PRICE_DATA)
    
    for ticker in list_of_tickers:
        time.sleep(0.0625)
        
        data = yf.Ticker(ticker)
        
        if(data.news ):
            
            df = pd.DataFrame.from_dict(data.news)
            
            if "thumbnail" in df.columns:
                columns = ["thumbnail"]
                
                
                df = df.drop(columns, axis=1)
            
            df["relatedTickers"] = df["relatedTickers"].astype(str)
            
            engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_YF_NEWS, echo=False)
            
            df.to_sql(ticker, con=engine, if_exists="replace", index=True)
            
            engine.dispose()
            
        

def get_and_store_news_api_org_todays_top_business_headlines():
    key = read_api_key_from_file(PATH_TO_NEWS_API_ORG_API_KEY)
    url = f"https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey={key}"
    
    data = requests.get(url)
    data = data.json()
    
    df = pd.DataFrame.from_dict(data["articles"])
    
    df["source"] = df["source"].astype(str)
    df = df.drop(["urlToImage"], axis=1)
    
    
    engine = create_engine("sqlite:///" + PATH_TO_DB_WITH_NEWS_API_ORG_NEWS, echo=False)
            
    df.to_sql(NEWS_API_TOP_BUSINESS_HEADLINES_TABLE_NAME, con=engine, if_exists="replace", index=True)
    
    engine.dispose()
    
    