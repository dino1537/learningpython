import os
import tkinter as tk
from tkinter import PhotoImage

import pygame

# Initialize pygame for audio
pygame.mixer.init()

# Create a main window
root = tk.Tk()
root.title("Music Widget")
root.configure(bg="#100F0F")  # Set the background color of the root window

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

# Function to exit the widget
def exit_widget():
    root.destroy()

# Get a list of audio files in the "Music" directory
music_directory = "/home/dino/Music/Italian"
audio_files = [f for f in os.listdir(music_directory) if f.endswith((".mp3", ".flac", ".wav"))]

# Initialize the index of the current audio file
current_audio_index = 0

# Create a frame for the music widget
music_widget_frame = tk.Frame(
    root, width=150, height=75, relief="solid", bd=2, padx=5, pady=5, bg="#100F0F"
)
music_widget_frame.pack(padx=5, pady=5)

# Add an audio player to the frame
audio_player = tk.Frame(music_widget_frame, bd=2, relief="solid", bg="#100F0F")
audio_player.pack(pady=10, padx=10, fill="x")

# Create icons for buttons
play_icon = PhotoImage(file="play.png")
pause_icon = PhotoImage(file="pause.png")
stop_icon = PhotoImage(file="stop.png")
next_icon = PhotoImage(file="next.png")
exit_icon = PhotoImage(file="exit.png")  # Add an icon for the exit button

# Add buttons with icons
play_button = tk.Button(
    music_widget_frame,
    image=play_icon,
    command=lambda: play_audio(
        os.path.join(music_directory, audio_files[current_audio_index])
    ),
    bg="#100F0F",  # Set the background color of the button
)
play_button.pack(side="left", padx=2)
pause_button = tk.Button(music_widget_frame, image=pause_icon, command=pause_audio, bg="#100F0F")
pause_button.pack(side="left", padx=2)
stop_button = tk.Button(music_widget_frame, image=stop_icon, command=stop_audio, bg="#100F0F")
stop_button.pack(side="left", padx=2)
next_button = tk.Button(music_widget_frame, image=next_icon, command=play_next_audio, bg="#100F0F")
next_button.pack(side="left", padx=2)
exit_button = tk.Button(music_widget_frame, image=exit_icon, command=exit_widget, bg="#100F0F")  # Add an exit button
exit_button.pack(side="left", padx=2)

# Play the first audio file
play_audio(os.path.join(music_directory, audio_files[current_audio_index]))

# Start the Tkinter main loop
root.mainloop()
