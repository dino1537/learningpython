
import subprocess

# Define the MPD host and port
MPD_HOST = 'localhost'
MPD_PORT = '6600'

# Function to send commands to MPD
def mpd_command(command):
    subprocess.run(['mpc', '-h', MPD_HOST, '-p', MPD_PORT, command])

# Function to list available playlists
def list_playlists():
    playlists = subprocess.check_output(['mpc', '-h', MPD_HOST, '-p', MPD_PORT, 'lsplaylist']).decode('utf-8').split('\n')
    return [p for p in playlists if p]

# Function to show a Rofi menu with playlist options
def show_playlist_menu(playlists):
    rofi_input = "\n".join(playlists)
    rofi_cmd = f'echo -e """{rofi_input}""" | rofi -dmenu -p "Select Playlist:" -format i -selected-row 0'
    selected_index = int(subprocess.check_output(rofi_cmd, shell=True).decode('utf-8').strip())
    return playlists[selected_index]

# Function to control the music player
def main():
    while True:
        # Show the main control menu
        menu_options = """Play/Pause
Stop
Next
Previous
Change Playlist
Volume Up
Volume Down
Quit"""
        rofi_cmd = f'echo -e """{menu_options}""" | rofi -dmenu -p "Music Player Controller:" -format i -selected-row 0'
        choice = subprocess.check_output(rofi_cmd, shell=True).decode('utf-8').strip()

        if choice == '0':  # Play/Pause
            mpd_command('toggle')
        elif choice == '1':  # Stop
            mpd_command('stop')
        elif choice == '2':  # Next
            mpd_command('next')
        elif choice == '3':  # Previous
            mpd_command('prev')
        elif choice == '4':  # Change Playlist
            playlists = list_playlists()
            if not playlists:
                continue
            selected_playlist = show_playlist_menu(playlists)
            mpd_command(f'clear; load "{selected_playlist}"')
            mpd_command('play')
        elif choice == '5':  # Volume Up
            # Prompt the user for a volume level between 1 and 100
            volume_level = input("Enter volume level (1-100): ")
            try:
                volume_level = int(volume_level)
                if 1 <= volume_level <= 100:
                    mpd_command(f'volume {volume_level}')
                else:
                    print("Volume level must be between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 100.")
        elif choice == '6':  # Volume Down
            # Prompt the user for a volume level between 1 and 100
            volume_level = input("Enter volume level (1-100): ")
            try:
                volume_level = int(volume_level)
                if 1 <= volume_level <= 100:
                    mpd_command(f'volume {volume_level}')
                else:
                    print("Volume level must be between 1 and 100.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 100.")
        elif choice == '7':  # Quit
            break

if __name__ == "__main__":
    main()
