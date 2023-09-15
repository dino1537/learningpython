import subprocess

# Replace this URL with the URL of the internet radio station you want to stream
radio_station_url = "http://stream.104.6rtl.com/rtl-60er70er/mp3-192"

# Define the command to play the radio stream with mpv
command = ["mpv", radio_station_url]

# Start the mpv player to stream the radio station
mpv_process = subprocess.Popen(command)

# You can add a delay or a timer to control how long the stream plays
# For example, wait for 1 hour (3600 seconds)
import time
time.sleep(3600)

# Terminate the mpv process when you're done streaming
mpv_process.terminate()

