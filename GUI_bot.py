
#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
from file_manager.sort_dir import sort_folder

GREEN = "\033[92m"
RESET = "\033[0m"


class FileExplorerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
        self.current_path = os.path.abspath(path)

        self.create_widgets()

    def create_widgets(self):
        # Create label to display current folder path
        self.path_label_text = tk.StringVar(value=f"current folder - {self.current_path}")
        self.path_label = ttk.Label(self.root, textvariable=self.path_label_text)
        self.path_label.pack(pady=10)

        # Create Sort and Exit buttons side by side on the top
        self.sort_button = ttk.Button(self.root, text="Sort", command=self.sort_folder_prompt)
        self.sort_button.pack(side="top", padx=5, pady=5)
        self.exit_button = ttk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(side="top", padx=5, pady=5)

        # Create Treeview to display directory contents
        self.tree = ttk.Treeview(self.root, columns=("Name", "Type"), show="headings", selectmode="browse")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.pack(expand=True, fill="both")

        # Bind events for double-click, Enter key, and arrow keys
        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.tree.bind("<Return>", self.on_item_double_click)
        self.tree.bind("<Up>", self.on_arrow_key)
        self.tree.bind("<Down>", self.on_arrow_key)

        # Load directory contents and set focus to the first item
        self.load_directory_contents()
        self.tree.selection_set(self.tree.get_children()[0])

        # Enable full-screen mode and bind Escape key for exiting full-screen
        self.root.attributes('-zoomed', True)

        # Create ContextMenu instance
        self.context_menu = ContextMenu(self)

    def load_directory_contents(self):
        # Load directory contents and update Treeview
        path = self.current_path
        try:
            entries = [".."] + [entry for entry in os.listdir(path) if not entry.startswith('.')]
        except OSError as e:
            print(f"Error reading directory {path}: {e}")
            return

        self.tree.delete(*self.tree.get_children())

        for entry in entries:
            entry_path = os.path.join(path, entry)
            is_directory = os.path.isdir(entry_path)
            self.tree.insert("", "end", values=(entry, "Folder" if is_directory else "File"))

    def on_item_double_click(self, event):
        # Handle double-click on Treeview item
        item_id = self.tree.selection()[0]
        item_name = self.tree.item(item_id, "values")[0]

        current_path = self.current_path
        if item_name == "..":
            parent_path = os.path.dirname(current_path)
            self.current_path = parent_path
        else:
            new_path = os.path.join(current_path, item_name)
            if os.path.isdir(new_path):
                self.current_path = new_path

        self.load_directory_contents()

    def on_arrow_key(self, event):
        # Handle arrow key events for Treeview
        selected_item = self.tree.selection()
        if selected_item:
            if event.keysym == "Up":
                prev_item = self.tree.prev(selected_item)
                if prev_item:
                    self.tree.selection_set(prev_item)
            elif event.keysym == "Down":
                next_item = self.tree.next(selected_item)
                if next_item:
                    self.tree.selection_set(next_item)

    def sort_folder_prompt(self):
        # Display a prompt to confirm sorting
        result = tkinter.messagebox.askquestion("Sort Folder", "Do you want to sort the current folder?")
        if result == "yes":
            sort_folder(self.current_path)
    
    def run_bot():
        root = tk.Tk()
        app = FileExplorerApp(root)
        root.mainloop()


class ContextMenu:
    def __init__(self, app):
        # Create a context menu with options Sort and Exit
        self.app = app
        self.menu = tk.Menu(app.root, tearoff=0)
        self.menu.add_command(label="Sort", command=app.sort_folder_prompt)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=app.root.destroy)

        # Bind the right mouse button to show the context menu
        app.tree.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        # Display the context menu at the location of the right mouse click
        self.menu.post(event.x_root, event.y_root)


if __name__ == "__main__":
    FileExplorerApp.run_bot()