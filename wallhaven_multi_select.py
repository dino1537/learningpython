import os
import requests
import json
import subprocess
import argparse
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QWidget, QProgressBar, QAbstractItemView
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import QObject, pyqtSignal

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
def download_wallpapers(selected_images, walldir, progress_callback):
    if not selected_images:
        logger.warning("No images selected for download.")
        return
    
    os.makedirs(walldir, exist_ok=True)
    logger.info("Downloading wallpapers...")
    total_images = len(selected_images)
    for i, image_id in enumerate(selected_images, start=1):
        image_id = os.path.splitext(os.path.basename(image_id))[0]
        for item in search_results:
            if item["id"] == image_id:
                image_url = item["path"]
                break
        else:
            logger.warning("Image with ID %s not found. Skipping.", image_id)
            continue
        filename = os.path.join(walldir, os.path.basename(image_url))
        subprocess.run(["curl", "-o", filename, image_url], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        progress_callback.emit(i, total_images)
    logger.info("Wallpapers downloaded in %s", walldir)

# Create a PyQt5 application for the GUI
app = QApplication([])

# Define a custom signal for updating the progress bar
class ProgressSignal(QObject):
    update_progress = pyqtSignal(int, int)

# Function to run the script
def run_script(args):
    global search_results

    # Function to download the selected images
    def download_selected_images():
        selected_items = list_widget.selectedItems()
        selected_images = [item.data(Qt.UserRole) for item in selected_items]
        if not selected_images:
            QMessageBox.warning(main_window, "No Selection", "Please select wallpapers to download.")
            return
        progress_bar.setValue(0)  # Reset progress bar
        download_wallpapers(selected_images, args.walldir, progress_signal.update_progress)
        QMessageBox.information(main_window, "Download Complete", "Wallpapers downloaded successfully.")

    # Initialize the GUI
    main_window = QMainWindow()
    main_window.setWindowTitle("Wallhaven Wallpaper Downloader")
    central_widget = QWidget()
    main_window.setCentralWidget(central_widget)
    layout = QVBoxLayout()
    central_widget.setLayout(layout)

    # Create a list widget to display thumbnails
    list_widget = QListWidget()
    list_widget.setSelectionMode(QAbstractItemView.MultiSelection)  # Enable multiple selections
    layout.addWidget(list_widget)

    # Create a progress bar
    progress_bar = QProgressBar()
    layout.addWidget(progress_bar)

    # Create a progress signal object and connect it to the progress bar
    progress_signal = ProgressSignal()
    progress_signal.update_progress.connect(lambda value, max_value: progress_bar.setValue(int((value / max_value) * 100)))

    # Function to update the list widget with thumbnails
    def update_list_widget(query):
        list_widget.clear()
        search_results = get_results(query, args.max_pages, args.sorting, args.quality, args.atleast)
        for i, item in enumerate(search_results):
            thumbnail_url = item["thumbs"][args.quality]
            list_item = QListWidgetItem()
            list_widget.addItem(list_item)
            list_widget.setIconSize(QSize(200, 200))
            list_widget.setResizeMode(QListView.Adjust)
            list_widget.setFlow(QListView.LeftToRight)
            list_widget.setWrapping(True)
            list_widget.setViewMode(QListView.IconMode)
            pixmap = QPixmap()
            pixmap.loadFromData(requests.get(thumbnail_url).content)
            list_item.setIcon(QIcon(pixmap))
            list_item.setData(Qt.UserRole, item["id"])

    # Create a button to trigger the download
    download_button = QPushButton("Download Selected Wallpapers")
    download_button.clicked.connect(download_selected_images)

    # Create a button to change the download directory
    def select_directory():
        directory = QFileDialog.getExistingDirectory(main_window, "Select Download Directory", args.walldir)
        if directory:
            args.walldir = directory
            logger.info("Download directory set to: %s", args.walldir)

    directory_button = QPushButton("Select Download Directory")
    directory_button.clicked.connect(select_directory)

    # Initialize the list widget with search results
    search_results = get_results(args.query, args.max_pages, args.sorting, args.quality, args.atleast)
    update_list_widget(args.query)

    # Show the GUI
    layout.addWidget(download_button)
    layout.addWidget(directory_button)
    main_window.show()
    app.exec_()

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
        run_script(args)
    except KeyboardInterrupt:
        logger.info("Download canceled due to user interruption.")
    except Exception as e:
        logger.error("An error occurred: %s", str(e))

