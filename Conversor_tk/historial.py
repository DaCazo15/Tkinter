import tkinter as tk
from tkinter import ttk
from ico import url
from dltFile import dlt
import os

url_ico = url()  
historial_window = None 
last_modified_time = None  

def guardar_resultado(mensaje):
    try:
        with open("resultados.txt", "r") as file:
            contenido_existente = file.read()
    except FileNotFoundError:
        contenido_existente = ""
    
    with open("resultados.txt", "w") as file:
        file.write(f"{mensaje}\n")
        file.write("=" * 15 + "\n")
        file.write(contenido_existente)  

def actualizar_historial(text_area):
    try:
        with open("resultados.txt", "r") as file:
            contenido = file.read() 
            text_area.config(state=tk.NORMAL)
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, contenido)  
            text_area.config(state=tk.DISABLED)
    except FileNotFoundError:
        text_area.config(state=tk.NORMAL)
        text_area.delete(1.0, tk.END) 
        text_area.insert(tk.END, "No hay historial disponible.")  
        text_area.config(state=tk.DISABLED)

def actualizar_periodicamente(text_area):
    global last_modified_time
    try:
        current_modified_time = os.path.getmtime("resultados.txt")
        if last_modified_time is None or current_modified_time != last_modified_time:
            last_modified_time = current_modified_time
            actualizar_historial(text_area)  
    except FileNotFoundError:
        if last_modified_time is not None: 
            last_modified_time = None
            actualizar_historial(text_area)

    historial_window.after(1000, lambda: actualizar_periodicamente(text_area)) 

def historial(parent):
    global historial_window
    if historial_window is not None and tk.Toplevel.winfo_exists(historial_window):
        historial_window.focus() 
        return

    historial_window = tk.Toplevel(parent)
    historial_window.geometry(f"500x300+{parent.winfo_x() + parent.winfo_width() + 10}+{parent.winfo_y()}")
    historial_window.title("Historial")
    historial_window.iconbitmap(url_ico)
    historial_window.geometry("500x300")
    historial_window.resizable(False, False)

    frame = ttk.Frame(historial_window, padding="10")
    frame.pack(fill=tk.BOTH, expand=True)

    label = ttk.Label(frame, text="Historial", font=("Arial", 16))
    label.pack(pady=10)

    text_frame = ttk.Frame(frame)
    text_frame.pack(fill=tk.BOTH, padx=5, pady=5)

    text_area = tk.Text(text_frame, wrap=tk.WORD, height=10, state=tk.DISABLED)
    text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    actualizar_historial(text_area) 

    close_button = tk.Button(historial_window, text="Cerrar", command=historial_window.destroy, bg="#00419b", fg="white", width=10)
    close_button.place(x=50, y=20)

    delete_historial = tk.Button(historial_window, text="Borrar historial", command=lambda: dlt(text_area), bg="red", fg="white")
    delete_historial.place(x=340, y=20) 

    actualizar_periodicamente(text_area) 

    historial_window.protocol("WM_DELETE_WINDOW", on_historial_close)  

def on_historial_close():
    global historial_window
    historial_window.destroy() 
    historial_window = None