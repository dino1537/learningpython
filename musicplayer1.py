import os
import pygame
import argparse
import eyed3
from rich.console import Console
from rich.table import Table


def list_music_files(directory):
    music_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".mp3", ".wav", ".ogg", ".flac")):
                music_files.append(os.path.join(root, file))
    music_files.sort(key=lambda x: (os.path.splitext(x)[1], x))
    return music_files


def play_music(music_file, volume=1.0):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()


def pause_music():
    pygame.mixer.music.pause()


def unpause_music():
    pygame.mixer.music.unpause()


def stop_music():
    pygame.mixer.music.stop()


def set_volume(volume):
    pygame.mixer.music.set_volume(volume)


def display_metadata(music_file):
    audiofile = eyed3.load(music_file)
    if audiofile:
        console = Console()
        table = Table()
        table.add_column("Metadata", style="bold")
        table.add_column("Value")
        if audiofile.tag:
            table.add_row("Title", audiofile.tag.title)
            table.add_row("Artist", audiofile.tag.artist)
            table.add_row("Album", audiofile.tag.album)
            year = audiofile.tag.getBestDate()
            year_str = str(year) if year else "N/A"
            table.add_row("Year", year_str)
        else:
            table.add_row("Title", "N/A")
            table.add_row("Artist", "N/A")
            table.add_row("Album", "N/A")
            table.add_row("Year", "N/A")
        console.print(table)
    else:
        print("No metadata available.")


def main():
    parser = argparse.ArgumentParser(description="Play music from your local library")
    parser.add_argument(
        "directory",
        metavar="DIRECTORY",
        type=str,
        help="Directory containing music files",
    )
    args = parser.parse_args()

    directory = args.directory

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    music_files = list_music_files(directory)

    if not music_files:
        print(f"No music files found in '{directory}'.")
        return

    console = Console()
    console.print("Select a music file to play (q to quit):")

    current_music_file = None
    current_volume = 1.0

    while True:
        table = Table(show_header=True, header_style="bold")
        table.add_column("Index", style="cyan")
        table.add_column("File Name")
        for i, music_file in enumerate(music_files):
            table.add_row(str(i + 1), os.path.basename(music_file))

        console.print(table)
        console.print(
            "Enter the corresponding number to perform an action (q to quit):",
            style="yellow",
        )
        console.print("p: Play")
        console.print("s: Stop")
        console.print("v: Set Volume")
        console.print("n: Next")
        console.print("b: Previous")

        try:
            choice = input().lower()
        except ValueError:
            choice = ""

        if choice == "q":
            break
        elif choice.isdigit():
            choice = int(choice)
            if choice >= 1 and choice <= len(music_files):
                selected_music_file = music_files[choice - 1]
                if current_music_file != selected_music_file:
                    if current_music_file:
                        stop_music()
                    current_music_file = selected_music_file
                    console.print(
                        f"Selected: {os.path.basename(selected_music_file)}",
                        style="green",
                    )
                    play_music(selected_music_file, current_volume)
                else:
                    console.print(
                        f"Resuming: {os.path.basename(selected_music_file)}",
                        style="green",
                    )
                    unpause_music()
            else:
                console.print(
                    "Invalid choice. Please enter a valid number.", style="red"
                )
        else:
            if choice == "p":
                if current_music_file:
                    console.print(
                        f"Resuming: {os.path.basename(current_music_file)}",
                        style="green",
                    )
                    unpause_music()
                else:
                    console.print(
                        "No music selected. Please choose a song to play.", style="red"
                    )
            elif choice == "s":
                if current_music_file:
                    console.print("Stopping music", style="red")
                    stop_music()
                    current_music_file = None
                else:
                    console.print(
                        "No music playing. Select a song to play.", style="red"
                    )
            elif choice == "v":
                try:
                    console.print("Enter volume (0.0 to 1.0):", style="yellow")
                    volume = float(input())
                    if 0.0 <= volume <= 1.0:
                        current_volume = volume
                        set_volume(current_volume)
                        console.print(f"Volume set to {volume}", style="yellow")
                    else:
                        console.print(
                            "Invalid volume. Enter a value between 0.0 and 1.0.",
                            style="red",
                        )
                except ValueError:
                    console.print(
                        "Invalid input. Please enter a valid volume value.", style="red"
                    )
            elif choice == "n":
                if current_music_file:
                    console.print("Playing next song", style="green")
                    stop_music()
                    index = music_files.index(current_music_file)
                    if index < len(music_files) - 1:
                        selected_music_file = music_files[index + 1]
                        current_music_file = selected_music_file
                        play_music(selected_music_file, current_volume)
                else:
                    console.print(
                        "No music playing. Select a song to play.", style="red"
                    )
            elif choice == "b":
                if current_music_file:
                    console.print("Playing previous song", style="green")
                    stop_music()
                    index = music_files.index(current_music_file)
                    if index > 0:
                        selected_music_file = music_files[index - 1]
                        current_music_file = selected_music_file
                        play_music(selected_music_file, current_volume)
                else:
                    console.print(
                        "No music playing. Select a song to play.", style="red"
                    )
            else:
                console.print(
                    "Invalid command. Please enter a valid command.", style="red"
                )


if __name__ == "__main__":
    main()
