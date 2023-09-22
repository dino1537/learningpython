import os
from pytube import YouTube
from youtubesearchpython import VideosSearch
import subprocess
import shlex
import shutil

def get_query_from_dmenu():
    try:
        cmd = "echo -n '' | dmenu -p 'Enter a YouTube search query:'"
        query = subprocess.check_output(cmd, shell=True, text=True).strip()
        return query
    except subprocess.CalledProcessError as e:
        print("Error: dmenu exited with a non-zero status code.")
        return None

def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]

        if not results:
            print("No search results found.")
            return None
        else:
            return results

    except Exception as e:
        print("An error occurred during the search:", str(e))
        return None

def select_audio(results):
    if not results:
        return None

    try:
        input_text = "\n".join([f"{video['title']}" for video in results])
        input_text = shlex.quote(input_text)
        cmd = f"echo -e {input_text} | dmenu -p 'Select a video to play:' -l {len(results)}"
        selected_title = subprocess.check_output(cmd, shell=True, text=True).strip()

        if not selected_title:
            return None

        for video in results:
            if video['title'] == selected_title:
                return f"https://www.youtube.com/watch?v={video['id']}"

        print("Invalid selection. Please select a video from the list.")
        return None
    except subprocess.CalledProcessError as e:
        print("Error: dmenu exited with a non-zero status code.")
        return None

def play_audio(url):
    try:
        yt = YouTube(url)
        stream = yt.streams.filter(only_audio=True).first()

        stream_url = stream.url
        title = yt.title  # Get the title of the YouTube video
        # Use MPC to add the audio stream to the MPD playlist
        subprocess.call(["mpc", "add", stream_url])
        # Start playback using MPC
        subprocess.call(["mpc", "play"])

    except Exception as e:
        print("An error occurred while playing the audio:", str(e))

if __name__ == "__main__":
    while True:
        query = get_query_from_dmenu()
        if query is None:
            break

        results = display_search_results(query)
        if results is not None:
            selected_url = select_audio(results)
            if selected_url is not None:
                play_audio(selected_url)

