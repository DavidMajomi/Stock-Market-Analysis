import requests
import time
from typing import List, Dict

API_KEY = "Enter your api key"

def get_finance_news(api_key: str, companies: List[str], from_date: str, page_size: int = 10) -> Dict[str, List[Dict]]:
    base_url = "https://content.guardianapis.com/search"
    news_by_company = {}

    for company in companies:
        params = {
            'api-key': api_key,
            'q': company,
            'section': 'business',
            'from-date': from_date,
            'page-size': page_size,
            'show-fields': 'headline,body',
            'show-blocks': 'all'
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

# Print results
for company, articles in news.items():
    print(f"\nNews for {company}:")
    for article in articles:
        headline = article.get('fields', {}).get('headline', 'No headline available')
        date = article.get('webPublicationDate', 'Date not available')
        full_text = article.get('fields', {}).get('body', 'Full text not available')

        print(f"- {headline}")
        print(f"  Date: {date}")
        print(f"  Full Text:")
        print(f"  {full_text[:500]}...")  # Print first 500 characters of the full text
        print()

    print(f"Total articles for {company}: {len(articles)}")
    print("-" * 50)