import tkinter as tk
import customtkinter

class ToDoWindow(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("To Do List")
        self.geometry("600x400")
        self.resizable(False, False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header_frame = customtkinter.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        self.entry_todo = customtkinter.CTkEntry(self.header_frame, placeholder_text="New task")
        self.entry_todo.pack(side=tk.LEFT, padx=5, fill="x", expand=True)

        self.button_add = customtkinter.CTkButton(self.header_frame, text="Add", command=self.add_todo)
        self.button_add.pack(side=tk.RIGHT, padx=5)

        self.todo_list_frame = customtkinter.CTkScrollableFrame(self)
        self.todo_list_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.todo_items = []  

    def add_todo(self):
        text = self.entry_todo.get().strip()
        if text:
            todo_item = ToDoItem(self.todo_list_frame, text, self.delete_todo_item)
            todo_item.pack(fill="x", padx=5, pady=2)
            self.todo_items.append(todo_item)
            self.entry_todo.delete(0, tk.END)

    def delete_todo_item(self, item):
        item.destroy()
        self.todo_items.remove(item)


class ToDoItem(customtkinter.CTkFrame):
    def __init__(self, master, text, delete_command):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure(1, weight=1)
        self.text = text
        self.delete_command = delete_command

        self.checkbox = customtkinter.CTkCheckBox(self, text="", command=self.toggle_done)
        self.checkbox.grid(row=0, column=0, padx=5)
        self.label = customtkinter.CTkLabel(self, text=text, anchor="w")
        self.label.grid(row=0, column=1, padx=5, sticky="ew")
        self.button_delete = customtkinter.CTkButton(self, text="Delete", width=80, command=self.delete_item)
        self.button_delete.grid(row=0, column=2, padx=5)

        self.done = False

    def toggle_done(self):
        self.done = not self.done
        if self.done:
            self.label.configure(font=("Arial", 14, "overstrike"))
        else:
            self.label.configure(font=("Arial", 14))

    def delete_item(self):
        self.delete_command(self)