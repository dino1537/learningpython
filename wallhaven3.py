import os
import requests
import json
import subprocess
import argparse
import logging
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QLabel, QPushButton, QListWidget, QListWidgetItem, QFileDialog, QMessageBox, QWidget, QProgressBar
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QPixmap, QIcon

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
        progress_callback.emit(i, len(selected_images))
    logger.info("Wallpapers downloaded in %s", walldir)

# Create a PyQt5 application for the GUI
app = QApplication([])

# Create a custom signal for updating the progress bar
from PyQt5.QtCore import QObject, pyqtSignal
class ProgressSignal(QObject):
    update_progress = pyqtSignal(int, int)

# Create a custom main window class
class WallpaperDownloaderWindow(QMainWindow):
    def __init__(self, args):
        super().__init__()
        self.args = args
        self.search_results = []  # Initialize an empty list to store search results
        self.progress_signal = ProgressSignal()  # Create a progress signal object
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle("Wallhaven Wallpaper Downloader")
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Create a list widget to display thumbnails
        list_widget = QListWidget()
        layout.addWidget(list_widget)

        # Create a progress bar
        progress_bar = QProgressBar()
        layout.addWidget(progress_bar)

        # Initialize the list widget with search results
        self.update_list_widget(self.args.query)

        # Create a button to trigger the download
        download_button = QPushButton("Download Selected Wallpapers")
        layout.addWidget(download_button)

        # Function to download the selected images
        def download_selected_images():
            selected_items = list_widget.selectedItems()
            selected_images = [item.data(Qt.UserRole) for item in selected_items]
            if not selected_images:
                QMessageBox.warning(self, "No Selection", "Please select wallpapers to download.")
                return
            progress_bar.setValue(0)  # Reset progress bar
            download_wallpapers(selected_images, self.args.walldir, self.progress_signal.update_progress)
            QMessageBox.information(self, "Download Complete", "Wallpapers downloaded successfully.")
        
        download_button.clicked.connect(download_selected_images)

        # Create a button to change the download directory
        def select_directory():
            directory = QFileDialog.getExistingDirectory(self, "Select Download Directory", self.args.walldir)
            if directory:
                self.args.walldir = directory
                logger.info("Download directory set to: %s", self.args.walldir)
        
        directory_button = QPushButton("Select Download Directory")
        layout.addWidget(directory_button)
        directory_button.clicked.connect(select_directory)

    def update_list_widget(self, query):
        list_widget = self.centralWidget().findChild(QListWidget)
        list_widget.clear()
        self.search_results = get_results(query, self.args.max_pages, self.args.sorting, self.args.quality, self.args.atleast)
        for i, item in enumerate(self.search_results):
            thumbnail_url = item["thumbs"][self.args.quality]
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

# Function to run the script
def run_script(args):
    # Create the main window with the GUI elements
    main_window = WallpaperDownloaderWindow(args)

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
