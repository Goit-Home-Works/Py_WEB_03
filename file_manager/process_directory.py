"""Обробка каталогу та його підкаталогів."""
from pathlib import Path
from file_manager.process_file import process_file
import logging
from threading import Thread, Semaphore


def folder_content(directory_path: Path) -> list[Path]:
    try:
        directory = list(directory_path.rglob("*"))
        return directory
    except IndexError:
        print("No path to folder")
        return []

def process_directory(folders, path):
    semaphore = Semaphore(2)
    threads = []
    for item in folders:
        thread = Thread(
            name=item,
            target= process_folder,
            args=(item, semaphore, path)
        )
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()
    
    for item in folders:
        if item.is_dir() and not list(item.iterdir()):
            item.rmdir()
    folders = folder_content(path)
    for item in folders:
        if item.is_dir() and not list(item.iterdir()):
            item.rmdir()

def process_folder(item, semaphore, path):
    with semaphore:
        logging.debug("start folder")
        target_folder = path
        for el in item.glob("**/*"):
            process_file(el, target_folder)
        logging.debug("finished to sort folder")

def to_sort(folder_path, sorted_folder_path):
    logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(threadName)s %(levelname)s: %(message)s",
    datefmt="%M:%S"
)

    dirs_to_sort = folder_content(folder_path)
    process_directory(dirs_to_sort, sorted_folder_path)

if __name__ == "__main__":
    
    path = "~/Desktop/мотлох"
    folder_path = Path(path).expanduser()
    sorted_folder_path = Path(path + "/Sorted").expanduser()  # Update with your desired sorted folder path
    to_sort(folder_path, sorted_folder_path)
