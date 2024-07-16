import os

from scrape import get_s_and_p_info, get_most_active_stocks_from_yfinance
from get_stock_data import get_S_and_p_ticker_and_listing_data_as_dataframe, get_price_data_and_populate_db, populate_db_with_most_active_stocks
from get_stock_news import get_and_store_all_s_and_p_news_from_yfinance_in_DB, get_and_store_news_api_org_todays_top_business_headlines

os.chdir(os.path.dirname(os.path.abspath(__file__)))


# os.chdir("Src/scripts")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_all_required_data() -> None:
        
    print("Getting S & P info")
    get_s_and_p_info()
    print("Done")

    print("getting current most active stocks")
    get_most_active_stocks_from_yfinance()
    print("Done")
    
    print("Populating Db with most active stocks")
    populate_db_with_most_active_stocks()
    print("Done")
    
    print("Getting all s and p news from yfinance")
    get_and_store_all_s_and_p_news_from_yfinance_in_DB()
    print("Done")
    
    print("Getting top business headlines from newsapi.org")
    get_and_store_news_api_org_todays_top_business_headlines()
    print("Done")
        
    print("Getting Price Data and Populating Database")
    ticker_listing_data = get_S_and_p_ticker_and_listing_data_as_dataframe()
    get_price_data_and_populate_db(ticker_listing_data)
    print("Done")

