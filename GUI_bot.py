
#!/usr/bin/env python3
import os
from tkinter import ttk, StringVar, messagebox, Menu, Tk
from file_manager.sort_dir import sort_folder

GREEN = "\033[92m"
RESET = "\033[0m"

class GUI_bot:
    def __init__(self, root=None):
        if root is None:
            root = Tk()
        self.root = root
        self.root.title("File Explorer")
        self.current_path = StringVar(value=os.getcwd())

        self.create_widgets()

    def create_widgets(self):
        self.path_label = ttk.Label(self.root, textvariable=self.current_path)
        self.path_label.pack(pady=10)
        
        self.sort_button = ttk.Button(self.root, text="Sort",command=self.sort_folder_prompt)
        self.sort_button.pack(side="top",padx=5,pady=5)
        self.exit_button = ttk.Button(self.root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(side="top",padx=5,pady=5)

        self.tree = ttk.Treeview(self.root, columns=("Name", "Type"), show="headings", selectmode="browse")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.pack(expand=True, fill="both")

        self.tree.bind("<Double-1>", self.on_item_double_click)
        self.tree.bind("<Return>", self.on_item_double_click)
        self.tree.bind("<Up>", self.on_arrow_key)
        self.tree.bind("<Down>", self.on_arrow_key)

        self.load_directory_contents()
        self.tree.selection_set(self.tree.get_children()[0])  # Set focus to the first item

        # Full-screen
        self.root.attributes('-zoomed', True)

        # Context menu
        self.context_menu = ContextMenu(self)

    def load_directory_contents(self):
        path = self.current_path.get()
        try:
            entries = [".."] + [entry for entry in os.listdir(path) if not entry.startswith('.')]
        except OSError as e:
            # print(f"Error reading directory {path}: {e}")
            return

        self.tree.delete(*self.tree.get_children())

        for entry in entries:
            entry_path = os.path.join(path, entry)
            is_directory = os.path.isdir(entry_path)
            self.tree.insert("", "end", values=(entry, "Folder" if is_directory else "File"))

    def on_item_double_click(self, event):
        item_id = self.tree.selection()[0]
        item_name = self.tree.item(item_id, "values")[0]

        current_path = self.current_path.get()
        if item_name == "..":
            parent_path = os.path.dirname(current_path)
            self.current_path.set(parent_path)
        else:
            new_path = os.path.join(current_path, item_name)
            if os.path.isdir(new_path):
                self.current_path.set(new_path)

        self.load_directory_contents()

    def on_arrow_key(self, event):
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
        result = messagebox.askquestion("Sort Folder", "Do you want to sort the current folder?")
        if result == "yes":
            current_folder_path = self.current_path.get()
            print(current_folder_path)
            print(type(current_folder_path))
            sort_folder(current_folder_path)
            # self.load_directory_contents()
            
            
    def run_bot(self):
        self.root.mainloop()

class ContextMenu:
    def __init__(self, app):
        self.app = app
        self.menu = Menu(app.root, tearoff=0)
        self.menu.add_command(label="Sort", command=app.sort_folder_prompt)
        self.menu.add_separator()
        self.menu.add_command(label="Exit", command=app.root.destroy)

        app.tree.bind("<Button-3>", self.show_menu)

    def show_menu(self, event):
        self.menu.post(event.x_root, event.y_root)


if __name__ == "__main__":
    app = GUI_bot()
    app.run_bot()
    