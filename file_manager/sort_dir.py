"""Головний модуль"""
import logging
from pathlib import Path
from file_manager.process_directory import to_sort

def sort_folder(folder) -> None:
    """ Головна функція обробки папки

    Args:
        folder (str): передаем шлях до папки
    """
    logging.basicConfig(
        level = logging.DEBUG,
        format = "{asctime} - {threadName} - {}",
        style  = '{',
    )
    folder_path = Path(folder)
    sorted_folder_path = folder_path
    to_sort(folder_path, sorted_folder_path)
    