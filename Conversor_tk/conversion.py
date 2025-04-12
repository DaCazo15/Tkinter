import tkinter as tk 
from tkinter import messagebox, ttk
import string
from wscrap import scrap
from ico import url
from historial import * 

letras = string.ascii_letters
puntos = string.punctuation

root = tk.Tk()
root.title("Conversión")  
root.iconbitmap(url_ico)
root.geometry("300x250")  
root.resizable(False, False)

t, p = scrap()
v = [f"{moneda.ljust(10)}{precio.rjust(15)}" for moneda, precio in zip(t, p)]

if not t:
    messagebox.showerror("Error", "No se pudieron cargar las monedas.")
    root.destroy()

def mostrar_mensaje():
    moneda = entrada.get()  
    cantidad = dinero.get()  
    
    if moneda == "Selecciona una moneda" or moneda == "":
        messagebox.showerror("Error", "Por favor, selecciona una moneda.")
        return
    
    try:
        cantidad = float(cantidad)
    except ValueError:
        messagebox.showerror("Error", f"El monto '{cantidad}' no es válido. Ingresa un número.")
        return
    moneda = moneda.split(" ")[0]
    if moneda.upper() in t:  
        i = t.index(moneda.upper())  
        precio = float(p[i].replace(',', '.'))
        resultado = cantidad / precio 
        mensaje = f"Tenias {resultado:,.2f}$\n\n{moneda.upper()}: {precio}Bs"

        guardar_resultado(mensaje)
        messagebox.showinfo(f"Cantidad en {moneda}", f"Tienes {resultado:,.2f}$\n\n{moneda.upper()}: {precio}Bs")
    else:
        messagebox.showerror("Error", f"La moneda '{moneda}' no está disponible.")

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

#-------------------------------------Confi tk-------------------------------------#
frame = tk.Frame(root, width=250, height=200, bg="#e0e0e0", bd=2.5, relief="sunken")
frame.pack(expand=True, padx=10, pady=10)
frame.pack_propagate(False)

tk.Label(frame, text="Moneda:", bg="#e0e0e0").pack(pady=5)
entrada = ttk.Combobox(frame, values=v, justify="center", state="readonly", width=20)  
entrada.pack(pady=5)
entrada.pack_propagate(False)
entrada.set("Selecciona una moneda")  

tk.Label(frame, text="Dinero:", bg="#e0e0e0").pack(pady=5)
dinero = tk.Entry(frame, justify="center", width=22)
dinero.pack(pady=5)

add_placeholder(dinero, "Ingresa la cantidad")

boton = tk.Button(frame, text="Consultar precio", command=mostrar_mensaje, bg="#0078D7", fg="black")
boton.place (x = 120, y = 140)
histo= tk.Button(frame, text="Historial", command=lambda: historial(root), bg="gray", fg="black")
histo.place (x = 30, y = 140)

root.mainloop()