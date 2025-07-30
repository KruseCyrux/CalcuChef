import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.ingredients_window import open_ingredients_window
from ui.recipes_window import open_recipes_window
from ui.stats_window import open_stats_window

def launch_main_window():
    root = ttk.Window(themename="flatly") 
    root.title("CalcuChef - Calculadora de Recetas")
    root.geometry("400x300")
    root.resizable(False, False)

    ttk.Label(root, text="CalcuChef", font=("Segoe UI", 24, "bold")).pack(pady=30)

    ttk.Button(root, text="Gestion de Ingredientes", width=30, bootstyle="primary", command=open_ingredients_window).pack(pady=10)
    ttk.Button(root, text="Gestion de Recetas", width=30, bootstyle="success", command=open_recipes_window).pack(pady=10)
    ttk.Button(root, text="Estadisticas", width=30, bootstyle="info", command=open_stats_window).pack(pady=10)
    ttk.Button(root, text="Salir", width=30, bootstyle="danger", command=root.quit).pack(pady=20)

    root.mainloop()