import os
import threading
from scrape import get_s_and_p_info, get_most_active_stocks_from_yfinance
from get_stock_data import get_S_and_p_ticker_and_listing_data_as_dataframe, get_price_data_and_populate_db, populate_db_with_most_active_stocks
from get_stock_news import get_and_store_all_s_and_p_news_from_yfinance_in_DB, get_and_store_news_api_org_todays_top_business_headlines

# os.chdir("Src/scripts")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_s_and_p_data():
    
    ticker_listing_data = get_S_and_p_ticker_and_listing_data_as_dataframe()
    get_price_data_and_populate_db(ticker_listing_data)
    print("Done getting Price Data and Populating Database")
    
    
def get_most_active():
    get_most_active_stocks_from_yfinance()
    print("Done getting current most active stocks")
    
    # populate_db_with_most_active_stocks()
    print("Done populating Db with most active stocks")
    

def init_all_required_data() -> None:        
    
    get_s_and_p_info()
    print("Done getting S & P info")

    
    s_and_p_requirements = threading.Thread(target=get_s_and_p_data)

    yf_most_active = threading.Thread(target=get_most_active)

    news_api_headlines = threading.Thread(target=get_and_store_news_api_org_todays_top_business_headlines)
    
    
    s_and_p_requirements.start()
    yf_most_active.start()
    news_api_headlines.start()
    
    
    news_api_headlines.join()
    print("Done getting top business headlines from newsapi.org")
    
    yf_most_active.join()
    s_and_p_requirements.join()
    
    get_and_store_all_s_and_p_news_from_yfinance_in_DB()
    print("Done getting all s and p news from yfinance")
    

    
    
        