import tkinter as tk
from tkinter import messagebox

def launch_main_window():
    root = tk.Tk()
    root.title("CalcuChef - Calculadora de Cotizaciones de Recetas")
    root.geometry("400x300")
    root.resizable(False, False)

    title_label = tk.Label(root, text="CalcuChef", font=("Arial", 24, "bold"))
    title_label.pack(pady=20)

    ingredients_button = tk.Button(root, text="Gestión de Ingredientes", width=30, command=lambda: messagebox.showinfo("Ingredientes", "Abrir módulo de ingredientes (próxima sesión)"))
    ingredients_button.pack(pady=10)

    recipes_button = tk.Button(root, text="Gestión de Recetas", width=30, command=lambda: messagebox.showinfo("Recetas", "Abrir módulo de recetas (próxima sesión)"))
    recipes_button.pack(pady=10)

    exit_button = tk.Button(root, text="Salir", width=30, command=root.quit)
    exit_button.pack(pady=10)

    root.mainloop()