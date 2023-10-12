import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
import subprocess
import shlex
import shutil  # Import shutil module


def get_query_from_rofi():
    try:
        cmd = "rofi -dmenu -p 'Enter a YouTube search query:'"
        query = subprocess.check_output(cmd, shell=True, text=True).strip()
        return query
    except subprocess.CalledProcessError as e:
        print("Rofi exited with a non-zero status code. Exiting.")
        return None


def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]

        if not results:
            print("No search results found.")
        else:
            return results  # Return the results list

    except Exception as e:
        print("An error occurred:", str(e))


def select_audio(results):
    try:
        input_text = "\n".join([f"{video['title']}" for video in results])
        input_text = shlex.quote(input_text)
        cmd = f"echo -e {input_text} | rofi -dmenu -p 'Select a video to play:' -i -kb-cancel '!Alt+Escape'"
        selected_title = subprocess.check_output(cmd, shell=True, text=True).strip()

        # Check if the Escape key was pressed
        if selected_title == "!Alt+Escape":
            return None

        # Find the corresponding video URL
        for video in results:
            if video["title"] == selected_title:
                return f"https://www.youtube.com/watch?v={video['id']}"

        print("Invalid selection. Please select a video from the list.")
        return None
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None


def play_audio(url, player="mpv"):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()

        # Get the streaming URL without downloading
        stream_url = stream.url

        # Check if mpv is available, if not, use a default player
        if player == "mpv" and shutil.which("mpv"):
            subprocess.call(["mpv", stream_url])
        else:
            print("mpv is not available. Using default player.")
            subprocess.call(["vlc", stream_url])

    except Exception as e:
        print("An error occurred:", str(e))


if __name__ == "__main__":
    while True:
        query = get_query_from_rofi()  # Get the query from Rofi
        if not query:
            break  # Exit if the user cancels Rofi or if there's an error
        results = display_search_results(query)  # Store the results
        selected_url = select_audio(results)
        if selected_url:
            play_audio(selected_url)
