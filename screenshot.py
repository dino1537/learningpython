from PIL import ImageGrab
from datetime import datetime
import os
import subprocess
import re

# Function to take a screenshot of a specific monitor
def capture_screenshot(monitor_info, monitor_index):
    left, top, right, bottom = monitor_info
    
    # Capture the screenshot of the selected monitor
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    
    # Get the current date and time for the filename
    current_datetime = datetime.now().strftime("%Y%m%d%H%M%S")
    
    # Set the complete file path with the timestamp
    file_path = f"/home/dino/Pictures/screenshots/screenshot_{current_datetime}_monitor{monitor_index}.png"
    
    # Save the screenshot
    screenshot.save(file_path)
    print(f"Screenshot saved as {file_path}")

# Function to get monitor information using xrandr
def get_monitor_info():
    monitor_info = []
    xrandr_output = subprocess.check_output(["xrandr"]).decode("utf-8")
    
    # Use regular expressions to extract monitor information
    monitor_pattern = re.compile(r'([\w-]+)\s+connected\s+(?:primary\s+)?(\d+)x(\d+)\+(\d+)\+(\d+)')
    matches = monitor_pattern.findall(xrandr_output)
    
    for match in matches:
        monitor_name, width, height, left, top = match
        right = int(left) + int(width)
        bottom = int(top) + int(height)
        monitor_info.append((int(left), int(top), right, bottom))
    
    return monitor_info

if __name__ == "__main__":
    # Get monitor information using xrandr
    monitors = get_monitor_info()
    
    for monitor_index, monitor_info in enumerate(monitors):
        print(f"Monitor {monitor_index}: {monitor_info}")
    
    # Ask the user to select a monitor
    monitor_index = int(input("Enter the number of the monitor to capture: "))
    
    if monitor_index < 0 or monitor_index >= len(monitors):
        print("Invalid selection. Please choose a valid monitor.")
    else:
        capture_screenshot(monitors[monitor_index], monitor_index)

