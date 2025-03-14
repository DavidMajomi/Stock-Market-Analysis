import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import path_constants
from io import StringIO

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PATH_TO_CSV_WITH_S_AND_P_DATA = path_constants.PATH_TO_CSV_WITH_S_AND_P_DATA
PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS = path_constants.PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS


def get_s_and_p_info():
    
    link = (
        "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies#S&P_500_component_stocks"
    )
    df = pd.read_html(link, header=0)[0]

    # Write to CSV
    df.to_csv(PATH_TO_CSV_WITH_S_AND_P_DATA, index=False)
    

def get_most_active_stocks_from_yfinance():
    
    try:
        
        headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
        
        url='https://finance.yahoo.com/most-active/'
        response=requests.get(url,headers=headers)

        
        html = response.text
        
        dataframes = pd.read_html(StringIO(html))
        df = dataframes[0]
        
        df.drop(columns=["52 Wk Range", "Unnamed: 2"], inplace=True)
        
        
        price_list = df["Price"].to_list()

        for i in range(len(price_list)):
            temp = price_list[i]
            first_space_in_str = temp.find(' ')
            price_list[i] = temp[0:first_space_in_str]
            
            
        Price = pd.Series(price_list)
        # print(Price)

        # df.replace({'Price': Price})
        df["Price"] = Price
        
        df.rename(columns={
            'Symbol': 'symbol', 
            'Change %': 'percent_change', 
            'Avg Vol (3M)': 'avg_vol_3_month', 
            "Price" : "price",
            "Change" : "change",
            "Market Cap": "mkt_cap", 
            "P/E Ratio (TTM)" : "pe_ratio", 
            "52 Wk Change %" : "52_wk_percent_change"
            }, inplace=True)
        
        df.to_csv(PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS, index=False)
        
    except requests.exceptions.Timeout:
        print("The request timed out.")
    except requests.exceptions.HTTPError as errh:
        print(f"HTTP error occurred: {errh}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except PermissionError:
        print("Permission error. Please check the file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


    
if __name__ == '__main__':
    # get_yfinace_using_pandas_scraping()
    get_most_active_stocks_from_yfinance()
    
    