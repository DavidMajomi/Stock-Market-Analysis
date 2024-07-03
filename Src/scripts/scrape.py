import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import path_constants

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
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    
    url='https://finance.yahoo.com/most-active/'
    response=requests.get(url,headers=headers)

    soup=BeautifulSoup(response.content,'lxml')
    
    most_active_stocks_by_order = []
    
    for item in soup.select('.simpTblRow'):
        symbol = item.select('[aria-label=Symbol]')[0].get_text()
        Name = item.select('[aria-label=Name]')[0].get_text()
        price = item.select('[aria-label*=Price]')[0].get_text()
        change = item.select('[aria-label=Change]')[0].get_text()
        percent_change = item.select('[aria-label="% Change"]')[0].get_text()
        Volume = item.select('[aria-label="Volume"]')[0].get_text()
        avg_vol_3_month = item.select('[aria-label="Avg Vol (3 month)"]')[0].get_text()
        mkt_cap = item.select('[aria-label="Market Cap"]')[0].get_text()
        pe_ratio = item.select('[aria-label="PE Ratio (TTM)"]')[0].get_text()

        ticker = {
            "symbol" : symbol,
            "Name" : Name,
            "price" : price,
            "change" : change,
            "percent_change" : percent_change,
            "Volume" : Volume,
            "avg_vol_3_month" : avg_vol_3_month,
            "mkt_cap" : mkt_cap,
            "pe_ratio" : pe_ratio
        }
        
        most_active_stocks_by_order.append(ticker)
        
        df = pd.DataFrame(most_active_stocks_by_order)
        df.to_csv(PATH_TO_CSV_WITH_MOST_ACTIVE_STOCKS, index=False)
        
    