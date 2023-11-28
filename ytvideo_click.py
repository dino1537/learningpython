import os
import subprocess
import requests
import json
import click
import shutil

@click.group()
def cli():
    pass

@click.command()
@click.option('--player', prompt='Your preferred player', help='The media player to use (mpv/vlc).')
@click.option('--search_query', prompt='YouTube search query', help='The search query for YouTube videos.')
def search_and_play(player, search_query):
    api_key = os.getenv("YOUTUBE_API_KEY")  # Get API key from environment variable
    if not api_key:
        print("Please set the YOUTUBE_API_KEY environment variable.")
        return

    search_url = "https://www.googleapis.com/youtube/v3/search"
    search_params = {
        "part": "snippet",
        "q": search_query,
        "key": api_key,
        "maxResults": 10,
        "type": "video"
    }
    response = requests.get(search_url, params=search_params)
    results = response.json()

    for i, item in enumerate(results['items'], start=1):
        print(f"{i}. {item['snippet']['title']}")

    video_num = int(input("Enter the number of the video you want to play: ")) - 1
    video_id = results['items'][video_num]['id']['videoId']

    url = f"https://www.youtube.com/watch?v={video_id}"
    try:
        if player == "mpv" and shutil.which("mpv"):
            subprocess.call(["mpv", url])
        elif player == "vlc" and shutil.which("vlc"):
            subprocess.call(["vlc", url])
        else:
            print("Please install either 'mpv' or 'vlc' media player.")
    except Exception as e:
        print(str(e))

cli.add_command(search_and_play)

if __name__ == "__main__":
    cli()
