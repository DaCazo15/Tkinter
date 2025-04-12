import os
import tkinter as tk

def exist_list() -> bool: return os.path.exists("file.txt")

def dlt_duplicados():
    with open('file.txt', 'r') as archivo:
        lineas = archivo.readlines()

    lineas_unicas = list(dict.fromkeys(lineas))

    with open('file.txt', 'a') as archivo_salida:
        archivo_salida.writelines(lineas_unicas)

def agg_tarea(tarea, estado, list_tarea=None):
    if list_tarea is None:
        list_tarea = []
    if not os.path.exists("state.txt"):
        with open("state.txt", 'w') as file:
            if estado == "0":
                file.write("False" + "\n")
    else:
        with open("state.txt", 'a') as file:
            if estado == "0":
                file.write("False" + "\n")

    list_tarea.append(tarea)
    list_tarea = list(set(list_tarea))
    with open("file.txt", 'a') as file:
        for tarea in list_tarea:
            file.write(tarea + "\n")
        
def estado_tarea(indice_tarea):
    with open("state.txt", 'r') as file:
        list_estado = [line.strip() for line in file.readlines()]  
    if list_estado[indice_tarea] == "False":
        list_estado[indice_tarea] = "True"
    elif list_estado[indice_tarea] == "True":
        list_estado[indice_tarea] = "False"

    with open("state.txt", 'w') as file:
        for nuevo_estado in list_estado:
            file.write(nuevo_estado + "\n")
    
    



def dlt_tarea(tarea, list_tarea=None):
    if list_tarea is None:
        list_tarea = []
    if tarea in list_tarea:
        for tr in list_tarea:
            if tr == tarea:
                
                list_tarea.remove(tarea, "")
        for tr in list_tarea:
            with open("file.txt", 'w') as file:
                file.write(tr)
    else:
        return None

def actualizar(text_area):
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
            actualizar(text_area)  
    except FileNotFoundError:
        if last_modified_time is not None: 
            last_modified_time = None
            actualizar(text_area)