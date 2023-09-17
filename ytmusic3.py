import subprocess
import yt_dlp

# Function to search YouTube and return a list of video URLs
def search_youtube(query, max_results=20):
    ydl_opts = {
        'quiet': True,
        'extract_audio': True,
        'audio_format': 'mp3',
        'default_search': 'auto',
        'verbose': True,  # Add this line to enable verbose mode
        'max_results': max_results,  # Set the maximum number of results
        'youtube_view_count': None,  # Sort results by view count
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(f"ytsearch:{query}", download=False)
        video_urls = []

        if 'entries' in info_dict:
            for entry in info_dict['entries']:
                video_url = entry['webpage_url']  # Use 'webpage_url' instead of 'url'
                video_urls.append(video_url)
        
        return video_urls

# Function to display and choose from the list of video URLs
def choose_and_play_video(video_urls):
    if not video_urls:
        print("No results found.")
        return
    
    print("Choose a video to play:")
    for i, url in enumerate(video_urls, start=1):
        print(f"{i}. {url}")

    choice = input("Enter the number of the video you want to play: ")

    try:
        choice = int(choice)
        if 1 <= choice <= len(video_urls):
            selected_video_url = video_urls[choice - 1]
            selected_player = input("Choose a player (mplayer, mpv, vlc): ").strip().lower()

            if selected_player == "mplayer":
                play_audio_mplayer(selected_video_url)
            elif selected_player == "mpv":
                play_audio_mpv(selected_video_url)
            elif selected_player == "vlc":
                play_audio_vlc(selected_video_url)
            else:
                print("Invalid player choice.")
        else:
            print("Invalid choice.")
    except ValueError:
        print("Invalid input. Please enter a number.")

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
    video_urls = search_youtube(query)

    if video_urls:
        choose_and_play_video(video_urls)
    else:
        print(f"No results found for '{query}'")

