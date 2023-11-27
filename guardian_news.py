import requests
from rich import print

# Define your API key from The Guardian API
api_key = 'YOUR_API_KEY'

# Define the topics and the number of articles you want for each
topics = ['India', 'Poltics', 'Arsenal', 'Cricket', 'Science', 'Technology', 'world news']
num_articles = 5

# Initialize an empty dictionary to store the articles
all_articles = {}

# Fetch and store the latest articles for each topic
for topic in topics:
    # Build the API URL
    api_url = f'https://content.guardianapis.com/search?q={topic}&api-key={api_key}&page-size={num_articles}'

    # Make the API request
    response = requests.get(api_url)
    data = response.json()

    # Extract and store the articles
    articles = []
    for article in data['response']['results']:
        articles.append({'Title': article['webTitle'], 'URL': article['webUrl']})
    
    # Store the articles for this topic
    all_articles[topic] = articles

# Format and print the output using rich
for topic, articles in all_articles.items():
    print(f'[bold]{topic} News:[/bold]')
    for article in articles:
        print(f'[link={article["URL"]}]{article["Title"]}[/link]')
    print()

