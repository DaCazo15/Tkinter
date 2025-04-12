import tkinter as tk

def close_win(widget, tk, event_type):
    widget.bind(event_type, lambda evento: tk.destroy())

