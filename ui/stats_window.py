import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
from matplotlib import pyplot as plt

from core.stats import (
    obtener_ingrediente_mas_usado,
    obtener_receta_mas_rentable,
    total_invertido_en_ingredientes,
    precios_de_recetas
)

def open_stats_window():
    window = ttk.Toplevel()
    window.title("Estadísticas de CalcuChef")
    window.state("zoomed")  # Pantalla completa
    window.resizable(True, True)

    def mostrar_ingrediente_mas_usado():
        dato = obtener_ingrediente_mas_usado()
        if dato:
            Messagebox.ok(title="Ingrediente más usado", message=f"{dato[0]} aparece en {dato[1]} receta(s).")
        else:
            Messagebox.show_warning("Sin datos", "No hay ingredientes registrados.")

    def mostrar_receta_mas_rentable():
        receta = obtener_receta_mas_rentable()
        if receta:
            ganancia = receta["precio_sugerido"] - receta["costo_total"]
            Messagebox.ok(title="Receta más rentable", message=f"{receta['nombre']}\nGanancia: ${ganancia:.2f}")
        else:
            Messagebox.show_warning("Sin datos", "No hay recetas registradas.")

    def mostrar_total_invertido():
        total = total_invertido_en_ingredientes()
        Messagebox.ok(title="Total invertido", message=f"Se ha invertido un total de ${total:.2f} en ingredientes.")

    def graficar_precios():
        datos = precios_de_recetas()
        if not datos:
            Messagebox.show_warning("Sin datos", "No hay recetas para graficar.")
            return

        nombres = [d[0] for d in datos]
        precios = [d[1] for d in datos]

        plt.figure(figsize=(10, 6))  # Tamaño más grande por pantalla completa
        plt.barh(nombres, precios, color="skyblue")
        plt.xlabel("Precio Sugerido")
        plt.title("Precios de recetas")
        plt.tight_layout()
        plt.show()

    ttk.Label(window, text="Estadísticas disponibles", font=("Segoe UI", 20, "bold")).pack(pady=20)

    ttk.Button(window, text="Ingrediente más usado", command=mostrar_ingrediente_mas_usado, bootstyle="primary").pack(pady=10, fill=X, padx=50)
    ttk.Button(window, text="Receta más rentable", command=mostrar_receta_mas_rentable, bootstyle="success").pack(pady=10, fill=X, padx=50)
    ttk.Button(window, text="Total invertido en ingredientes", command=mostrar_total_invertido, bootstyle="info").pack(pady=10, fill=X, padx=50)
    ttk.Button(window, text="Graficar precios de recetas", command=graficar_precios, bootstyle="warning").pack(pady=20, fill=X, padx=50)
