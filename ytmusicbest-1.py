import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
from rich import print
from rich.table import Table
from rich.console import Console
from rich.style import Style
import subprocess
from rich.prompt import Prompt
import requests

console = Console()

# ... (existing imports)
def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]

        if not results:
            print("[bold red]No search results found.[/bold red]")
        else:
            table = Table(title="Search Results", show_lines=True, title_style="bold white on blue", style="green")
            table.add_column("No.", justify="center", style="dim")
            table.add_column("Title", justify="left", style="magenta") 
            table.add_column("URL", justify="center", style="blue")

            for i, video in enumerate(results, start=1):
                table.add_row(
                    f"[white]{i}[/white]",
                    f"[yellow]{video['title']}[/yellow]",
                    f"[blue]https://www.youtube.com/watch?v={video['id']}[/blue]"
                )

            console.print(table)
        
        return results  # Return the results list

    except Exception as e:
        print(f"[bold red]An error occurred:[/bold red] {str(e)}")
# ... (rest of the script)

def play_audio(url, player="mpv"):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        
        # Get the streaming URL without downloading
        stream_url = stream.url

        # Play the audio using the selected media player
        if player == "mpv":
            subprocess.call(["mpv", stream_url])
        elif player == "mplayer":
            subprocess.call(["mplayer", stream_url])
        elif player == "vlc":
            subprocess.call(["vlc", stream_url])
        else:
            print("[bold red]Invalid player selection. Supported players: mpv, mplayer, vlc[/bold red]")

    except Exception as e:
        print(f"[bold red]An error occurred:[/bold red] {str(e)}")

if __name__ == "__main__":
    os.system("clear")

    while True:
        action = input("Enter a YouTube search query or 'quit' to exit: ")
        if action.lower() == "quit":
            break
        else:
            results = display_search_results(action)
            selection = Prompt.ask("Enter the number of the video you want to play (or 'back' to go back): ")

            if selection.lower() == "back":
                continue
            try:
                selection = int(selection)
                if 1 <= selection <= len(results):
                    selected_url = f"https://www.youtube.com/watch?v={results[selection - 1]['id']}"
                    player = Prompt.ask("Select a media player ([blue]mpv[/blue], [blue]mplayer[/blue], [blue]vlc[/blue]): ").strip().lower()
                    play_audio(selected_url, player)
                else:
                    print("[bold red]Invalid selection. Please enter a valid number.[/bold red]")
            except ValueError:
                print("[bold red]Invalid input. Please enter a number or 'back'.[/bold red]")
