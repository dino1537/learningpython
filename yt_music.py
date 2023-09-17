import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
import subprocess

def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]

        if not results:
            print("No search results found.")
        else:
            print("Search Results:")
            for i, video in enumerate(results):
                print(f"{i + 1}. {video['title']}")
                print(f"   URL: https://www.youtube.com/watch?v={video['id']}")
        
        return results  # Return the results list

    except Exception as e:
        print("An error occurred:", str(e))

def play_audio(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()
        
        # Get the streaming URL without downloading
        stream_url = stream.url

        # Play the audio using mpv
        subprocess.call(["mpv", stream_url])

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
            selection = input("Enter the number of the video you want to play (or 'back' to go back): ")
            if selection.lower() == "back":
                continue
            try:
                selection = int(selection)
                if 1 <= selection <= len(results):
                    selected_url = f"https://www.youtube.com/watch?v={results[selection - 1]['id']}"
                    play_audio(selected_url)
                else:
                    print("Invalid selection. Please enter a valid number.")
            except ValueError:
                print("Invalid input. Please enter a number or 'back'.")

