import sys
from ytmusicapi import YTMusic
import subprocess

# Initialize the YTMusic API client
ytmusic = YTMusic()

def search_and_play_song(query):
    try:
        # Search for songs based on the query
        search_results = ytmusic.search(query, filter="songs", limit=5)

        if not search_results:
            print("No matching songs found.")
            return

        print("Choose a song to play:")
        for i, song in enumerate(search_results, start=1):
            print(f"{i}. {song['title']} by {song['artists'][0]['name']}")

        choice = int(input("Enter the number of the song you want to play: "))
        if 1 <= choice <= len(search_results):
            song = search_results[choice - 1]
            video_id = song['videoId']
            video_url = f"https://www.youtube.com/watch?v={video_id}"

            # Use mpv or mpc to play the song
            player = "mpv"  # Change this to "mpc" if you prefer MPC
            subprocess.run([player, video_url])
        else:
            print("Invalid choice.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python listen_to_ytmusic.py <song_query>")
        sys.exit(1)

    # Get the song query from the command line arguments
    song_query = " ".join(sys.argv[1:])

    # Search for and play the song
    search_and_play_song(song_query)

