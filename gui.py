import tkinter as tk
import customtkinter
from tkinter import messagebox
from PIL import Image, ImageTk
import json
from note import save_note, delete_note_by_id, copy_to_editor, toggle_pinned
from settings import open_settings
from todo import ToDoWindow

font_sizes = {"Heading": 30, "Subheading": 24, "Normal": 20}

def open_todo_window(root):
    todo_window = ToDoWindow(root)
    todo_window.grab_set() 

from file_manager import get_notes

class RootWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("JKeep")
        self.geometry("800x600")
        self.resizable(True, True)
        try:
            self.iconbitmap("icon.ico")
        except tk.TclError:
            print("Icon not found or invalid format.")

        self.header = Header(self)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.left_frame = LeftFrame(self)
        self.left_frame.grid(row=1, column=0, sticky="nsew")

        self.right_frame = RightFrame(self)
        self.right_frame.grid(row=1, column=1, sticky="nsew")

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(1, weight=1)

        self.bind("<F11>", self.toggle_fullscreen)
        self.bind("<Escape>", self.toggle_fullscreen)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.note_container_frame = None

    def toggle_fullscreen(self, event=None):
        self.attributes('-fullscreen', not self.attributes('-fullscreen'))

    def update_notes_list(self):
        if self.note_container_frame:
            self.note_container_frame.destroy()

        self.note_container_frame = customtkinter.CTkFrame(self.left_frame, fg_color="#333333")
        self.note_container_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
        self.note_container_frame.columnconfigure(0, weight=1)
        for i in range(100):
            self.note_container_frame.rowconfigure(i, weight=1)

        notes = get_notes()
        if notes:
            self.left_frame.notes_label.configure(text="")
            self.left_frame.instruction_label.grid_forget()
            for i, (note_id, note_text, pinned, formatted_text) in enumerate(notes):
                self.create_note_container(json.loads(formatted_text), i, note_id, pinned)
        else:
            self.left_frame.notes_label.configure(text="Your notes will go here")
            self.left_frame.instruction_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    def create_note_container(self, formatted_data, row_index, note_id, pinned):
        try:
            container = customtkinter.CTkFrame(self.note_container_frame, fg_color="transparent", corner_radius=5, border_width=2, border_color="#555555")
            container.grid(row=row_index, column=0, sticky="nsew", padx=10, pady=(5, 0))
            container.columnconfigure(0, weight=1)

            try:
                label = customtkinter.CTkLabel(container, text=formatted_data["text"], font=("Arial", font_sizes[formatted_data["font_size"]]), text_color="lightgray", anchor="w", justify="left", wraplength=300)
            except (KeyError, TypeError):
                label = customtkinter.CTkLabel(container, text=formatted_data["text"], font=("Arial", font_sizes["Normal"]), text_color="lightgray", anchor="w", justify="left", wraplength=300)
            label.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
            container.rowconfigure(0, weight=1)

            menu = tk.Menu(label, tearoff=0, bg="#333333", fg="lightgray")
            menu.add_command(label="Delete", command=lambda note_id=note_id: delete_note_by_id(note_id, self))
            menu.add_command(label="Edit", command=lambda note_id=note_id: self.edit_note(note_id))
            if pinned:
                menu.add_command(label="Unpin", command=lambda note_id=note_id: toggle_pinned(note_id, False, self))
            else:
                menu.add_command(label="Pin", command=lambda note_id=note_id: toggle_pinned(note_id, True, self))
            label.bind("<Button-3>", lambda event, menu=menu: menu.post(event.x_root, event.y_root))
            label.bind("<Button-1>", lambda event, note_text=formatted_data["text"], note_id=note_id: copy_to_editor(note_text, note_id, self))

            if pinned:
                container.configure(fg_color="#444444")

            self.add_font_menu(label)
            return container
        except Exception as e:
            messagebox.showerror("Error #3", f"Error creating note container: {e}")

    def edit_note(self, note_id):
        from file_manager import get_note_by_id
        note = get_note_by_id(note_id)
        if note:
            note_text, pinned, formatted_text = note
            formatted_data = json.loads(formatted_text)
            self.right_frame.note_entry.delete("1.0", tk.END)
            self.right_frame.note_entry.insert("1.0", note_text)
            self.right_frame.current_note_id = note_id
            self.right_frame.selected_font_size.set(formatted_data["font_size"])
            self.right_frame.change_note_font_size(formatted_data["font_size"])

    def add_font_menu(self, widget):
        font_menu = tk.Menu(widget, tearoff=0, bg="#333333", fg="lightgray")
        for size_name in font_sizes:
            font_menu.add_command(label=size_name, command=lambda s=size_name: self.change_font_size(widget, s))

        widget.bind("<Button-3>", lambda event, menu=font_menu: menu.post(event.x_root, event.y_root))

    def change_font_size(self, widget, size):
        try:
            widget.configure(font=("Arial", font_sizes[size]))
        except KeyError:
            customtkinter.CTkMessageBox(title="Error #2", message="Incorrect font size.")
        except Exception as e:
            customtkinter.CTkMessageBox(title="Error #1", message=f"Font change error: {e}")

    def on_closing(self):
        from file_manager import close_db
        close_db()
        self.destroy()

class Header(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.header_label = customtkinter.CTkLabel(self, text="JKeep", font=("Arial", 26))
        self.header_label.pack(pady=10, side=tk.LEFT, expand=True, fill="x")

        
        try:
            image = Image.open("settings_icon.png")
            photo = ImageTk.PhotoImage(image)
            self.settings_button = customtkinter.CTkButton(self, text="Settings", image=photo, compound=tk.RIGHT, fg_color=("gray70", "gray30"), hover_color=("gray80", "gray40"), border_width=0, command=lambda: open_settings(master))
            self.settings_button.image = photo
            self.settings_button.pack(side=tk.RIGHT, padx=10, pady=10)
        except FileNotFoundError:
            print("Icon file not found!")
            self.settings_button = customtkinter.CTkButton(self, text="Settings", command=lambda: open_settings(master), fg_color=("gray70", "gray30"), hover_color=("gray80", "gray40"), border_width=0)
            self.settings_button.pack(side=tk.RIGHT, padx=10, pady=10)

      
        self.todo_button = customtkinter.CTkButton(self, text="To Do", command=lambda: open_todo_window(master), fg_color=("gray70", "gray30"), hover_color=("gray80", "gray40"), border_width=0)
        self.todo_button.pack(side=tk.RIGHT, padx=10, pady=10)



class LeftFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#333333")

        self.notes_label = customtkinter.CTkLabel(self, text="Your notes will go here", font=("Arial", 16), text_color="lightgray")
        self.notes_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

        self.instruction_label = customtkinter.CTkLabel(self, text="To create, enter text and Enter", font=("Arial", 12), text_color="#888888")
        self.instruction_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

class RightFrame(customtkinter.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="#222222")

        self.note_label = customtkinter.CTkLabel(self, text="Note:", font=("Arial", 20), text_color="lightgray")
        self.note_label.pack(pady=10, padx=10)

        self.note_entry = customtkinter.CTkTextbox(self, font=("Arial", 12), fg_color="#444444", text_color="lightgray")
        self.note_entry.bind("<Return>", lambda event: save_note(event, master))
        self.note_entry.bind("<Control-Return>", lambda event: self.note_entry.insert(tk.END, "\n"))
        self.note_entry.pack(pady=10, padx=10, fill="both", expand=True)

        self.selected_font_size = tk.StringVar(self, "Normal")
        self.current_note_id = None

        self.font_menu_main = tk.Menu(self.note_entry, tearoff=0, bg="#333333", fg="lightgray")
        for size_name in font_sizes:
            self.font_menu_main.add_command(label=size_name, command=lambda s=size_name: self.change_note_font_size(s))

        self.note_entry.bind("<Button-3>", lambda event, menu=self.font_menu_main: menu.post(event.x_root, event.y_root))

    def change_note_font_size(self, size):
        try:
            self.note_entry.configure(font=("Arial", font_sizes[size]))
            self.selected_font_size.set(size)
        except KeyError:
            customtkinter.CTkMessageBox(title="Error #2", message="Incorrect font size.")
        except Exception as e:
            customtkinter.CTkMessageBox(title="Error #1", message=f"Font change error: {e}")