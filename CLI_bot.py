import os
from file_manager.norton_commander import display_directory_contents


RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"




class FileManagerBot:
    def run(self):
        try:
            start_path = os.path.expanduser("~")
            display_directory_contents(start_path)
            print(f"{GREEN}Folder was sorted{RESET}")
        except Exception as e:
            # print(f"{RED}Error: '{e}'{RESET}")
            pass