import tkinter as tk
from ttkbootstrap import Toplevel, Button
from core.data_backup import exportar_datos, importar_datos
from tkinter import messagebox

def open_backup_window():
    ventana = Toplevel()
    ventana.title("Respaldo de Datos")
    ventana.geometry("300x150")
    ventana.resizable(False, False)

    Button(ventana, text="Exportar respaldo", bootstyle="success", width=25,
           command=lambda: ejecutar_respaldo(exportar_datos)).pack(pady=15)

    Button(ventana, text="Importar respaldo", bootstyle="info", width=25,
           command=lambda: ejecutar_respaldo(importar_datos)).pack(pady=5)

def ejecutar_respaldo(funcion):
    try:
        funcion()
        messagebox.showinfo("Éxito", "Operación completada exitosamente.")
    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
