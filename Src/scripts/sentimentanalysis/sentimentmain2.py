
import requests
from transformers import pipeline

API_key = 'enter api key here'
keyword = 'gold'
date = '2024-08-28'

pipe = pipeline("text-classification", model="ProsusAI/finbert")

url = (f"http://newsapi.org/v2/everything?"
       f'q={keyword}&'
       f'from={date}&'
       'sortBy=popularity&'
       f'apiKey={API_key}'
       )

response = requests.get(url)

# Check for errors in the response
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.json())  # Print the error message
else:
    data = response.json()
    articles = data.get("articles", [])
    
    if not articles:
        print("No articles found.")
    else:
        total_score = 0
        num_articles = 0

        for i, article in enumerate(articles):
            if keyword.lower() not in article.get("description", "").lower():
                continue

            print(f'Title: {article["title"]}')
            print(f'Link: {article["url"]}')
            print(f'Published: {article["publishedAt"]}')

            sentiment = pipe(article["content"])[0]

            print(f"Sentiment: {sentiment['label']}, Score: {sentiment['score']}")
            print("-" * 40)

            if sentiment["label"] == "positive":
                total_score += sentiment["score"]
                num_articles += 1
            elif sentiment["label"] == "negative":
                total_score -= sentiment["score"]
                num_articles += 1

        if num_articles > 0:
            final_score = total_score / num_articles
            print(f"Overall Sentiment: {'Positive' if final_score >= 0.15 else 'Negative' if final_score <= -0.15 else 'Neutral'} {final_score}")
        else:
            print("No relevant articles found.")
