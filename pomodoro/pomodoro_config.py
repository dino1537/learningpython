import subprocess
import time
import sys
import json
import threading
import os

def show_notification(message):
    subprocess.Popen(["notify-send", "Pomodoro Timer", message])

def pomodoro_timer(settings, stop_event):
    work_duration = settings["work_duration"] * 60
    break_duration = settings["break_duration"] * 60
    long_break_interval = settings["long_break_interval"]
    custom_messages = settings.get("custom_messages", {})
    custom_breaks = settings.get("custom_breaks", {})

    sessions_completed = 0
    long_break_duration = 15 * 60

    tasks = []  # List to store tasks associated with work sessions

    def exit_handler():
        print("\nPomodoro timer stopped.")
        stop_event.set()
        if tasks:
            print("\nCompleted Tasks:")
            for i, task in enumerate(tasks, 1):
                print(f"{i}. {task}")
        sys.exit(0)

    def check_for_stop():
        while not stop_event.is_set():
            char = input("Enter 'q' to stop the timer or 'terminate' to exit: ")
            if char.strip().lower() == "q":
                exit_handler()
            elif char.strip().lower() == "terminate":
                os.kill(os.getpid(), 9)  # Terminate the script and its background process
            
    # Start a separate thread to check for the stop and terminate commands
    stop_thread = threading.Thread(target=check_for_stop)
    stop_thread.daemon = True
    stop_thread.start()

    while not stop_event.is_set():
        try:
            # Work session
            show_notification(custom_messages.get("work", f"Work for {work_duration // 60} minutes!"))
            time.sleep(work_duration)
            
            sessions_completed += 1

            if sessions_completed % long_break_interval == 0:
                # Long break
                show_notification(custom_messages.get("long_break", f"Take a {long_break_duration // 60}-minute long break!"))
                time.sleep(long_break_duration)
            else:
                # Short break or custom break
                break_message = custom_messages.get("short_break", f"Take a {break_duration // 60}-minute break!")
                if sessions_completed in custom_breaks:
                    break_duration = custom_breaks[sessions_completed] * 60
                    break_message = custom_messages.get("custom_break", f"Take a {break_duration // 60}-minute custom break!")
                show_notification(break_message)
                time.sleep(break_duration)

        except KeyboardInterrupt:
            exit_handler()

if __name__ == "__main__":
    try:
        with open("config.json", "r") as config_file:
            settings = json.load(config_file)
    except FileNotFoundError:
        print("Config file not found. Using default settings.")
        settings = {
            "work_duration": 25,
            "break_duration": 5,
            "long_break_interval": 4,
            "custom_messages": {},
            "custom_breaks": {}
        }

    stop_event = threading.Event()

    print("Pomodoro timer is running. Enter 'q' to stop or 'terminate' to exit.")
    pomodoro_timer(settings, stop_event)
