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
from rich.box import Box
from rich.panel import Panel

console = Console()
MEDIA_PLAYERS = ["mpv", "mplayer", "vlc"]
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

def clear_screen():
    os.system("clear")

def display_help():
    console.print("[bold cyan] [green]YouTube[/green] Player Command-line Application[/bold cyan]")
    console.print("[italic]Instructions:[/italic]")

    # Draw a box around the help section
    panel_content = "\n".join([
        "[yellow]1.[/yellow] Enter a search query to find YouTube videos.",
        "[yellow]2.[/yellow] Select a video to play.",
        "[yellow]3.[/yellow] Choose a media player to play the audio.",
        "[yellow]4.[/yellow] Type 'quit' to exit the application.",
    ])
    panel = Panel(panel_content)
    console.print(panel)

    console.print("[italic]Enjoy your music! [/italic]")

def print_separator():
    console.print("\n[bold][cyan]----------------------------------------[/cyan][/bold]\n")

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
    clear_screen()
    display_help()

    while True:
        console.print("\n  [yellow][/yellow] ", end="")
        action = input("\033[36mEnter a YouTube search query or 'quit' to exit:\033[0m ")
        if action.lower() == "quit":
            clear_screen()
            break
        else:
            results = display_search_results(action)
            print_separator()
            console.print("  [yellow][/yellow] ", end="")
            selection = Prompt.ask("\033[36mEnter the number of the video you want to play (or 'back' to go back):\033[0m ")

            if selection.lower() == "back":
                clear_screen()
                display_help()
                continue
            try:
                selection = int(selection)
                if 1 <= selection <= len(results):
                    selected_url = f"https://www.youtube.com/watch?v={results[selection - 1]['id']}"
                    console.print("  [yellow][/yellow] ", end="")
                    player_prompt = Prompt.ask(f"\033[93mSelect a media player ({'/'.join(MEDIA_PLAYERS)}):\033[0m ")
                    clear_screen()
                    play_audio(selected_url, player_prompt)
                    display_help()
                else:
                    print("[bold red]Invalid selection. Please enter a valid number.[/bold red]")
            except ValueError:
                print("[bold red]Invalid input. Please enter a number or 'back'.[/bold red]")
