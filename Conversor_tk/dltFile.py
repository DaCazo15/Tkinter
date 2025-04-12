import os
import tkinter as tk

def dlt(text_area):
    current_directory = os.getcwd()
    txt_files = [file for file in os.listdir(current_directory) if file.endswith('.txt')]
    if txt_files:
        archivo = txt_files[0]
        os.remove(archivo)
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "No hay historial disponible.")
        text_area.config(state=tk.DISABLED)