import tkinter as tk
from tkinter import messagebox
from matplotlib import pyplot as plt

from core.stats import (
    obtener_ingrediente_mas_usado,
    obtener_receta_mas_rentable,
    total_invertido_en_ingredientes,
    precios_de_recetas
)

def open_stats_window():
    window = tk.Toplevel()
    window.title("Estadísticas de CalcuChef")
    window.geometry("400x300")

    def mostrar_ingrediente_mas_usado():
        dato = obtener_ingrediente_mas_usado()
        if dato:
            messagebox.showinfo("Ingrediente más usado", f"{dato[0]} aparece en {dato[1]} receta(s).")
        else:
            messagebox.showwarning("Sin datos", "No hay ingredientes registrados.")

    def mostrar_receta_mas_rentable():
        receta =  obtener_receta_mas_rentable()
        if receta:
            ganancia = receta["precio_sugerido"] - receta["costo_total"]
            messagebox.showinfo("Receta más rentable", f"{receta['nombre']}\nGanancia: ${ganancia:.2f}")
        else:
            messagebox.showwarning("Sin datos", "No hay recetas registradas.")

    def mostrar_total_invertido():
        total = total_invertido_en_ingredientes()
        messagebox.showinfo("Total invertido en ingredientes", f"${total:.2f}")

    def graficar_precios():
        datos = precios_de_recetas()
        if not datos:
            messagebox.showwarning("Sin datos", "No hay recetas para graficar.")
            return
        
        nombres = [d[0] for d in datos]
        precios = [d[1] for d in datos]

        plt.figure(figsize=(8,4))
        plt.barh(nombres, precios, color="skyblue")
        plt.xlabel("Precio Sugerido")
        plt.title("Precios de recetas")
        plt.tight_layout()
        plt.show()

    tk.Button(window, text="Ingrediente más usado", command=mostrar_ingrediente_mas_usado).pack(pady=5)
    tk.Button(window, text="Receta más rentable", command=mostrar_receta_mas_rentable).pack(pady=5)
    tk.Button(window, text="Total invertido en ingredientes", command=mostrar_total_invertido).pack(pady=5)
    tk.Button(window, text="Graficar precios de recetas", command=graficar_precios).pack(pady=10)