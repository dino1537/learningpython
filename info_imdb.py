import imdb
from rich.console import Console

def get_movie_info(query):
    # Create an instance of the IMDb class
    ia = imdb.IMDb()

    # Search for the movie or TV show by title
    search_results = ia.search_movie(query)

    if not search_results:
        console = Console()
        console.print("[red]No results found for '{query}'[/red].")
        return

    # Get the first result (most relevant) from the search
    movie = search_results[0]

    # Fetch additional information about the movie or TV show
    ia.update(movie)

    # Create a styled output using rich
    title_style = "bold cyan"
    subtitle_style = "bold yellow"
    info_style = "italic"

    # Create a Console for the output
    console = Console(width=80)  # Adjust the width as needed

    # Print the information with rich formatting
    console.print("\n[bold]Movie Info[/bold]")
    console.print(f"[{title_style}]Title:[/]", movie['title'])
    console.print(f"[{subtitle_style}]Year:[/]", movie['year'])
    console.print(f"[{subtitle_style}]Rating:[/]", movie['rating'])
    console.print(f"[{subtitle_style}]Genres:[/]", ', '.join(movie['genres']))
    console.print(f"[{subtitle_style}]Plot:[/]")
    console.print(f"[{info_style}]{movie['plot'][0]}[/]")

if __name__ == "__main__":
    query = input("Enter the movie or TV show title: ")
    get_movie_info(query)

