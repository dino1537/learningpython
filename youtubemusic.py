import subprocess
import yt_dlp

# Function to search YouTube and return the video URL
def search_youtube(query):
    ydl_opts = {
        'quiet': True,
        'extract_audio': True,
        'audio_format': 'mp3',
        'default_search': 'auto',
        'verbose': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{query}", download=False)
        if 'entries' in info_dict:
            video_url = info_dict['entries'][0]['webpage_url']
            return video_url

# Function to play the audio using mplayer
def play_audio_mplayer(video_url):
    subprocess.run(['mplayer', '-vo', 'null', '-ao', 'alsa', video_url])

# Function to play the audio using mpv
def play_audio_mpv(video_url):
    subprocess.run(['mpv', '--no-video', video_url])

# Function to play the audio using vlc
def play_audio_vlc(video_url):
    subprocess.run(['vlc', '--no-video', video_url])

if __name__ == "__main__":
    query = input("Enter your YouTube search query: ")
    video_url = search_youtube(query)

    if video_url:
        print(f"Playing audio from {video_url}")
        print("Choose a player: ")
        print("1. mplayer")
        print("2. mpv")
        print("3. vlc")
        player_choice = input("Enter the number of your choice (1/2/3): ")

        if player_choice == "1":
            play_audio_mplayer(video_url)
        elif player_choice == "2":
            play_audio_mpv(video_url)
        elif player_choice == "3":
            play_audio_vlc(video_url)
        else:
            print("Invalid choice. Exiting.")
    else:
        print(f"No results found for '{query}'")

