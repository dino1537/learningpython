import os
import subprocess
import requests
import json
from rich.console import Console
import shutil

class YouTubePlayer:

    def __init__(self, api_key, player):
        self.api_key = api_key
        self.player = player
        self.results = []
        self.console = Console()

    def search_videos(self, search_query):
        search_url = "https://www.googleapis.com/youtube/v3/search"
        search_params = {
            "part": "snippet",
            "q": search_query,
            "key": self.api_key,
            "maxResults": 10,
            "type": "video"
        }
        response = requests.get(search_url, params=search_params)
        return response.json()

    def print_search_results(self):
        self.console.print("[bold underline]Search Results[/bold underline]")
        for i, item in enumerate(self.results['items'], start=1):
            self.console.print(f"[bold cyan]{i}. {item['snippet']['title']}[/bold cyan]")

    def get_video_id(self, video_num):
        return self.results['items'][video_num]['id']['videoId']

    def play_video(self, video_id):
        url = f"https://www.youtube.com/watch?v={video_id}"
        try:
            if self.player == "mpv" and shutil.which("mpv"):
                subprocess.call(["mpv", url])
            elif self.player == "vlc" and shutil.which("vlc"):
                subprocess.call(["vlc", url])
            else:
                print("Please install either 'mpv' or 'vlc' media player.")
        except Exception as e:
            print(str(e))

    def run(self):
        while True:
            search_query = input("Enter a YouTube search query (or 'q' to quit): ")
            if search_query.lower() == 'q':
                break
            self.results = self.search_videos(search_query)
            self.print_search_results()
            video_num = int(input("Enter the number of the video you want to play: ")) - 1
            video_id = self.get_video_id(video_num)
            self.play_video(video_id)

if __name__ == "__main__":
    api_key = os.getenv("YOUTUBE_API_KEY")  # Get API key from environment variable
    if not api_key:
        print("Please set the YOUTUBE_API_KEY environment variable.")
        exit(1)
    player = input("Enter your preferred player (mpv/vlc): ")
    player_app = YouTubePlayer(api_key, player)
    player_app.run()
