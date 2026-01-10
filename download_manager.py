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
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import FileSystemEvent
import time
import logging
import shutil
from pathlib import Path

from utils.FILE_EXT import all_extensions


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

#Base DIR
BASE_DIR = Path(__file__).resolve().parent
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
        dest_path:Path=WATCH_FOLDER/path
        src_path:Path = WATCH_FOLDER/filename
        dest_path.mkdir(exist_ok=True)
        if (dest_path/filename).exists():
            temp_dest_file=dest_path
            temp_file = Path(filename)
            name, ext = temp_file.stem,temp_file.suffix
            if (name.startswith(".") and not ext.strip()):
                filename = "no_name" + ext
                temp_file = Path(filename)
                name, ext = temp_file.stem,temp_file.suffix
            counter = 1
            while True:
                new_filename = f"{name} ({counter}){ext}"
                dest_path = temp_dest_file/new_filename
                if not (dest_path.exists()):
                    break
                counter += 1
            filename = new_filename  # Update for logging
        shutil.move(src_path,dest_path)
        logging.info(f"[Success]File Moved : {(Path(path)/filename).as_posix()}")
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
    extension:str=os.path.splitext(filename)[-1].lower()
    for folder,extensions in all_extensions.items():
        if (extension in ('.crdownload', '.part',".tmp",".winmd")):
            flag = True
            break
        if (extension in extensions):
            flag=True
            if not extension:
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
            
    def wait_and_move(self, filepath:Path):
        filename = filepath.name
        if filename.endswith(('.crdownload', '.part',".tmp",".winmd")):
            logging.info(f"[Skipped Temp File] {filename}")
            return
        # Wait until file is stable (size doesn't change)
        last_size = -1
        while True:
            try:
                current_size = filepath.stat().st_size
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
            self.wait_and_move(Path(str(event.src_path)))
    def on_moved(self,event:FileSystemEvent):
        if not event.is_directory:
            logging.info(f"[Created] {event.src_path}")
            self.wait_and_move(Path(str(event.dest_path)))

# Run Watchdog
def start_watching():
    logging.info(f"Watching folder: {WATCH_FOLDER}")
    event_handler:downloadManager = downloadManager()
    observer = Observer()
    observer.schedule(event_handler, str(WATCH_FOLDER))  # recursive=True to watch subfolder
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



if __name__ == "__main__":
    start_watching()