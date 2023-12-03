import requests
from rich.console import Console
from rich.tree import Tree
from rich import box
from rich.panel import Panel
import argparse
import os

# Get New York Times API credentials from environment variables
NY_API_KEY = os.getenv('NY_API_KEY')

# Base URL for the New York Times API
BASE_URL = 'https://api.nytimes.com/svc/books/v3/'

# Initialize Rich console
console = Console()

def get_top_sellers_list(list_name='hardcover-fiction'):
    """Fetches the top sellers list for books from NYTimes."""
    url = f'{BASE_URL}lists/current/{list_name}.json?api-key={NY_API_KEY}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        console.print(f"Failed to fetch top sellers list for {list_name}. Status code: {response.status_code}", style="bold red")
        return None

def display_top_sellers(books, list_name):
    """Displays top sellers list for books in a tree format."""
    tree = Tree(f"📚 Top Sellers Books - {list_name.replace('-', ' ').title()}", guide_style="bold bright_yellow")
    for book in books['results']['books']:
        tree.add(f"[bold]{book['rank']}. {book['title']}[/bold] by {book['author']}\n[link={book['amazon_product_url']}]Buy on Amazon[/link]")
    console.print(Panel(tree, box=box.ROUNDED, border_style="bright_yellow"))

def main():
    parser = argparse.ArgumentParser(description="NYTimes Best Sellers CLI Utility")
    parser.add_argument("--list", type=str, default="hardcover-fiction", help="Name of the best sellers list (default is 'hardcover-fiction')")
    args = parser.parse_args()

    top_sellers = get_top_sellers_list(args.list)
    if top_sellers:
        display_top_sellers(top_sellers, args.list)

if __name__ == '__main__':
    main()
