from pathlib import Path
import shutil
from datetime import datetime
from file_manager.normalize import normalize

def process_file(file_path: Path, target_folder: Path) -> None:
    """Process a file by moving it to the target folder and renaming it."""
    file_extension = file_path.suffix[1:].lower()
    categories = {
        'images': ['jpeg', 'png', 'jpg', 'svg', 'gif', 'svg'],
        'videos': ['avi', 'mp4', 'mov', 'mkv'],
        'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
        'music': ['mp3', 'ogg', 'wav', 'amr'],
        'archives': ['zip', 'gz', 'tar'],
        'SCRIPTS': ['json','log', 'py', 'pyc', 'js', 'jsx', 'css','html']
    }
    category = None
    for cat, extensions in categories.items():
        if file_extension in extensions:
            category = cat
            break
    if category is None:
        category = 'unknown'

    try:
        # Initialize target_path to avoid NameError
        target_path = target_folder / category / (normalize(file_path.stem) + file_path.suffix)
        counter = 1

        while target_path.exists():
            new_file_name = f"{normalize(file_path.stem)}_{counter}{file_path.suffix}"
            target_path = target_folder / category / new_file_name
            counter += 1

    except shutil.ReadError as e:
        print(f"Error processing archive at '{file_path}': {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing '{file_path}': {e}")
    else:
        try:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(target_path))
        except shutil.Error as e:
            print(f"Error moving file to '{target_path}': {e}")
