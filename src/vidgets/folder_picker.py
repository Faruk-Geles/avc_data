# folder_picker.py
import tkinter as tk
from tkinter import filedialog
import sys

def pick_folder():
    root = tk.Tk()
    root.withdraw()           # hide main window
    root.attributes("-topmost", True)  # bring dialog on top
    folder = filedialog.askdirectory()
    root.destroy()
    return folder

if __name__ == "__main__":
    folder = pick_folder()
    # Print the selection to stdout. Streamlit will capture this.
    if folder:
        print(folder)
    # Exit (no folder -> empty stdout)
