import tkinter as tk
import os



def add_placeholder(entry, placeholder):
    entry.insert(0, placeholder)
    entry.config(fg='grey')
    entry.bind("<FocusIn>", lambda event: clear_placeholder(entry, placeholder))
    entry.bind("<FocusOut>", lambda event: restore_placeholder(entry, placeholder))

def clear_placeholder(entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, tk.END)
        entry.config(fg='black')

def restore_placeholder(entry, placeholder):
    if entry.get() == "":
        entry.insert(0, placeholder)
        entry.config(fg='grey')

def borrar_file():
    if os.path.exists("file.txt") and os.path.exists("state.txt"):
        os.remove("file.txt")
        os.remove("state.txt")

def limpiar(t):
    with open("state.txt", 'r') as file:
        r = [line.strip() for line in file.readlines()]
      
    for widget in t.winfo_children():
        widget.destroy()

def limpiar_entry(entry):
    entry.delete(0, tk.END)
