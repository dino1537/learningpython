from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table
from pytube import YouTube
from youtubesearchpython import VideosSearch
import os
import subprocess


console = Console()

def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]

        if not results:
            console.print("No search results found.", style="bold red")
        else:
            console.print("\nSearch Results:", style="bold green")
            
            # Create a Rich Table object
            table = Table(show_header=True, header_style="bold magenta")
            
            # Specify the Column Names while initializing the Table
            table.add_column('No.')
            table.add_column('Title')
            
            for i, video in enumerate(results):
                # Adding rows
                table.add_row(str(i + 1), video['title'])
            
            console.print(table)
        
        return results  # Return the results list

    except Exception as e:
        console.print("An error occurred: " + str(e), style="bold red")

def play_audio(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        
        # Get the streaming URL without downloading
        stream_url = stream.url

        # Play the audio using mpv
        subprocess.call(["mpv", stream_url])

    except Exception as e:
        console.print("An error occurred: " + str(e), style="bold red")

if __name__ == "__main__":
    os.system("clear")

    while True:
        action = prompt("\nEnter a YouTube search query or 'quit' to exit: ", completer=WordCompleter(['quit']), complete_while_typing=True)
        if action.lower() == "quit":
            break
        else:
            results = display_search_results(action)  # Store the results
            if results:
                selection = prompt("\nEnter the number of the video you want to play (or 'back' to go back): ", completer=WordCompleter(['back', 'quit'] + [str(i+1) for i in range(len(results))]), complete_while_typing=True)
                if selection.lower() == "back":
                    continue
                elif selection.lower() == "quit":
                    break
                try:
                    selection = int(selection)
                    if 1 <= selection <= len(results):
                        selected_url = f"https://www.youtube.com/watch?v={results[selection - 1]['id']}"
                        console.print("\nBuffering video...", style="bold cyan")
                        play_audio(selected_url)
                except ValueError:
                    console.print("Invalid input. Please enter a number or 'back'.", style="bold red")
