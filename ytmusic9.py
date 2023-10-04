import sys
import subprocess
import click
from ytmusicapi import YTMusic
from rich import print
from rich.panel import Panel
from rich.table import Table

# Initialize the YTMusic API client
ytmusic = YTMusic()

def search_and_play(query, type, limit, page):
    """
    Search for songs, albums, artists, or playlists based on the query and display the selected result.

    Args:
        query (str): Search query.
        type (str): Type of search (songs, albums, artists, playlists).
        limit (int): Number of search results to display.
        page (int): Page number for paginated results.
    """
    try:
        # Initialize the table to display results
        table = Table(title=f"Search Results ({type.capitalize()})", show_lines=True, header_style="bold cyan")
        table.add_column("Number", style="cyan")
        table.add_column("Title" if type == "songs" else "Name", style="cyan")
        table.add_column("Artist" if type == "songs" else "Album" if type == "albums" else "Owner", style="magenta")

        # Fetch a larger number of results
        search_results = ytmusic.search(query, filter=type, limit=limit*10)

        if not search_results:
            print(Panel(f"No matching {type} found.", style="red"))
            sys.exit(1)

        # Display results in chunks based on limit and page
        start_index = (page - 1) * limit
        end_index = start_index + limit

        for i, result in enumerate(search_results[start_index:end_index], start=start_index+1):
            if type == "songs":
                title = result['title']
                artist = result['artists'][0]['name']
            elif type == "albums":
                title = result['title']
                artist = result['artists'][0]['name']
            elif type == "artists":
                title = result.get('name', 'N/A')  # Handle missing artist name
                artist = title if title != 'N/A' else result.get('displayName', 'N/A')  # Display "displayName" if available
            elif type == "playlists":
                title = result['title']
                artist = result['ownerName']

            table.add_row(
                str(i),
                title,
                artist
            )

        print(table)

        while True:
            choice = click.prompt(click.style("Enter the number of the item you want to explore (q to exit)", fg="cyan"))
            
            # Check if the user wants to exit
            if choice.lower() == "q" or choice.lower() == "exit":
                # sys.exit(0)  # Remove this line to continue running the script
                break  # Exit the loop to continue running the script

            # Check if the input is a valid integer
            if choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(search_results):
                    item = search_results[choice - 1]
                    if type == "songs":
                        video_id = item['videoId']
                        video_url = f"https://www.youtube.com/watch?v={video_id}"
                        player = "mpv"  # Change this to "mpc" if you prefer MPC
                        subprocess.run([player, video_url])
                    elif type == "albums":
                        album_id = item['browseId']
                        album_url = f"https://music.youtube.com/playlist?list={album_id}"
                        click.launch(album_url)  # Open the album in a web browser
                    else:
                        print(f"Selected {type}: [bold cyan]{item['title']}[/bold cyan]")
                    # Remove the 'break' statement to continue running the script
                else:
                    print(Panel("[bold red]Invalid choice.[/bold red]", style="red"))
            else:
                print(Panel("[bold red]Invalid input.[/bold red]", style="red"))

    except Exception as e:
        print(Panel(f"[bold red]An error occurred:[/bold red] {str(e)}", style="red"))
        sys.exit(1)

@click.command()
@click.argument("query", type=str, required=True)
@click.option("--type", type=click.Choice(["songs", "albums", "artists", "playlists"]), default="songs",
              help="Specify the type of search (songs, albums, artists, playlists)")
@click.option("--limit", type=int, default=15, help="Number of search results to display")
@click.option("--page", type=int, default=1, help="Page number for paginated results")
def search_and_play_cli(query, type, limit, page):
    search_and_play(query, type, limit, page)

if __name__ == "__main__":
    search_and_play_cli()

