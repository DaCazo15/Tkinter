import tkinter as tk
from PIL import Image, ImageTk
from funsiones import *
from tarea import * 
import re
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ancho = 500
alto = 450
imagen_original = Image.open(os.path.join(BASE_DIR, "assets/save.png"))
imagen_redimensionada = imagen_original.resize((40, 40)) 
tooltip = None
#---------------------------------funsiones--------------------------
def mostrar_tooltip(evento, texto):
    global tooltip

    tooltip = tk.Toplevel(root)
    tooltip.wm_overrideredirect(True)  
    tooltip.geometry(f"+{evento.x_root + 10}+{evento.y_root + 10}")  
    label = tk.Label(tooltip, text=texto, background="#c4c5c6", relief="solid", borderwidth=1)
    label.pack()

def ocultar_tooltip(evento):
    global tooltip
    if tooltip:
        tooltip.destroy()

def remove(t): 
    if os.path.exists("file.txt") and os.path.exists("state.txt"): # verifica sin los archivos existen
        with open("file.txt", "r") as file:
            tareas = file.readlines()
        with open("state.txt", "r") as file:
            estados = file.readlines()
        tareas_actualizadas = []
        estados_actualizados = []
        for tarea, estado in zip(tareas, estados): #zip une las listas para iterarlas juntas
            if estado.strip() != "True":  # Mantener solo las tareas no finalizadas
                tareas_actualizadas.append(tarea)
                estados_actualizados.append(estado)
        with open("file.txt", "w") as file:
            file.writelines(tareas_actualizadas)
        with open("state.txt", "w") as file:
            file.writelines(estados_actualizados)
        cargar_tareas(t)
def save(t): # guarda la tarea
    guardar = asignar.get()
    if guardar.strip() == "" or guardar == "Crea una tarea": # verifica el input esta vacio
        if os.path.exists("file.txt"):
            with open("file.txt", "r") as file:
                tareas = file.readlines() 
            if not tareas:
                error_label = tk.Label(t, text="No hay tareas para guardar", font=("Arial", 12), bg="white")
                error_label.place(relx=0.5, rely=0.5, anchor="center")
                return
    if guardar != "" and guardar != "Crea una tarea": # verifica si hay algo en la entrada
        with open("file.txt", "a") as file:
            file.write(guardar + "\n")
        with open("state.txt", "a") as file:
            file.write("False\n")
        print("Tarea guardada:", guardar)  # Depuración
        limpiar(t)
        limpiar_entry(asignar)
        cargar_tareas(t)
    else:
        limpiar(t)
        cargar_tareas(t)
def change_color(label, variable): # cabia color del la tarea
    if variable.get():
        label.config(bg="lightgreen")  # Tarea completada
    else:
        label.config(bg="#ff6c6a")  # Tarea pendiente
def manejar_tarea(e, v, index): # actualiza el estado
    # Leer los estados actuales desde el archivo state.txt
    if os.path.exists("state.txt"):
        with open("state.txt", "r") as file:
            estados = file.readlines()
    else:
        estados = []
    while len(estados) <= index:
        estados.append("False\n")  # Rellenar con "False" si el índice no existe
    estados[index] = "True\n" if v.get() else "False\n"
    with open("state.txt", "w") as file:
        file.writelines(estados)
    change_color(e, v)
def cargar_tareas(frame_tareas): # carga todas las tarea
    for widget in frame_tareas.winfo_children():
        widget.destroy()  # Limpia el frame antes de cargar nuevas tareas
    if not os.path.exists("file.txt"):
        error_label = tk.Label(frame_tareas, text="No se encontraron tareas", font=("Arial", 12), bg="white")
        error_label.place(relx=0.5, rely=0.5, anchor="center")
        return
    if not os.path.exists("state.txt"):
        with open("file.txt", "r") as file:
            tareas = file.readlines()
        with open("state.txt", "w") as file:
            file.writelines(["False\n" for _ in tareas])
    try:
        with open("file.txt", "r") as file:
            tareas = file.readlines()
        print("Tareas cargadas:", tareas)  # Depuración
    except FileNotFoundError:
        tareas = []
    for index, tarea in enumerate(tareas, start=0):
        frame_tarea = tk.Frame(frame_tareas, bg="white")
        frame_tarea.pack(fill="x", padx=5, pady=2)
        with open("state.txt", "r") as file:
            estado = [line.strip() for line in file.readlines()]
        if index < len(estado):
            estado_tarea = estado[index]
        else:
            estado_tarea = "False"
        etiqueta_tarea = tk.Label(
            frame_tarea,
            text=f"{index + 1} - {tarea.strip()}",
            font=("Arial", 12),
            bg="#ff6c6a" if estado_tarea == "False" else "lightgreen",
            anchor="w"
        )
        etiqueta_tarea.pack(side="left", fill="x", expand=True)
        state_var = tk.BooleanVar(value=(estado_tarea == "True"))
        state_checkbutton = tk.Checkbutton(
            frame_tarea,
            onvalue=True,
            offvalue=False,
            bg="white",
            variable=state_var,
            command=lambda e=etiqueta_tarea, v=state_var, i=index: manejar_tarea(e, v, i)
        )
        state_checkbutton.pack(side="right")
#----------------------------------tk ventana ------------------------------
root = tk.Tk()
img_save = ImageTk.PhotoImage(imagen_redimensionada)
root.iconbitmap(os.path.join(BASE_DIR, "assets/list.ico"))
root.title("Lista de tareas")
root.bind("<Escape>", lambda evento: root.destroy())
ancho_pantalla = root.winfo_screenwidth()
alto_pantalla = root.winfo_screenheight()
y = int((alto_pantalla / 2) - (alto / 2) - 25)
x = int((ancho_pantalla / 2) - (ancho /2))
root.geometry(f"{ancho}x{alto}+{x}+{y}")
#----------------------------------tk ventanas----------------------------
titulo = tk.Label(root, text="Listado de tareas", font=("Arial", 15), fg="black")
titulo.pack(pady=15)
asignar = tk.Entry(root, relief="sunken", bg= "white", borderwidth=2, width=50)
asignar.place(x=25, y=70)
add_placeholder(asignar, "Crea una tarea")
asignar.bind("<Return>", lambda evento: save(frame_tareas))
frame_tareas = tk.Frame(root, bg="white", relief="sunken", borderwidth=2, width=450, height=300)
frame_tareas.place(x=25,y=100)
frame_tareas.pack_propagate(False)
cargar_tareas(frame_tareas)
guardar = tk.Label(root, text="Guardar", font=("Arial", 13), fg="black")
guardar.place(x=343,y=66)
save_tareas = tk.Button(
    root,
    image=img_save,
    height=40,
    width=40,
    relief="flat",
    bd=0,command= lambda: save(frame_tareas)
)
save_tareas.place(x=425,y=50)
tooltip_ = None
save_tareas.bind("<Enter>", lambda evento: mostrar_tooltip(evento, "Guardar"))
save_tareas.bind("<Leave>", ocultar_tooltip)
dlt_tareas = tk.Button(
    root,
    text="Borrar tareas",
    bg="white",
    command=lambda: remove(frame_tareas)
)
dlt_tareas.place(x=25, y=400)
root.mainloop()
