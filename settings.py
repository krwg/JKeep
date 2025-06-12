import tkinter as tk
import customtkinter
from tkinter import messagebox
import requests

CURRENT_VERSION = "1.5.0."
settings_window = None
selected_section = None

def open_settings(root):
    global settings_window, selected_section
    if settings_window is None or not settings_window.winfo_exists():
        settings_window = customtkinter.CTkToplevel(root)
        settings_window.title("Settings")
        settings_window.geometry("800x600")
        settings_window.resizable(False, False)

        left_settings_column = customtkinter.CTkFrame(settings_window, fg_color="#333333")
        left_settings_column.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        right_settings_column = customtkinter.CTkFrame(settings_window, fg_color="#222222")
        right_settings_column.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        settings_sections = {
            "Main": display_main,
            "About the application": display_about
        }

        for i, (section_name, display_func) in enumerate(settings_sections.items()):
            button = customtkinter.CTkButton(left_settings_column, text=section_name,
                                             command=lambda func=display_func, rc=right_settings_column: select_section(func, rc),
                                             fg_color="#333333",
                                             hover_color=("gray80", "gray40"))
            button.grid(row=i, column=0, sticky="ew", pady=5)

        selected_section = display_about
        selected_section(right_settings_column)

        settings_window.columnconfigure(0, weight=1)
        settings_window.columnconfigure(1, weight=3)
        settings_window.protocol("WM_DELETE_WINDOW", close_settings)

def close_settings():
    global settings_window
    settings_window.destroy()
    settings_window = None

def check_for_updates():
    try:
        response = requests.get("https://raw.githubusercontent.com/krwg/JKeep/refs/heads/main/version.txt", timeout=5)
        response.raise_for_status()
        latest_version = response.text.strip()

        if latest_version > CURRENT_VERSION:
            messagebox.showinfo("Updates", f"Upgrade to version available {latest_version}!")
        else:
            messagebox.showinfo("Updates", "You have the latest version.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error checking for updates: {e}. Check your internet connection.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred: {e}")

def select_section(func, right_column):
    global selected_section
    selected_section = func
    clear_right_column(right_column)
    selected_section(right_column)

def clear_right_column(right_column):
    for widget in right_column.winfo_children():
        widget.grid_remove()
        widget.destroy()

def display_about(right_column):
    app_name_label = customtkinter.CTkLabel(right_column, text="JKeep", font=("Arial", 26), text_color="lightgray")
    app_name_label.pack(pady=5)

    app_desc_label = customtkinter.CTkLabel(right_column, text="Quick notes, no fuss.", font=("Arial", 20), text_color="lightgray")
    app_desc_label.pack(pady=2)

    author_label = customtkinter.CTkLabel(right_column, text="krwg. 2025", font=("Arial", 12), text_color="lightgray")
    author_label.pack(pady=5)

    version_label = customtkinter.CTkLabel(right_column, text=f"Version: 1.5.0 Moonstone", font=("Arial", 16))
    version_label.pack(pady=5)

    check_updates_button = customtkinter.CTkButton(right_column, text="Check for updates", command=check_for_updates, fg_color=("gray70", "gray30"), hover_color=("gray80", "gray40"))
    check_updates_button.pack(pady=5)

def display_main(right_column):
    main_label = customtkinter.CTkLabel(right_column, text="In development, expect in the new version", font=("Arial", 16))
    main_label.pack(pady=10)