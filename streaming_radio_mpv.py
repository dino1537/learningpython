import subprocess
import time
import json
import threading
import argparse
import logging


def load_config(config_file_path):
    try:
        # Load configuration from a JSON file
        with open(config_file_path, "r") as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_file_path}' not found.")
        exit(1)
    except json.JSONDecodeError:
        print(
            f"Error: Invalid JSON format in the configuration file '{config_file_path}'."
        )
        exit(1)


# ... (rest of the script remains the same)
def select_radio_station(config):
    stations = config.get("stations", [])

    if not stations:
        print("Error: No radio stations found in the configuration.")
        exit(1)

    print("Available Radio Stations:")
    for i, station in enumerate(stations, start=1):
        print(f"{i}. {station['name']}")

    while True:
        try:
            choice = int(
                input("Enter the number of the station you want to listen to: ")
            )
            if 1 <= choice <= len(stations):
                return stations[choice - 1]
            else:
                print("Invalid choice. Please enter a valid station number.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def stream_radio_station(station_url, stream_duration, volume):
    try:
        # Define the command to play the radio stream with mpv
        command = ["mpv", station_url, f"--volume={volume}"]

        # Start the mpv player to stream the radio station
        mpv_process = subprocess.Popen(command)

        # Create a thread to listen for user input to exit
        exit_thread = threading.Thread(target=exit_listener)
        exit_thread.start()

        start_time = time.time()
        while mpv_process.poll() is None:
            elapsed_time = time.time() - start_time
            print(f"Streaming... Elapsed time: {int(elapsed_time)} seconds", end="\r")
            time.sleep(1)

        print("\nStreaming completed successfully.")
    except FileNotFoundError:
        print("Error: mpv player not found. Please make sure mpv is installed.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


def exit_listener():
    # Listen for 'q' input to exit the script gracefully
    while True:
        user_input = input("Press 'q' to stop streaming: ")
        if user_input.lower() == "q":
            break


def setup_logging():
    logging.basicConfig(
        filename="streaming.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s: %(message)s",
    )


def main():
    setup_logging()

    parser = argparse.ArgumentParser(description="Stream an internet radio station.")
    parser.add_argument(
        "--config",
        type=str,
        default="config.json",
        help="Path to the configuration file (default: config.json)",
    )

    args = parser.parse_args()
    config_file_path = args.config

    try:
        config = load_config(config_file_path)
        station_info = select_radio_station(config)

        station_url = station_info.get("url")
        stream_duration = station_info.get("duration")
        volume = station_info.get("volume")

        if not station_url or not stream_duration:
            print("Error: Selected station is missing required settings.")
            exit(1)

        stream_radio_station(station_url, stream_duration, volume)
    except KeyboardInterrupt:
        print("\nStreaming interrupted by user.")
        logging.info("Streaming interrupted by user.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
