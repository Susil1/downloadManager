"""
    The code is a Python script that uses the Watchdog library to monitor The Download Folder for file
    creation and movement, categorizing files based on their extensions and moving them to appropriate
    destination folders.
    
    :param path: The `path` parameter in the `moveFile` function is the directory path where the file
    will be moved to. It is a string representing the destination directory where the file will be moved
    :type path: str
    :param filename: The `filename` parameter in the code refers to the name of the file that is being
    processed or moved. It is a string that represents the name of the file along with its extension
    :type filename: str
"""
import subprocess
import sys
import importlib

def install(package_name:str):
    try:
        importlib.import_module(package_name)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
install("watchdog")
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent
import time
import logging
import shutil
from pathlib import Path

#Base DIR
BASE_DIR = Path(__file__).resolve().parent

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        logging.FileHandler(r".\watcher.log", mode='w',encoding="utf-8"),
        logging.StreamHandler()
    ]
)

#Global Variables
WAIT_TIME=5
# file_extensions_by_type.py

# 🖼️ Image extensions
images:list[str] = ['.svg', '.png', '.bmp', '.jpg', '.webp', '.tiff', '.ico', '.gif', '.avif', '.jpeg']

# 📄 Document extensions
documents:list[str] = [".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf", ".md", ".epub", ".xls", ".xlsx", ".ppt", ".pptx"]

# 🎥 Video extensions
videos:list[str] = [".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv", ".webm", ".3gp"]

# 🎵 Audio extensions
audios:list[str] = [".mp3", ".wav", ".aac", ".ogg", ".flac", ".wma", ".m4a"]

# 📦 Archive extensions
archives:list[str] = [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz", ".iso"]

# ⚙️ Executable/script extensions
executables = [
    # Windows
    ".exe", ".msi", ".bat", ".cmd",
    # macOS
    ".app", ".dmg", ".pkg",
    # Linux / Unix
    ".sh", ".bin", ".run", ".AppImage", ".deb", ".rpm",
    # Cross-platform / others
    ".apk", ".jar", ".py"
]
#Web Files
# 🌐 Web-related file extensions
web_files: list[str] = [
    # HTML/CSS/JS
    ".html", ".htm", ".css", ".scss", ".sass", ".less", ".js", ".mjs", ".ts", ".tsx",

    # Template files
    ".ejs", ".hbs", ".mustache", ".pug", ".jinja", ".twig",

    # JSON, XML, YAML
    ".json", ".xml", ".yaml", ".yml",

    # Config/manifest files
    ".env", ".ini", ".conf", ".config", ".manifest", ".webmanifest",

    # Web fonts
    ".woff", ".woff2", ".ttf", ".otf", ".eot",

    # Misc
    ".php", ".asp", ".aspx", ".jsp", ".cfm"
]

# 🧪 Miscellaneous/Other extensions
others:list[str] = [".csv", ".db", ".sqlite3", ".log", ]

# ✅ Optional combined dict
all_extensions:dict[str,list[str]] = {
    "images": images,
    "documents": documents,
    "videos": videos,
    "audios": audios,
    "archives": archives,
    "executables": executables,
    "web_files":web_files,
    "others": others
}
WATCH_FOLDER:Path = Path.home() / "Downloads"

def moveFile(path:str,filename:str):
    """
    The function `moveFile` moves a file to a specified destination path, handling cases where a file
    with the same name already exists by appending a counter to the filename.
    
    :param path: The `path` parameter in the `moveFile` function represents the destination folder where
    the file will be moved to
    :type path: str
    :param filename: The `filename` parameter in the `moveFile` function represents the name of the file
    that you want to move to a different location
    :type filename: str
    """
    try:  
        dest_path:str=os.path.join(WATCH_FOLDER,path)
        src_path:str=os.path.join(WATCH_FOLDER,filename)
        os.makedirs(dest_path,exist_ok=True)
        if os.path.exists(os.path.join(dest_path,filename)):
            temp_dest_file=dest_path
            name, ext = os.path.splitext(filename)
            counter = 1
            while True:
                new_filename = f"{name} ({counter}){ext}"
                dest_path = os.path.join(temp_dest_file, new_filename)
                if not os.path.exists(dest_path):
                    break
                counter += 1
            filename = new_filename  # Update for logging
        shutil.move(src_path,dest_path)
        logging.info(f"[Success]File Moved : {os.path.join(path,filename)}")
    except Exception as e:
        logging.error(f"[Error]Error Moving : {filename}\nError: '{str(e)}'")
def moveToDest(filename:str):
    """
    The function `moveToDest` moves a file to a destination folder based on its extension.
    
    :param filename: The `filename` parameter is a string that represents the name of the file that
    needs to be moved to a specific destination based on its extension
    :type filename: str
    :return: The function `moveToDest` is returning either None or the result of the `moveFile`
    function, depending on the conditions met within the function.
    """
    flag:bool=False
    extention:str=os.path.splitext(filename)[-1].lower()
    for folder,extentions in all_extensions.items():
        if (extention in extentions):
            flag=True
            if not extention:
                logging.warning(f"Skipped file without extension: {filename}")
                return
            moveFile(folder.capitalize(),filename)
    if not flag:
        moveFile("others".capitalize(),filename)
# The `downloadManager` class is a Python class that monitors a specified folder for file creation and
# movement events, and moves the files to a destination folder once they are fully downloaded.
class downloadManager(FileSystemEventHandler):
    def __init__(self):
        for event in os.scandir(WATCH_FOLDER):
            if event.is_file():
                moveToDest(event.name)
            
    def wait_and_move(self, filepath:str):
        filename = os.path.basename(filepath)
        if filename.endswith(('.crdownload', '.part',".tmp")):
            logging.info(f"[Skipped Temp File] {filename}")
            return
        # Wait until file is stable (size doesn't change)
        last_size = -1
        while True:
            try:
                current_size = os.path.getsize(filepath)
                if current_size == last_size:
                    break
                last_size = current_size
                time.sleep(WAIT_TIME)
            except FileNotFoundError:
                logging.info(f"[Missing] {filename}")
                return
        moveToDest(filename)
    def on_created(self,event:FileSystemEvent):
        if not event.is_directory:
            logging.info(f"[Created] {event.src_path}")
            self.wait_and_move(str(event.src_path))
    def on_moved(self,event:FileSystemEvent):
        if not event.is_directory:
            logging.info(f"[Created] {event.src_path}")
            self.wait_and_move(str(event.dest_path))

# Run Watchdog
def start_watching():
    event_handler:downloadManager = downloadManager()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_FOLDER))  # recursive=True to watch subfolders
    observer.start()
    logging.info(f"Watching folder: {WATCH_FOLDER}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



if __name__ == "__main__":
    start_watching()