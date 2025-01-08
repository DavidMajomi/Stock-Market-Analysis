import requests
import time
from typing import List, Dict
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

API_KEY = 'enter your API key here'

# STOCK PRICES

def get_stock_data(symbol: str, api_key: str) -> Dict:
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "apikey": api_key,
        "outputsize": "full"
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching stock data for {symbol}: {response.status_code}")
        return None

def get_news_sentiment(symbols: List[str], api_key: str) -> Dict:
    base_url = "https://www.alphavantage.co/query"
    params = {
        "function": "NEWS_SENTIMENT",
        "tickers": ",".join(symbols),
        "apikey": api_key,
        "sort": "RELEVANCE"
    }
    
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching news sentiment: {response.status_code}")
        return None

def process_stock_data(data: Dict) -> pd.DataFrame:
    if not data or "Time Series (Daily)" not in data:
        return None
    
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient='index')
    df.index = pd.to_datetime(df.index)
    df = df.astype(float)
    df.columns = ['open', 'high', 'low', 'close', 'volume']
    return df.sort_index()

def process_news_sentiment(data: Dict) -> pd.DataFrame:
    if not data or "feed" not in data:
        return None
    
    news_data = []
    for article in data["feed"]:
        news_data.append({
            "time_published": article["time_published"],
            "title": article["title"],
            "summary": article["summary"],
            "overall_sentiment_score": article["overall_sentiment_score"],
            "overall_sentiment_label": article["overall_sentiment_label"],
            "relevance_score": article.get("ticker_sentiment", [{}])[0].get("relevance_score", "N/A"),
            "ticker": article.get("ticker_sentiment", [{}])[0].get("ticker", "N/A"),
        })
    
    df = pd.DataFrame(news_data)
    df['time_published'] = pd.to_datetime(df['time_published'])
    return df.sort_values('time_published', ascending=False)

# List of S&P 500 companies (a subset for demonstration)
companies = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META',
    'TSLA', 'BRK.A', 'NVDA', 'JPM', 'JNJ'
]

# Fetch and process stock data
stock_data = {}
for symbol in companies:
    data = get_stock_data(symbol, API_KEY)
    if data:
        stock_data[symbol] = process_stock_data(data)
    time.sleep(12)  # To respect Alpha Vantage's rate limit of 5 calls per minute

# Fetch and process news sentiment
news_data = get_news_sentiment(companies, API_KEY)
news_df = process_news_sentiment(news_data)

# Print some results
for symbol, df in stock_data.items():
    if df is not None:
        print(f"\nStock data for {symbol}:")
        print(df.tail())  # Print the last 5 days of stock data

if news_df is not None:
    print("\nRecent news sentiment:")
    print(news_df.head())  # Print the 5 most recent news articles with sentiment

# You can now use stock_data and news_df for further analysis and model building

# NEWS SENTIMENT 

def process_news_sentiment(data: Dict) -> pd.DataFrame:
    if not data or "feed" not in data:
        print("No valid data to process for news sentiment")
        return None
    
    news_data = []
    for article in data["feed"]:
        news_item = {
            "time_published": article.get("time_published", "N/A"),
            "title": article.get("title", "N/A"),
            "overall_sentiment_score": article.get("overall_sentiment_score", "N/A"),
            "overall_sentiment_label": article.get("overall_sentiment_label", "N/A"),
        }
        
        # Process ticker sentiments
        for ticker_info in article.get("ticker_sentiment", []):
            ticker = ticker_info.get("ticker")
            if ticker:
                news_item[f"{ticker}_relevance"] = ticker_info.get("relevance_score", "N/A")
                news_item[f"{ticker}_sentiment_score"] = ticker_info.get("ticker_sentiment_score", "N/A")
                news_item[f"{ticker}_sentiment_label"] = ticker_info.get("ticker_sentiment_label", "N/A")
        
        news_data.append(news_item)
    
    df = pd.DataFrame(news_data)
    df['time_published'] = pd.to_datetime(df['time_published'], format='%Y%m%dT%H%M%S', errors='coerce')
    return df.sort_values('time_published', ascending=False)

def safe_float_convert(x):
    try:
        return float(x)
    except (ValueError, TypeError):
        return np.nan

# After fetching the data
news_df = process_news_sentiment(news_data)

if news_df is not None:
    print("\nRecent news sentiment:")
    print(news_df[['time_published', 'title', 'overall_sentiment_label']].head())

    # Analyze sentiment for specific stocks
    companies = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META']
    for company in companies:
        relevance_col = f'{company}_relevance'
        sentiment_score_col = f'{company}_sentiment_score'
        sentiment_label_col = f'{company}_sentiment_label'
        
        if relevance_col in news_df.columns and sentiment_score_col in news_df.columns:
            company_data = news_df[[relevance_col, sentiment_score_col, sentiment_label_col]].copy()
            company_data[relevance_col] = company_data[relevance_col].apply(safe_float_convert)
            company_data[sentiment_score_col] = company_data[sentiment_score_col].apply(safe_float_convert)
            company_data = company_data.dropna()
            
            if not company_data.empty:
                avg_sentiment = company_data[sentiment_score_col].mean()
                avg_relevance = company_data[relevance_col].mean()
                print(f"\nAnalysis for {company}:")
                print(f"Average sentiment score: {avg_sentiment:.4f}")
                print(f"Average relevance score: {avg_relevance:.4f}")
                print("Most recent sentiment data:")
                print(company_data.head())
            else:
                print(f"\nNo valid sentiment data available for {company}")
        else:
            print(f"\nNo sentiment data columns found for {company}")

else:
    print("Failed to process news sentiment data")