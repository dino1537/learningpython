import os
import requests
from rich.console import Console
from rich.tree import Tree
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
from newspaper import Article
import webbrowser
import nltk


console = Console()
# Download the punkt tokenizer
nltk.download('punkt')

DELAY = 1  # delay between requests in seconds

@lru_cache(maxsize=128)
def fetch_articles(topic, api_key, num_articles=5):
    api_url = f"https://content.guardianapis.com/search?q={topic}&api-key={api_key}&page-size={num_articles}&order-by=newest"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch articles for {topic}. Status code: {response.status_code}")
        return []
    
    data = response.json()
    articles = [{"Title": article["webTitle"], "URL": article["webUrl"]} for article in data["response"]["results"]]
    return articles

def read_article(url):
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()

    console.print(f"\nTitle: [bold cyan]{article.title}[/bold cyan]")
    console.print(f"Authors: [bold cyan]{', '.join(article.authors)}[/bold cyan]")
    console.print(f"Publication Date: [bold cyan]{article.publish_date}[/bold cyan]")
    console.print(f"\nText: [bold cyan]{article.text}[/bold cyan]")
    console.print(f"\nSummary: [bold yellow]{article.summary}[/bold yellow]")
    console.print(f"\nKeywords: [bold green]{', '.join(article.keywords)}[/bold green]")

def main(topics):
    api_key = os.getenv("GUARDIAN_API_KEY")

    all_articles = {}
    with ThreadPoolExecutor(max_workers=5) as executor:
        future_to_topic = {executor.submit(fetch_articles, topic, api_key): topic for topic in topics}
        for future in as_completed(future_to_topic):
            topic = future_to_topic[future]
            try:
                all_articles[topic] = future.result()
            except Exception as exc:
                print(f"An error occurred while fetching articles for {topic}: {exc}")

    console = Console()
    tree = Tree(":newspaper: Articles", style="bold yellow", guide_style="bold blue")

    for topic, articles in all_articles.items():
        topic_branch = tree.add(f":bookmark_tabs: [bold magenta]{topic}[/bold magenta]")
        for article in articles:
            topic_branch.add(f':link: [link={article["URL"]}]{article["Title"]}[/link]')

    console.print(tree)

    url = input("\nPlease enter the URL of the article you want to read: ")
    read_article(url)

    open_in_browser = input("\nDo you want to open the article in your web browser? (yes/no): ")
    if open_in_browser.lower() == "yes":
        webbrowser.open(url)

if __name__ == "__main__":
    topics = ["India", "Poltics", "Arsenal", "Cricket", "Science", "Technology", "World"]
    main(topics)
