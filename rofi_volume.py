#!/usr/bin/env python3
import subprocess
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont


# Get the current volume using amixer
def get_current_volume():
    try:
        result = subprocess.check_output(["amixer", "get", "Master"])
        result = result.decode("utf-8")
        volume_str = result.split("[")[1].split("]")[0]
        return int(volume_str.rstrip("%"))
    except subprocess.CalledProcessError:
        pass
    return 0


# Set the volume using amixer
def set_volume(volume):
    try:
        subprocess.call(["amixer", "set", "Master", f"{volume}%"])
    except subprocess.CalledProcessError:
        pass


# Create a modern and sleek volume control dialog
def show_volume_slider():
    current_volume = get_current_volume()

    def set_and_close():
        nonlocal current_volume
        new_volume = volume_slider.get()
        if new_volume != current_volume:
            set_volume(new_volume)
            current_volume = new_volume
        root.destroy()

    # Create a floating window on the primary screen
    root = tk.Tk()
    root.title("Volume Control")
    root.overrideredirect(True)  # Remove window border and decorations
    root.attributes("-topmost", True)  # Keep the window on top

    # Determine the screen width and height of the primary screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Set the position of the window (adjust as needed)
    x = 100  # X-coordinate (left)
    y = 100  # Y-coordinate (top)

    window_width = 300  # Adjust this width as needed
    window_height = 200  # Adjust this height as needed

    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    style = ttk.Style()
    style.theme_use("clam")  # Use the 'clam' theme for a modern appearance

    # Define custom colors and font
    style.configure(
        "TButton",
        background="#74c7ec",  # Button background color
        foreground="#1e1e2e",  # Button text color
        font=("NotoSans Nerd Font Regular", 12),  # Button font
    )

    style.configure(
        "TLabel",
        background="#1e1e2e",  # Window background color
        foreground="white",  # Window font color
    )

    style.configure(
        "Horizontal.TScale",
        troughcolor="#74c7ec",  # Slider trough color
        sliderlength=15,  # Slider length
        sliderrelief="flat",  # Slider relief style
        sliderthickness=15,  # Slider thickness
        font=("NotoSans Nerd Font Regular", 10),  # Slider font
    )

    font = tkFont.Font(family="NotoSans Nerd Font Regular", size=14)

    volume_frame = ttk.Frame(root)
    volume_frame.pack(padx=20, pady=20)

    volume_label = ttk.Label(volume_frame, text=f"Volume: {current_volume}%", font=font)
    volume_label.grid(row=0, column=0, columnspan=2, pady=10)

    volume_slider = ttk.Scale(
        volume_frame,
        from_=0,
        to=100,
        orient="horizontal",
        length=200,
        style="Horizontal.TScale",
    )
    volume_slider.set(current_volume)
    volume_slider.grid(row=1, column=0, columnspan=2)

    ok_button = ttk.Button(
        volume_frame, text="OK", command=set_and_close, style="TButton"
    )
    ok_button.grid(row=2, column=0, pady=10)

    cancel_button = ttk.Button(
        volume_frame, text="Cancel", command=root.destroy, style="TButton"
    )
    cancel_button.grid(row=2, column=1, pady=10)

    root.mainloop()


if __name__ == "__main__":
    show_volume_slider()
