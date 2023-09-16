import wikipediaapi
from rich import print

def scrape_wikipedia(query):
    # Create a Wikipedia API object with a custom user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='mywiki-1 (dineshnarayan19@gmail.com)'
    )

    # Search for the query and get the first result
    page = wiki_wiki.page(query)

    if page.exists():
        # Display the title and summary
        title = page.title
        summary = page.summary

        # Display the output in a nice format using rich
        print(f"[bold]Title:[/bold] {title}")
        print(f"[cyan]Summary:[/cyan] {summary}")
    else:
        print("No results found on Wikipedia for the given query.")

if __name__ == "__main__":
    search_query = input("Enter a search query: ")
    scrape_wikipedia(search_query)

