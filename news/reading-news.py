import sys
import json
import os
from newspaper import Article
from rich.console import Console
from rich.table import Table
import webbrowser
import nltk

# Download the punkt tokenizer
nltk.download('punkt')

console = Console()

# Load the configuration file
with open('config.json') as f:
    config = json.load(f)

# Load the reading list
if os.path.exists(config['reading_list_file']):
    with open(config['reading_list_file']) as f:
        reading_list = json.load(f)
else:
    reading_list = []

def download_article(url):
    # Use the Article function from the newspaper library to parse the article
    article = Article(url)

    try:
        # Download the article
        article.download()
    except Exception as e:
        console.print(f"An error occurred while trying to download the article: [{config['error_color']}]{e}[/{config['error_color']}]")
        return None

    return article

def parse_article(article):
    try:
        # Parse the article
        article.parse()
    except Exception as e:
        console.print(f"An error occurred while trying to parse the article: [{config['error_color']}]{e}[/{config['error_color']}]")
        return False

    # Perform natural language processing on the article
    article.nlp()

    return True

def print_article(article):
    # Create a table
    table = Table(show_header=True, header_style=config['header_style'])
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Publication Date")
    table.add_row(article.title, ', '.join(article.authors), str(article.publish_date))

    # Print the table
    console.print(table)

    # Print the article's text
    console.print(f"Text: [{config['text_color']}]{article.text}[/{config['text_color']}]")

    # Print the article's summary
    console.print(f"Summary: [{config['summary_color']}]{article.summary}[/{config['summary_color']}]")

    # Print the article's keywords
    console.print(f"Keywords: [{config['keywords_color']}]{', '.join(article.keywords)}[/{config['keywords_color']}]")

def save_to_reading_list(url):
    reading_list.append(url)
    with open(config['reading_list_file'], 'w') as f:
        json.dump(reading_list, f)

def read_article():
    # Ask the user to input the URL of the article
    url = input("Please enter the URL of the article you want to read: ")

    article = download_article(url)
    if article is None:
        return

    if not parse_article(article):
        return

    print_article(article)

    # Ask the user if they want to save the article to their reading list
    save_to_list = input("Do you want to save this article to your reading list? (yes/no): ")
    if save_to_list.lower() == "yes":
        save_to_reading_list(url)

    # Ask the user if they want to open the article in a web browser
    open_in_browser = input("Do you want to open the article in your web browser? (yes/no): ")
    if open_in_browser.lower() == "yes":
        webbrowser.open(url)

if __name__ == "__main__":
    read_article()
