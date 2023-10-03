import tkinter as tk
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os
import pygame
import musicbrainzngs as mb
from mutagen.easyid3 import EasyID3  # Import EasyID3 for mp3 files
import requests 

# Initialize pygame for audio
pygame.mixer.init()

# Set the MusicBrainz API base URL
mb.set_useragent("AlbumArtDownloader", "1.0")

# Initialize music_directory and audio_files as global variables
music_directory = "/home/dino/Music"
audio_files = []


# Function to fetch album art using MusicBrainz API
def fetch_album_art(artist_name, album_name, output_directory):
    # Construct the query for fetching album art from Cover Art Archive
    query = f"{artist_name} {album_name}"
    url = f"https://musicbrainz.org/ws/2/release/?query={query}&fmt=json"

    try:
        # Send a GET request to the MusicBrainz API
        response = requests.get(url)

        # Check if the response was successful
        if response.status_code == 200:
            data = response.json()

            # Check if any releases were found
            if "releases" in data and len(data["releases"]) > 0:
                release_id = data["releases"][0]["id"]

                # Construct the URL for fetching album art from Cover Art Archive
                album_art_url = (
                    f"https://coverartarchive.org/release/{release_id}/front"
                )

                # Send a GET request to fetch the album art
                response = requests.get(album_art_url)

                # Check if the response was successful
                if response.status_code == 200:
                    # Save the album art image
                    with open(
                        os.path.join(output_directory, f"{album_name}.jpg"), "wb"
                    ) as f:
                        f.write(response.content)
                else:
                    print("Cover art not found.")
            else:
                print("No releases found.")
        else:
            print("Error fetching data from MusicBrainz.")
    except Exception as e:
        print(f"Error: {e}")


# Function to get metadata from audio file
def get_metadata(file_path):
    try:
        audio = EasyID3(file_path)
        metadata = {
            "artist": audio.get("artist", ["Unknown Artist"])[0],
            "album": audio.get("album", ["Unknown Album"])[0],
            "title": audio.get("title", ["Unknown Title"])[0],
            # Add more metadata fields as needed
        }
        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
    return {}


# Function to play the audio
def play_audio(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()
    metadata = get_metadata(audio_file)
    artist_name = metadata["artist"]
    album_name = metadata["album"]
    title = metadata["title"]
    # Fetch and display album art
    fetch_album_art(artist_name, album_name, album_art_output_directory)
    update_song_info(title, artist_name, album_name)


# Function to pause the audio
def pause_audio():
    pygame.mixer.music.pause()


# Function to stop the audio
def stop_audio():
    pygame.mixer.music.stop()


# Function to play the next audio file
def play_next_audio():
    global current_audio_index
    current_audio_index = (current_audio_index + 1) % len(audio_files)
    play_audio(os.path.join(music_directory, audio_files[current_audio_index]))


# Function to update song information (name, artist, album, and album art)
def update_song_info(title, artist_name, album_name):
    song_name_label.config(text=title)  # Update song name label
    artist_label.config(text=f"Artist: {artist_name}")  # Update artist label
    album_label.config(text=f"Album: {album_name}")  # Update album label
    # Load and display album art image
    album_art_path = os.path.join(album_art_output_directory, f"{album_name}.jpg")
    if os.path.exists(album_art_path):
        album_art = Image.open(album_art_path)
        album_art.thumbnail((100, 100))  # Resize the image
        album_art_photo = ImageTk.PhotoImage(album_art)
        album_art_label.config(image=album_art_photo)
        album_art_label.image = album_art_photo
    else:
        album_art_label.config(image=None)  # Clear the image


# Get a list of audio files in the "Music" directory
audio_files = [f for f in os.listdir(music_directory) if f.endswith((".mp3", ".wav"))]

# Initialize the index of the current audio file
current_audio_index = 0

# Directory to save album art images
album_art_output_directory = "album_art"
if not os.path.exists(album_art_output_directory):
    os.makedirs(album_art_output_directory)

# Create a main window
root = tk.Tk()
root.title("Music Widget")

# Create a frame for the music widget with a custom background color
music_widget_frame = tk.Frame(
    root, width=300, height=250, relief="solid", bd=2, padx=20, pady=20, bg="#2b2b2b"
)
music_widget_frame.pack(padx=20, pady=20)

# Create a frame for song information
song_info_frame = tk.Frame(music_widget_frame, bg="#3a3a3a")
song_info_frame.pack(pady=10)

# Create labels to display song information
song_name_label = tk.Label(
    song_info_frame, text="", font=("Arial", 12), bg="#3a3a3a", fg="#ffffff"
)
song_name_label.pack()
artist_label = tk.Label(
    song_info_frame, text="", font=("Arial", 12), bg="#3a3a3a", fg="#ffffff"
)
artist_label.pack()
album_label = tk.Label(
    song_info_frame, text="", font=("Arial", 12), bg="#3a3a3a", fg="#ffffff"
)
album_label.pack()

# Create a label for album art (initialize it to None)
album_art_label = tk.Label(song_info_frame, image=None, bg="#3a3a3a")
album_art_label.pack()

# Create icons for buttons
play_icon = PhotoImage(file="play.png")
pause_icon = PhotoImage(file="pause.png")
stop_icon = PhotoImage(file="stop.png")
next_icon = PhotoImage(file="next.png")

# Create custom styles for buttons
button_style = {
    "bg": "#3a3a3a",  # Background color
    "fg": "#ffffff",  # Text color
    "relief": "flat",  # Border style
    "font": ("Arial", 12),
}

# Add buttons with custom styles
play_button = tk.Button(
    music_widget_frame,
    image=play_icon,
    command=lambda: play_audio(
        os.path.join(music_directory, audio_files[current_audio_index])
    ),
    **button_style,
)
play_button.pack(side="left", padx=5)
pause_button = tk.Button(
    music_widget_frame, image=pause_icon, command=pause_audio, **button_style
)
pause_button.pack(side="left", padx=5)
stop_button = tk.Button(
    music_widget_frame, image=stop_icon, command=stop_audio, **button_style
)
stop_button.pack(side="left", padx=5)
next_button = tk.Button(
    music_widget_frame, image=next_icon, command=play_next_audio, **button_style
)
next_button.pack(side="left", padx=5)

# Play the first audio file
play_audio(os.path.join(music_directory, audio_files[current_audio_index]))

# Start the Tkinter main loop
root.mainloop()
