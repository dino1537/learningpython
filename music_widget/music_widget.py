import tkinter as tk
from tkinter import PhotoImage
import os
import pygame

# Initialize pygame for audio
pygame.mixer.init()

# Create a main window
root = tk.Tk()
root.title("Music Widget")


# Function to play the audio
def play_audio(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()


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


# Get a list of audio files in the "Music" directory
music_directory = "/home/dino/Music"
audio_files = [f for f in os.listdir(music_directory) if f.endswith((".mp3", ".wav"))]

# Initialize the index of the current audio file
current_audio_index = 0

# Create a frame for the music widget
music_widget_frame = tk.Frame(
    root, width=300, height=250, relief="solid", bd=2, padx=20, pady=20
)
music_widget_frame.pack(padx=20, pady=20)

# Add an audio player to the frame
audio_player = tk.Frame(music_widget_frame, bd=2, relief="solid")
audio_player.pack(pady=10, padx=10, fill="x")

# Create icons for buttons
play_icon = PhotoImage(file="play.png")
pause_icon = PhotoImage(file="pause.png")
stop_icon = PhotoImage(file="stop.png")
next_icon = PhotoImage(file="next.png")

# Add buttons with icons
play_button = tk.Button(
    music_widget_frame,
    image=play_icon,
    command=lambda: play_audio(
        os.path.join(music_directory, audio_files[current_audio_index])
    ),
)
play_button.pack(side="left", padx=5)
pause_button = tk.Button(music_widget_frame, image=pause_icon, command=pause_audio)
pause_button.pack(side="left", padx=5)
stop_button = tk.Button(music_widget_frame, image=stop_icon, command=stop_audio)
stop_button.pack(side="left", padx=5)
next_button = tk.Button(music_widget_frame, image=next_icon, command=play_next_audio)
next_button.pack(side="left", padx=5)

# Play the first audio file
play_audio(os.path.join(music_directory, audio_files[current_audio_index]))

# Start the Tkinter main loop
root.mainloop()
