from PIL import Image
import collections

# Open the image
image_path = "/home/dino/gallery-dl/wallhaven/warship.jpg"  # Replace with your image file path
image = Image.open(image_path)

# Resize the image for faster processing (optional)
# You can skip this step if you want to work with the original size
max_size = (100, 100)  # Adjust the size as needed
image=image.resize(max_size)

# Convert the image to RGB mode if it's not already
image = image.convert("RGB")

# Get the colors from the image
pixel_data = list(image.getdata())

# Define a function to convert RGB to hex
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

# Count the occurrences of each color
color_count = collections.Counter(pixel_data)

# Extract unique colors and convert them to hex
unique_colors = list(color_count.keys())

print("Unique Colors and their Hex Codes:")
for color in unique_colors:
    hex_code = rgb_to_hex(color)
    print(f"{hex_code}: {color_count[color]} pixels")

# If you want to save the hex codes to a text file
with open("color_codes.txt", "w") as file:
    for color in unique_colors:
        hex_code = rgb_to_hex(color)
        file.write(f"{hex_code}: {color_count[color]} pixels\n")

# Close the image
image.close()

