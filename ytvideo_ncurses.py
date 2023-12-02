import os
import urwid
from pytube import YouTube
from youtubesearchpython import VideosSearch
import subprocess
import shlex
import shutil

def display_search_results(search_query):
    try:
        videos_search = VideosSearch(search_query)
        results = videos_search.result()["result"]
        return results
    except Exception as e:
        return None

def select_video(results):
    if not results:
        return None

    try:
        menu_items = [f"{i + 1}. {video['title']}" for i, video in enumerate(results)]
        menu_items.append("Quit")

        def on_select(button, choice):
            if choice == len(menu_items) - 1:  # The last item is "Quit"
                raise urwid.ExitMainLoop()
            else:
                selected_video = results[choice]
                play_video(f"https://www.youtube.com/watch?v={selected_video['id']}")

        choices = [urwid.Button(item, on_press=on_select, user_data=i) for i, item in enumerate(menu_items)]
        return urwid.ListBox(urwid.SimpleFocusListWalker(choices))
    except ValueError:
        return None

def play_video(url, player="mpv"):
    try:
        if player == "mpv" and shutil.which("mpv"):
            subprocess.call(["mpv", url])
        else:
            os.system(f"vlc {url}")
    except Exception as e:
        print("An error occurred while playing the video:", str(e))

def main():
    query = input("Enter a YouTube search query (Press 'q' to quit): ")
    if query.lower() == 'q':
        return

    results = display_search_results(query)
    if results is not None:
        main_loop = urwid.MainLoop(select_video(results))
        main_loop.run()

if __name__ == "__main__":
    main()
