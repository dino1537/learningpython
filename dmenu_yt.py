import subprocess
import shlex
from youtubesearchpython import VideosSearch

def search_and_play_song():
    query = get_search_query()

    if not query:
        return

    videos_search = VideosSearch(query)
    results = videos_search.result()

    if not results:
        print("No search results found.")
        return

    video_choices = results["result"]
    song_choices = [f"{video['title']} - {video['link']}" for video in video_choices]

    input_text = "\n".join(song_choices)
    input_text = shlex.quote(input_text)
    cmd = f"echo -e {input_text} | dmenu -p 'Select a song to play:' -l {len(song_choices) - 1}"
    selected_song = subprocess.check_output(cmd, shell=True, text=True).strip()

    for video in video_choices:
        if selected_song.endswith(video["link"]):
            video_url = video["link"]
            subprocess.call(["mpv", video_url])
            return

    print("Invalid selection. Please choose a song from the list.")

def get_search_query():
    cmd = "echo -n | dmenu -p 'Enter a YouTube search query:'"
    search_query = subprocess.check_output(cmd, shell=True, text=True).strip()
    return search_query

if __name__ == "__main__":
    search_and_play_song()
