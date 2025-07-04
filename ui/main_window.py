import tkinter as tk
from ui.ingredients_window import open_ingredients_window
from tkinter import messagebox
from ui.recipes_window import open_recipes_window
from ui.stats_window import open_stats_window

def launch_main_window():
    root = tk.Tk()
    root.title("CalcuChef - Calculadora de Cotizaciones de Recetas")
    root.geometry("400x300")
    root.resizable(False, False)

    title_label = tk.Label(root, text="CalcuChef", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    ingredients_button = tk.Button(root, text="Gestión de Ingredientes", width=30, command=open_ingredients_window)
    ingredients_button.pack(pady=10)

    recipes_button = tk.Button(root, text="Gestión de Recetas", width=30, command=open_recipes_window)
    recipes_button.pack(pady=10)

    stats_button = tk.Button(root, text="Estadísticas", width=30, command=open_stats_window)
    stats_button.pack(pady=10)

    exit_button = tk.Button(root, text="Salir", width=30, command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()