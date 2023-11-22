import sys
from newspaper import Article
from rich.console import Console
from rich.table import Table
import webbrowser
import nltk

# Download the punkt tokenizer
nltk.download('punkt')

console = Console()

def read_article():
    # Ask the user to input the URL of the article
    url = input("Please enter the URL of the article you want to read: ")

    # Use the Article function from the newspaper library to parse the article
    article = Article(url)

    try:
        # Download the article
        article.download()
    except Exception as e:
        console.print(f"An error occurred while trying to download the article: [red]{e}[/red]")
        return

    try:
        # Parse the article
        article.parse()
    except Exception as e:
        console.print(f"An error occurred while trying to parse the article: [red]{e}[/red]")
        return

    # Perform natural language processing on the article
    article.nlp()

    # Create a table
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Title")
    table.add_column("Author")
    table.add_column("Publication Date")
    table.add_row(article.title, ', '.join(article.authors), str(article.publish_date))

    # Print the table
    console.print(table)

    # Print the article's text
    console.print(f"Text: [bold cyan]{article.text}[/bold cyan]")

    # Print the article's summary
    console.print(f"Summary: [bold yellow]{article.summary}[/bold yellow]")

    # Print the article's keywords
    console.print(f"Keywords: [bold green]{', '.join(article.keywords)}[/bold green]")

    # Ask the user if they want to open the article in a web browser
    open_in_browser = input("Do you want to open the article in your web browser? (yes/no): ")
    if open_in_browser.lower() == "yes":
        webbrowser.open(url)

if __name__ == "__main__":
    read_article()
