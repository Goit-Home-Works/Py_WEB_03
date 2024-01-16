from file_manager.process_directory import to_sort
import sys
from pathlib import Path
  
folder_path = Path(sys.argv[1]).expanduser()
sorted_folder_path = Path(folder_path / "Sorted").expanduser()  # Update with your desired sorted folder path
to_sort(folder_path, sorted_folder_path)
