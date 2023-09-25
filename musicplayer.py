
import os
import pygame
import argparse
import eyed3

def list_music_files(directory):
    music_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.mp3', '.wav', '.ogg', '.flac')):
                music_files.append(os.path.join(root, file))
    return music_files

def play_music(music_file, volume=1.0):
    pygame.mixer.init()
    pygame.mixer.music.set_volume(volume)
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

def display_metadata(music_file):
    audiofile = eyed3.load(music_file)
    if audiofile.tag:
        print(f"Title: {audiofile.tag.title}")
        print(f"Artist: {audiofile.tag.artist}")
        print(f"Album: {audiofile.tag.album}")
        print(f"Year: {audiofile.tag.getBestDate()}")
    else:
        print("No metadata available.")

def main():
    parser = argparse.ArgumentParser(description='Play music from your local library')
    parser.add_argument('directory', metavar='DIRECTORY', type=str, help='Directory containing music files')
    args = parser.parse_args()

    directory = args.directory

    if not os.path.isdir(directory):
        print(f"Error: '{directory}' is not a valid directory.")
        return

    music_files = list_music_files(directory)

    if not music_files:
        print(f"No music files found in '{directory}'.")
        return

    print("Available music files:")
    for i, music_file in enumerate(music_files):
        print(f"{i + 1}. {os.path.basename(music_file)}")

    pygame.mixer.init()
    pygame.mixer.music.set_volume(0.5)  # Set an initial volume (0.5 means 50% volume)
    while True:
        try:
            choice = input("Enter the number of the music file you want to play (0 to exit): ")
            if choice == '0':
                break
            elif choice.isdigit():
                choice = int(choice)
                if 1 <= choice <= len(music_files):
                    selected_music_file = music_files[choice - 1]
                    print(f"Selected: {os.path.basename(selected_music_file)}")
                    play_music(selected_music_file)
                    while pygame.mixer.music.get_busy():
                        command = input("Enter 'p' to pause, 'r' to resume, 's' to stop, 'v' to adjust volume, or '0' to exit: ")
                        if command == 'p':
                            pygame.mixer.music.pause()
                        elif command == 'r':
                            pygame.mixer.music.unpause()
                        elif command == 's':
                            pygame.mixer.music.stop()
                        elif command == 'v':
                            new_volume = float(input("Enter new volume (0.0 to 1.0): "))
                            pygame.mixer.music.set_volume(new_volume)
                        elif command == '0':
                            pygame.mixer.music.stop()
                            break
                else:
                    print("Invalid choice. Please enter a valid number.")
            else:
                print("Invalid input. Please enter a number.")
        except KeyboardInterrupt:
            print("\nExiting...")
            pygame.mixer.quit()
            sys.exit(0)

    pygame.mixer.quit()

if __name__ == "__main__":
    main()
