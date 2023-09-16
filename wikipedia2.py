import wikipediaapi
from rich import print
import click

def get_full_page_content(query):
    # Create a Wikipedia API object with a custom user agent
    wiki_wiki = wikipediaapi.Wikipedia(
        language='en',
        user_agent='mywiki/1.0 (dineshnarayan19@gmail.com)'
    )

    # Search for the query and get the first result
    page = wiki_wiki.page(query)

    if page.exists():
        # Get the full page content
        full_content = page.text
        return full_content
    else:
        return None

def view_page(query):
    full_content = get_full_page_content(query)
    if full_content:
        print(full_content)
    else:
        print("No results found on Wikipedia for the given query.")

def download_page_as_markdown(query, output_file):
    full_content = get_full_page_content(query)
    if full_content:
        # Append the ".md" extension to the output file name
        if not output_file.endswith(".md"):
            output_file += ".md"
        
        # Save the page content to a Markdown file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(full_content)
        print(f"Page downloaded as Markdown to '{output_file}'")
    else:
        print("No results found on Wikipedia for the given query.")

@click.command()
@click.option('--query', prompt='Enter a search query:', help='Search query on Wikipedia')
@click.option('--view', is_flag=True, help='View the whole page content')
@click.option('--download', type=str, help='Download the page in Markdown format to the specified file')
def main(query, view, download):
    if view:
        view_page(query)
    elif download:
        download_page_as_markdown(query, download)
    else:
        print("Please specify either '--view' or '--download' option.")

if __name__ == "__main__":
    main()

