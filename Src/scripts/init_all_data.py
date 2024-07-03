import os
from scrape import get_s_and_p_info
from get_stock_data import get_S_and_p_ticker_and_listing_data_as_dataframe, get_price_data_and_populate_db

# os.chdir("Src/scripts")
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def init_all_required_data() -> None:
        
    print("Getting S & P info")
    get_s_and_p_info()
    print("Done")

        
    print("Getting Price Data and Populating Database")
    ticker_listing_date = get_S_and_p_ticker_and_listing_data_as_dataframe()
    get_price_data_and_populate_db(ticker_listing_date)
    print("Done")



init_all_required_data()