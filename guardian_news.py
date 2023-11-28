import os
import requests
from rich.console import Console
from rich.tree import Tree
from rich import box
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed

DELAY = 1  # delay between requests in seconds

@lru_cache(maxsize=128)
def fetch_articles(topic, api_key, num_articles=5):
    api_url = f"https://content.guardianapis.com/search?q={topic}&api-key={api_key}&page-size={num_articles}"
    response = requests.get(api_url)
    
    if response.status_code != 200:
        print(f"Failed to fetch articles for {topic}. Status code: {response.status_code}")
        return []
    
    data = response.json()
    articles = [{"Title": article["webTitle"], "URL": article["webUrl"]} for article in data["response"]["results"]]
    return articles

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

    # Create a console object
    console = Console()

    # Create a tree
    tree = Tree(":newspaper: Articles", style="bold yellow", guide_style="bold blue")

    # Add branches to the tree
    for topic, articles in all_articles.items():
        topic_branch = tree.add(f":bookmark_tabs: [bold magenta]{topic}[/bold magenta]")
        for article in articles:
            topic_branch.add(f':link: [link={article["URL"]}]{article["Title"]}[/link]')

    # Print the tree to the console
    console.print(tree)

if __name__ == "__main__":
    topics = ["India", "Poltics", "Arsenal", "Cricket", "Science", "Technology", "World"]
    main(topics)
