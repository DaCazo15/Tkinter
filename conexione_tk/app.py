import tkinter as tk
from tkinter import ttk, messagebox
from wifi_manager import WiFiManager 

class WiFiConnectorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Conector WiFi - Windows")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        self.selected_wifi = tk.StringVar()
        self.password = tk.StringVar()
        
        self.create_widgets()
        self.refresh_wifi_list()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title_label = ttk.Label(main_frame, text="Redes WiFi Disponibles", font=('Arial', 12, 'bold'))
        title_label.pack(pady=5)
        
        wifi_frame = ttk.Frame(main_frame)
        wifi_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(wifi_frame, text="Selecciona una red:").pack(anchor=tk.W)
        self.wifi_combobox = ttk.Combobox(wifi_frame, textvariable=self.selected_wifi, state="readonly")
        self.wifi_combobox.pack(fill=tk.X, pady=5)
        
        password_frame = ttk.Frame(main_frame)
        password_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(password_frame, text="Contraseña:").pack(anchor=tk.W)
        password_entry = ttk.Entry(password_frame, textvariable=self.password, show="*")
        password_entry.pack(fill=tk.X, pady=5)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        refresh_btn = ttk.Button(button_frame, text="Actualizar lista", command=self.refresh_wifi_list)
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
        connect_btn = ttk.Button(button_frame, text="Conectar", command=self.connect_to_wifi)
        connect_btn.pack(side=tk.RIGHT, padx=5)

    def refresh_wifi_list(self):
        try:
            networks = WiFiManager.get_available_networks()
            if not networks:
                messagebox.showwarning("Advertencia", "No se encontraron redes WiFi disponibles.")
            else:
                self.wifi_combobox['values'] = networks
                self.wifi_combobox.set('')
                messagebox.showinfo("Éxito", "Lista de redes WiFi actualizada.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la lista: {str(e)}")

    def connect_to_wifi(self):
        ssid = self.selected_wifi.get()
        password = self.password.get()
        
        if not ssid:
            messagebox.showerror("Error", "Selecciona una red WiFi.")
            return
            
        if not password:
            messagebox.showerror("Error", "Ingresa la contraseña de la red WiFi.")
            return
            
        try:
            WiFiManager.connect_to_network(ssid, password)
            messagebox.showinfo("Éxito", f"Conectado exitosamente a {ssid}!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo conectar a {ssid}:\n{str(e)}")