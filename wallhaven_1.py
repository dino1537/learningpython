import os
import requests
import json
import subprocess
import argparse
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# User-configurable variables with defaults
DEFAULT_WALDIR = os.path.expanduser("~/.local/share/wallhaven")
DEFAULT_CACHEDIR = os.path.expanduser("~/.cache/wallhaven")
DEFAULT_MAX_PAGES = 4
DEFAULT_SORTING = "relevance"
DEFAULT_QUALITY = "large"
DEFAULT_ATLEAST = "1920x1080"

# Function to fetch search results from Wallhaven API
def get_results(query, max_pages, sorting, quality, atleast):
    data = []
    for page_no in range(1, max_pages + 1):
        params = {
            "q": query,
            "page": page_no,
            "atleast": atleast,
            "sorting": sorting,
        }
        response = requests.get("https://wallhaven.cc/api/v1/search", params=params)
        if response.status_code == 200:
            data += response.json().get("data", [])
        else:
            logger.error("Failed to fetch data from Wallhaven API. Status code: %s", response.status_code)
    return data

# Function to cache thumbnails
def cache_thumbnails(thumbnails, cachedir):
    os.makedirs(cachedir, exist_ok=True)
    logger.info("Caching thumbnails...")
    for url in thumbnails:
        filename = os.path.join(cachedir, os.path.basename(url))
        subprocess.run(["curl", "-o", filename, url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.info("Thumbnails cached in %s", cachedir)

# Function to download selected wallpapers
def download_wallpapers(selected_images, walldir):
    if not selected_images:
        logger.warning("No images selected for download.")
        return
    
    os.makedirs(walldir, exist_ok=True)
    logger.info("Downloading wallpapers...")
    for image_id in selected_images:
        image_id = os.path.splitext(os.path.basename(image_id))[0]
        for item in search_results:
            if item["id"] == image_id:
                image_url = item["path"]
                break
        else:
            logger.warning("Image with ID %s not found. Skipping.", image_id)
            continue
        subprocess.run(["curl", "-o", os.path.join(walldir, os.path.basename(image_url)), image_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    logger.info("Wallpapers downloaded in %s", walldir)

# Function to run the script
def run_script(query, walldir, cachedir, max_pages, sorting, quality, atleast):
    global search_results
    logger.info("Getting data...")
    search_results = get_results(query, max_pages, sorting, quality, atleast)

    if not search_results:
        logger.warning("No images found.")
        return
    
    logger.info("Select wallpapers to download:")
    for i, item in enumerate(search_results):
        print(f"{i + 1}. {item['id']} - {item['resolution']}")

    selected_indices = input("Enter the indices of the wallpapers to download (comma-separated): ").split(",")
    selected_images = [search_results[int(index) - 1]["id"] for index in selected_indices]
    
    logger.info("Selected images for download:")
    for image_id in selected_images:
        print(image_id)
    
    confirmation = input("Confirm the download (yes/no): ").strip().lower()
    if confirmation == "yes":
        download_wallpapers(selected_images, walldir)
    else:
        logger.info("Download canceled.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Wallhaven Wallpaper Downloader")
    parser.add_argument("query", help="Search query for wallpapers")
    parser.add_argument("--walldir", default=DEFAULT_WALDIR, help="Download directory for wallpapers")
    parser.add_argument("--cachedir", default=DEFAULT_CACHEDIR, help="Thumbnail cache directory")
    parser.add_argument("--max-pages", type=int, default=DEFAULT_MAX_PAGES, help="Maximum number of search result pages")
    parser.add_argument("--sorting", default=DEFAULT_SORTING, help="Sorting method (e.g., relevance, random)")
    parser.add_argument("--quality", default=DEFAULT_QUALITY, help="Thumbnail quality (e.g., large, original)")
    parser.add_argument("--atleast", default=DEFAULT_ATLEAST, help="Minimum resolution (e.g., 1920x1080)")
    
    args = parser.parse_args()

    try:
        run_script(args.query, args.walldir, args.cachedir, args.max_pages, args.sorting, args.quality, args.atleast)
    except KeyboardInterrupt:
        logger.info("Download canceled due to user interruption.")
    except Exception as e:
        logger.error("An error occurred: %s", str(e))
