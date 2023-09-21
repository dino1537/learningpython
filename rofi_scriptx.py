import os
import subprocess

# Directory containing your scripts.
script_directory = "/home/dino/applications/scripts"

# Get a list of all files in the script directory.
script_files = [f for f in os.listdir(script_directory) if os.path.isfile(os.path.join(script_directory, f))]

# Create a newline-separated string of script files.
script_list = "\n".join(script_files)

# Use Rofi to display the list of script files and let the user choose one.
rofi_process = subprocess.Popen(["rofi", "-dmenu", "-p", "Select a script:"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, _ = rofi_process.communicate(input=script_list.encode())

# Get the selected script filename.
selected_script_filename = stdout.decode().strip()

# Construct the full path to the selected script.
selected_script_path = os.path.join(script_directory, selected_script_filename)

if os.path.exists(selected_script_path):
    try:
        # Execute the selected script.
        subprocess.call(["bash", selected_script_path])
    except Exception as e:
        print(f"Error executing the selected script: {e}")
else:
    print("No script selected or the selected script does not exist.")

