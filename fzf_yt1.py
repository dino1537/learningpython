import os
import socket
from pytube import YouTube
from pytube.cli import on_progress
from youtubesearchpython import VideosSearch
import subprocess
import shlex
import shutil  # Import shutil module
import configparser
from tqdm import tqdm
import requests

class ProgressYouTube(YouTube):
    def stream_download(self, itag, output_path=None, filename=None, filename_prefix=None):
        stream = self.streams.get_by_itag(itag)

        output_path = output_path or os.getcwd()

        # if the user specifies a filename then use it
        if filename:
            filename = filename
        # if no filename is specified but a prefix is then prepend it to the
        # default filename
        elif filename_prefix:
            filename = filename_prefix + stream.default_filename
        # if neither a filename or prefix is specified then use the default
        # filename
        else:
            filename = stream.default_filename

        file_path = os.path.join(output_path, filename)
        with open(file_path, 'wb') as fh:
            for chunk in tqdm(stream.iter_segments(), unit='B', unit_scale=True):
                fh.write(chunk)

        return file_path


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]

        if not results:
            print("No search results found.")
        else:
            for i, video in enumerate(results, start=1):
                print(f"{i}. {video['title']}")

        return results  # Return the results list

    except Exception as e:
        print("An error occurred:", str(e))
        return None


def select_audio(results):
    try:
        input_text = "\n".join([f"{video['title']}" for video in results])
        input_text = shlex.quote(input_text)
        cmd = f"echo -e {input_text} | fzf --prompt 'Select a video to play:'"
        selected_title = subprocess.check_output(cmd, shell=True, text=True).strip()

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


def download_audio(url, download_directory):
    try:
        yt = YouTube(url, on_progress_callback=on_progress)
        stream = yt.streams.filter(only_audio=True).first()
        # Get the correct file extension
        ext = stream.mime_type.split("/")[1]
        # Create the filename using the title of the video
        filename = f"{yt.title}.{ext}"
        # Download the audio stream
        stream.download(output_path=download_directory, filename=filename)
    except Exception as e:
        print("An error occurred:", str(e))

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('settings.ini')
    player = config['DEFAULT']['Player']
    download_directory = config['DEFAULT']['DownloadDirectory']

    while True:
        action = input("Please enter a YouTube search query to find and play audio, or type 'quit' to exit the program. Thank you!: ")
        if action.lower() == "quit":
            break
        else:
            if is_connected():
                results = display_search_results(action)  # Store the results
                selected_url = select_audio(results)
                if selected_url:
                    download = input("Do you want to download the audio? (yes/no): ")
                    if download.lower() == "yes":
                        download_audio(selected_url, download_directory)
                    play_audio(selected_url, player)
            else:
                print("You are not connected to the internet. Please check your connection and try again.")
