import sys
import subprocess
import click
from ytmusicapi import YTMusic
from rich import print
from rich.panel import Panel
from rich.table import Table
from rich.style import Style

# Initialize the YTMusic API client
ytmusic = YTMusic()

@click.command()
@click.argument("query", type=str, nargs=-1, required=True)
def search_and_play_song(query):
    """
    Search for songs based on the query and play the selected song.

    Args:
        query (str): Search query for songs.
    """
    query = " ".join(query)

    try:
        # Search for songs based on the query
        search_results = ytmusic.search(query, filter="songs", limit=5)

        if not search_results:
            print(Panel("[bold red]No matching songs found.[/bold red]", style=Style(color="white", bg="red")))
            sys.exit(1)

        table = Table(title="Search Results", show_lines=True, header_style="bold cyan")
        table.add_column("Number", style="cyan")
        table.add_column("Title", style="cyan")
        table.add_column("Artist", style="magenta")

        for i, song in enumerate(search_results, start=1):
            table.add_row(
                str(i),
                song['title'],
                song['artists'][0]['name']
            )

        print(table)

        choice = click.prompt(click.style("Enter the number of the song you want to play", fg="cyan"), type=int)
        if 1 <= choice <= len(search_results):
            song = search_results[choice - 1]
            video_id = song['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Use mpv or mpc to play the song
            player = "mpv"  # Change this to "mpc" if you prefer MPC
            subprocess.run([player, video_url])
        else:
            print(Panel("[bold red]Invalid choice.[/bold red]", style=Style(color="white", bg="red")))
            sys.exit(1)

    except Exception as e:
        print(Panel(f"[bold red]An error occurred:[/bold red] {str(e)}", style=Style(color="white", bg="red")))
        sys.exit(1)

if __name__ == "__main__":
    search_and_play_song()

