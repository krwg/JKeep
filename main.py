import tkinter as tk
import customtkinter
from gui import RootWindow
from file_manager import db_start

if __name__ == "__main__":
    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    root = RootWindow()
    db_start()
    root.update_notes_list()
    root.mainloop()