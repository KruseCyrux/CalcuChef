import tkinter as tk
from tkinter import simpledialog, messagebox
from core.data_manager import load_ingredients, load_recipes, save_recipes
from core.calculator import calcular_costo_total, calcular_precio_sugerido

def open_recipes_window():
    window = tk.Toplevel()
    window.title("Gestión de Recetas")
    window.geometry("500x580")

    ingredients = load_ingredients()
    recipes = load_recipes()

    recipes_listbox = tk.Listbox(window, width=50)
    recipes_listbox.pack(pady=10)

    def refresh_list():
        recipes_listbox.delete(0, tk.END)
        for i, r in enumerate(recipes):
            recipes_listbox.insert(tk.END, f"{i+1}. {r['nombre']} - ${r['costo_total']}")

    def add_recipe():
        nombre = simpledialog.askstring("Nueva Receta", "Nombre de la receta:")
        if not nombre:
            return

        ingredientes_receta = []
        for ing in ingredients:
            cantidad = simpledialog.askstring("Cantidad", f"¿Cuánto de '{ing['nombre']}'?")
            if cantidad:
                try:
                    cantidad = float(cantidad)
                    if cantidad > 0:
                        ingredientes_receta.append({
                            "nombre": ing["nombre"],
                            "precio": ing["precio"],
                            "cantidad": cantidad
                        })
                except ValueError:
                    messagebox.showerror("Error", "Cantidad inválida.")
        if not ingredientes_receta:
            messagebox.showwarning("Advertencia", "No se ingresaron ingredientes.")
            return

        costo_total = calcular_costo_total(ingredientes_receta)
        precio_sugerido = calcular_precio_sugerido(costo_total)

        nueva_receta = {
            "nombre": nombre,
            "ingredientes": ingredientes_receta,
            "costo_total": round(costo_total, 2),
            "precio_sugerido": precio_sugerido
        }
        recipes.append(nueva_receta)
        save_recipes(recipes)
        refresh_list()
        messagebox.showinfo("Éxito", f"Receta guardada.\nCosto: ${costo_total:.2f}\nSugerido: ${precio_sugerido:.2f}")

    def ver_detalle():
        selection = recipes_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        receta = recipes[index]
        detalles = f"Receta: {receta['nombre']}\n\nIngredientes:\n"
        for ing in receta["ingredientes"]:
            detalles += f"- {ing['nombre']}: {ing['cantidad']} x ${ing['precio']} = ${round(ing['cantidad'] * ing['precio'], 2)}\n"
        detalles += f"\nCosto total: ${receta['costo_total']}\nPrecio sugerido: ${receta['precio_sugerido']}"
        messagebox.showinfo("Detalle de Receta", detalles)

    tk.Button(window, text="Agregar Receta", command=add_recipe).pack(pady=5)
    tk.Button(window, text="Ver Detalle", command=ver_detalle).pack(pady=5)

    refresh_list()
