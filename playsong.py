import os
import subprocess


def search_and_play_music(music_folder):
    # Check if the specified folder exists
    if not os.path.exists(music_folder):
        print(f"The folder '{music_folder}' does not exist.")
        return

    # List all files in the music folder
    music_files = [
        os.path.join(music_folder, filename) for filename in os.listdir(music_folder)
    ]

    if not music_files:
        print(f"No music files found in '{music_folder}'.")
        return

    # Filter for common music file extensions (you can extend this list)
    valid_extensions = [".mp3", ".wav", ".flac", ".ogg", ".m4a", ".wma"]
    music_files = [
        file
        for file in music_files
        if any(file.endswith(ext) for ext in valid_extensions)
    ]

    if not music_files:
        print(f"No supported music files found in '{music_folder}'.")
        return

    # Display the list of music files
    print("Found music files:")
    for i, music_file in enumerate(music_files, start=1):
        print(f"{i}. {os.path.basename(music_file)}")

    # Prompt the user to select a song
    while True:
        try:
            choice = int(input("Enter the number of the song to play (0 to exit): "))
            if choice == 0:
                break
            elif 1 <= choice <= len(music_files):
                selected_song = music_files[choice - 1]
                print(f"Playing: {os.path.basename(selected_song)}")

                # Choose either MPlayer or MPV to play the song
                player = "mpv"  # Change to "mpv" if you prefer MPV
                subprocess.run([player, selected_song])
            else:
                print("Invalid choice. Please enter a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    music_folder = input("Enter the path to your Music folder: ")
    search_and_play_music(music_folder)
