import requests
from rich.console import Console
from rich.tree import Tree
from rich import box
from rich.panel import Panel
import argparse
import os

# Get New York Times API credentials from environment variables
NY_API_KEY = os.getenv('NY_API_KEY')
NY_APP_ID = os.getenv('NY_APP_ID')
NY_SECRET = os.getenv('NY_SECRET')

# Base URL for the New York Times API
BASE_URL = 'https://api.nytimes.com/svc/'

# Initialize Rich console
console = Console()

def get_news(section='home'):
    """Fetches news articles from a specific section of NYTimes."""
    url = f'{BASE_URL}topstories/v2/{section}.json?api-key={NY_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_popular_articles():
    """Fetches popular articles from NYTimes."""
    url = f'{BASE_URL}mostpopular/v2/viewed/1.json?api-key={NY_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_top_sellers_list(list_name='hardcover-fiction'):
    """Fetches the top sellers list for books from NYTimes."""
    url = f'{BASE_URL}books/v3/lists/current/{list_name}.json?api-key={NY_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        console.print(f"Failed to fetch top sellers list for {list_name}. Status code: {response.status_code}", style="bold red")
        return None

def display_news(news):
    """Displays news articles in a tree format."""
    tree = Tree("📰 News Articles", guide_style="bold bright_blue")
    for article in news['results']:
        tree.add(f"[bold]{article['title']}[/bold]\n{article['abstract']}\n[link={article['url']}]Read more...[/link]")
    console.print(Panel(tree, box=box.ROUNDED, border_style="bright_blue"))

def display_popular_articles(articles):
    """Displays popular articles in a tree format."""
    tree = Tree("🌟 Popular Articles", guide_style="bold bright_green")
    for article in articles['results']:
        tree.add(f"[bold]{article['title']}[/bold]\n{article['abstract']}\n[link={article['url']}]Read more...[/link]")
    console.print(Panel(tree, box=box.ROUNDED, border_style="bright_green"))

def display_top_sellers(books, list_name):
    """Displays top sellers list for books in a tree format."""
    tree = Tree(f"📚 Top Sellers Books - {list_name.replace('-', ' ').title()}", guide_style="bold bright_yellow")
    for book in books['results']['books']:
        tree.add(f"[bold]{book['rank']}. {book['title']}[/bold] by {book['author']}\n[link={book['amazon_product_url']}]Buy on Amazon[/link]")
    console.print(Panel(tree, box=box.ROUNDED, border_style="bright_yellow"))


def main():
    parser = argparse.ArgumentParser(description="NYTimes News CLI Utility")
    parser.add_argument("--section", type=str, help="Section of news to fetch")
    parser.add_argument("--popular", action="store_true", help="Get popular articles")
    parser.add_argument("--list", type=str, help="Name of the best sellers list")
    args = parser.parse_args()

    if args.popular:
        popular_articles = get_popular_articles()
        if popular_articles:
            display_popular_articles(popular_articles)
        else:
            console.print("[bold red]Failed to fetch popular articles.[/bold red]")
    elif args.list:
        top_sellers = get_top_sellers_list(args.list)
        if top_sellers:
            display_top_sellers(top_sellers, args.list)
        else:
            console.print(f"[bold red]Failed to fetch top sellers list for {args.list}.[/bold red]")
    elif args.section:
        news = get_news(args.section)
        if news:
            display_news(news)
        else:
            console.print(f"[bold red]Failed to fetch news for section {args.section}.[/bold red]")
    else:
        # Default action if no arguments are provided
        news = get_news()
        if news:
            display_news(news)
        else:
            console.print("[bold red]Failed to fetch news articles.[/bold red]")

if __name__ == '__main__':
    main()
