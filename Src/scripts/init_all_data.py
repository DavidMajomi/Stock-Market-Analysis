import os
import time
import multiprocessing
from dotenv import load_dotenv
from scrape import get_s_and_p_info, get_most_active_stocks_from_yfinance
import get_stock_data
from get_stock_data import get_S_and_p_ticker_and_listing_data_as_dataframe, populate_db_with_most_active_stocks
from get_stock_news import get_and_store_all_s_and_p_news_from_yfinance_in_DB, get_and_store_news_api_org_todays_top_business_headlines

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def get_s_and_p_data(testing_mode):
    
    ticker_listing_data = get_S_and_p_ticker_and_listing_data_as_dataframe()
    
    if testing_mode:
        start = time.time()
        get_stock_data.generate_price_data_and_populate_db(ticker_listing_data)
        end = time.time()
        
        print(f"Time to generate price data = {(end - start)/60} Minutes")
    else:
        get_stock_data.get_price_data_and_populate_db(ticker_listing_data)
        
    print("Done getting Price Data and Populating Database")
    
    
def get_most_active():
    get_most_active_stocks_from_yfinance()
    print("Done getting current most active stocks")
    
    populate_db_with_most_active_stocks()
    print("Done populating Db with most active stocks")
    

def init_all_required_data() -> None:        
    true_false_dict = {
        "True" : True,
        "TRUE" : True,
        "true" : True,
        "False" : False,
        "FALSE" : False,
        "false" : False
    }
    
    load_dotenv(override=True)
    testing_mode = true_false_dict[os.getenv("TESTING_MODE")]
    print(f"Testing Mode: {testing_mode}")
    
    
    get_s_and_p_info()
    print("Done getting S & P info")

    
    s_and_p_requirements = multiprocessing.Process(target=get_s_and_p_data, args=(testing_mode,))

    yf_most_active = multiprocessing.Process(target=get_most_active)

    news_api_headlines = multiprocessing.Process(target=get_and_store_news_api_org_todays_top_business_headlines)
    
    
    s_and_p_requirements.start()
    yf_most_active.start()
    news_api_headlines.start()
    
    
    news_api_headlines.join()
    print("Done getting top business headlines from newsapi.org")
    
    yf_most_active.join()
    print("Done getting Yfinance most active stocks")
    
    s_and_p_requirements.join()
    
    if not testing_mode:
        get_and_store_all_s_and_p_news_from_yfinance_in_DB()
        print("Done getting all s and p news from yfinance")
    
    print("Done")    
        
if __name__ == "__main__":
    init_all_required_data()