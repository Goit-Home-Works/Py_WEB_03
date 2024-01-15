#!/usr/bin/env python3
from rich.tree import Tree
from rich import print as rprint
import random

RED = "\033[91m"
GREEN = "\033[92m"
RESET = "\033[0m"


class App_run:
    
    def cli_bot_run():
        pass
    
    def gui_bot_run():
        pass
    
    def good_bye():
        print("Good bye!")
        
    def menu_printing():
        tree = Tree("    =============")
        tree.add(" Menu Options ")
        tree.add("=============")
        options = ["1. GUI application", "2. CLI application", "3. Exit"]
        colors = ["red", "blue", "green", "yellow", "cyan"]
        
        random_color = random.choice(colors)
        random_index = colors.index(random_color)
        for i in range(len(options)):
            tree.add(f"[{colors[(random_index+i)%len(colors)]}] {options[i]}")
            
        rprint(tree)


if __name__ == "__main__":
    while True:
        App_run.menu_printing()
        try:
            action = int(input(f"{GREEN}Choose number of action...{RESET}"))
        except ValueError:
            print("{RED}Invalid input! Please enter a valid number.{RESET}")
            
        if action == 1:
            App_run.gui_bot_run()
        elif action == 2:
            App_run.cli_bot_run()
        elif action == 3:
            App_run.good_bye()
            break
        else:
            continue
