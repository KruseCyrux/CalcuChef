import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from funciones.estadisticas import obtener_estadisticas

def mostrar_estadisticas():
    ventana = ttk.Toplevel(title="Estadisticas de CalcuChef", themename="flatly")
    ventana.geometry("600x450")

    ttk.Label(ventana, text="Estadisticas Generales", font=("Segoe UI", 18), bootstyle="success").pack(pady=20)

    stats = obtener_estadisticas()

    ttk.Label(ventana, text=f"Receta mas rentable: {stats['receta_mas_rentable']}", bootstyle="info").pack(pady=5)
    ttk.Label(ventana, text=f"Ingrediente mas utilizado: {stats['ingrediente_mas_usado']}", bootstyle="info").pack(pady=5)
    ttk.Label(ventana, text=f"Ganancia media por receta: {stats['ganancia_promedio']:.2f}", bootstyle="info").pack(pady=5)
    ttk.Label(ventana, text=f"Total de recetas: {stats['total_de_recetas']}", bootstyle="info").pack(pady=5)

    ttk.Button(ventana, text="Cerrar", command=ventana.destroy, bootstyle="secondary").pack(pady=30)