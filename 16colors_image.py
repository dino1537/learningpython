from PIL import Image
import collections
import colorsys

# Open the image
image_path = "/home/dino/gallery-dl/wallhaven/cat_leaves.png"  # Replace with your image file path
image = Image.open(image_path)

# Resize the image for faster processing (optional)
# You can skip this step if you want to work with the original size
max_size = (100, 100)  # Adjust the size as needed
image = image.resize(max_size)

# Convert the image to RGB mode if it's not already
image = image.convert("RGB")

# Get the colors from the image
pixel_data = list(image.getdata())

# Define a function to convert RGB to hex
def rgb_to_hex(rgb):
    return "#{:02x}{:02x}{:02x}".format(rgb[0], rgb[1], rgb[2])

# Count the occurrences of each color
color_count = collections.Counter(pixel_data)

# Sort colors by frequency in descending order
sorted_colors = sorted(color_count.items(), key=lambda x: x[1], reverse=True)

# Extract the 16 most prominent colors
top_colors = sorted_colors[:16]

print("16 Most Prominent Colors and their Hex Codes:")
for color, count in top_colors:
    hex_code = rgb_to_hex(color)
    print(f"{hex_code}: {count} pixels")

# Close the image
image.close()

