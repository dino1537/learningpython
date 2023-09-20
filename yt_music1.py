import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
from rich import print
from rich.table import Table
from rich.console import Console
import subprocess

console = Console()


def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]

        if not results:
            print("No search results found.")
        else:
            table = Table(show_header=True, header_style="bold magenta")
            table.add_column("No.", style="dim")
            table.add_column("Title", style="cyan")
            table.add_column("URL", style="green")

            for i, video in enumerate(results, start=1):
                table.add_row(
                    f"{i}",
                    video["title"],
                    f"https://www.youtube.com/watch?v={video['id']}",
                )

            console.print(table)

        return results  # Return the results list

    except Exception as e:
        print("An error occurred:", str(e))


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
            print("Invalid player selection. Supported players: mpv, mplayer, vlc")

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    os.system("clear")

    while True:
        action = input("Enter a YouTube search query or 'quit' to exit: ")
        if action.lower() == "quit":
            break
        else:
            results = display_search_results(action)  # Store the results
            selection = input(
                "Enter the number of the video you want to play (or 'back' to go back): "
            )
            if selection.lower() == "back":
                continue
            try:
                selection = int(selection)
                if 1 <= selection <= len(results):
                    selected_url = f"https://www.youtube.com/watch?v={results[selection - 1]['id']}"
                    player = input(
                        "Select a media player (mpv, mplayer, vlc): "
                    ).strip()
                    play_audio(selected_url, player)
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number or 'back'.")
