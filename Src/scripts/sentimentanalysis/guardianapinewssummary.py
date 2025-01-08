import sys
import os
import requests
import time
from typing import List, Dict

# Uncomment below to use api key from file
# from api_tools import read_api_key_from_file

# # Get current file path
# CURRENT_FILE_DIR = os.path.abspath(__file__)

# # Get root dir
# MODULE_DIR = os.path.abspath(f"{CURRENT_FILE_DIR}/../../")

# sys.path.append(MODULE_DIR)
    
# import Src.scripts.path_constants as path_constants

# # Change directory to that of path constants since all paths are declared relative to it
# os.chdir(os.path.dirname(os.path.abspath("Src\scripts\path_constants.py")))

# PATH_TO_GUARDIAN_NEWS_API_KEY = path_constants.PATH_TO_GUARDIAN_NEWS_API_KEY

# API_KEY = read_api_key_from_file(PATH_TO_GUARDIAN_NEWS_API_KEY)

API_KEY = "Enter your api key"


def get_finance_news(api_key: str, companies: List[str], from_date: str, page_size: int = 50) -> Dict[str, List[Dict]]:
    base_url = "https://content.guardianapis.com/search"
    news_by_company = {}

    for company in companies:
        params = {
            'api-key': api_key,
            'q': company,
            'section': 'business',
            'from-date': from_date,
            'page-size': page_size,
            'show-fields': 'headline,trailText'
        }

        response = requests.get(base_url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            articles = data['response']['results']
            news_by_company[company] = articles
        else:
            print(f"Error fetching news for {company}: {response.status_code}")
        
        # Be nice to the API and avoid rate limiting
        time.sleep(1)

    return news_by_company

# List of S&P 500 companies (a subset for demonstration)
companies = [
    'Apple', 'Microsoft', 'Amazon', 'Alphabet', 'Meta Platforms',
    'Tesla', 'Berkshire Hathaway', 'NVIDIA', 'JPMorgan Chase', 'Johnson & Johnson'
]

# Generic date (1 year ago from an arbitrary date)
from_date = '2023-07-09'

news = get_finance_news(API_KEY, companies, from_date)

# Debug: Print the structure of the first article for the first company
for company, articles in news.items():
    if articles:
        print(f"\nDebug: First article structure for {company}:")
        print(articles[0])
        break  # Only print for the first company

# Print results
for company, articles in news.items():
    print(f"\nNews for {company}:")
    for article in articles:
        # Access headline and summary from 'fields'
        headline = article.get('fields', {}).get('headline', 'No headline available')
        summary = article.get('fields', {}).get('trailText', 'Summary not available')
        
        # Access date directly from the article dictionary
        date = article.get('webPublicationDate', 'Date not available')

        print(f"- {headline}")
        print(f"  Date: {date}")
        print(f"  Summary: {summary}")
        print()