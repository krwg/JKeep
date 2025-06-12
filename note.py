import tkinter as tk
from tkinter import messagebox
import json
from file_manager import insert_note, update_note

def save_note(event=None, master=None):
    note_entry = master.right_frame.note_entry
    current_note_id = master.right_frame.current_note_id
    selected_font_size = master.right_frame.selected_font_size

    if current_note_id:
        note = note_entry.get("1.0", tk.END).strip()
        if note:
            try:
                font_size = selected_font_size.get()
                formatted_data = {"text": note, "font_size": font_size}
                formatted_text = json.dumps(formatted_data)
                update_note(current_note_id, note, formatted_text)
                master.update_notes_list()
                note_entry.delete("1.0", tk.END)
                selected_font_size.set("Normal")
                master.right_frame.change_note_font_size("Normal")
                master.right_frame.current_note_id = None
            except Exception as e:
                messagebox.showerror("Error", f"Error saving note: {e}")
        else:
            messagebox.showwarning("Warning", "The note is empty!")
    else:
        if event and event.state & 0x0004:
            note_entry.insert(tk.END, "\n")
        else:
            note = note_entry.get("1.0", tk.END).strip()
            if note:
                try:
                    font_size = selected_font_size.get()
                    formatted_data = {"text": note, "font_size": font_size}
                    formatted_text = json.dumps(formatted_data)
                    insert_note(note, formatted_text)
                    master.update_notes_list()
                    note_entry.delete("1.0", tk.END)
                    selected_font_size.set("Normal")
                    master.right_frame.change_note_font_size("Normal")
                except Exception as e:
                    messagebox.showerror("Error", f"Error saving note: {e}")
            else:
                messagebox.showwarning("Warning", "The note is empty!")

def delete_note_by_id(note_id, master):
    from file_manager import delete_note
    delete_note(note_id)
    master.update_notes_list()

def copy_to_editor(note_text, note_id, master):
    note_entry = master.right_frame.note_entry
    note_entry.delete("1.0", tk.END)
    note_entry.insert("1.0", note_text)
    master.right_frame.current_note_id = note_id

def toggle_pinned(note_id, pinned, master):
    from file_manager import update_pinned
    update_pinned(note_id, pinned)
    master.update_notes_list()