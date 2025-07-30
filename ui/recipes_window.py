import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
from core.data_manager import load_ingredients, load_recipes, save_recipes
from core.calculator import calcular_costo_total, calcular_precio_sugerido
from core.simulator import simular_produccion
from core.exporter import export_recipes_to_csv

def open_recipes_window():
    window = ttk.Toplevel()
    window.title("Gestión de Recetas")
    window.geometry("500x600")
    window.state("zoomed")   # <-- maximizar ventana secundaria
    window.resizable(True, True)

    ingredients = load_ingredients()
    recipes = load_recipes()

    search_var = ttk.StringVar()
    category_var = ttk.StringVar()

    ttk.Label(window, text="Buscar receta por nombre:", bootstyle="primary").pack(pady=(10, 2))
    ttk.Entry(window, textvariable=search_var, width=40).pack()

    ttk.Label(window, text="Filtrar por categoría:", bootstyle="primary").pack(pady=(10, 2))
    ttk.Entry(window, textvariable=category_var, width=40).pack()

    ttk.Button(window, text="Aplicar Filtros", bootstyle="info", command=lambda: refresh_list(search_var.get(), category_var.get())).pack(pady=5)

    recipes_listbox = tk.Listbox(window, width=60, height=10)
    recipes_listbox.pack(pady=10)

    def refresh_list(filtro_nombre="", filtro_categoria=""):
        recipes_listbox.delete(0, "end")
        for i, r in enumerate(recipes):
            if (filtro_nombre.lower() in r["nombre"].lower()) and (filtro_categoria.lower() in r["categoria"].lower()):
                recipes_listbox.insert("end", f"{i+1}. {r['nombre']} - {r['categoria']} - ${r['costo_total']}")

    def add_recipe():
        nombre = simpledialog.askstring("Nueva Receta", "Nombre de la receta:")
        if not nombre:
            return
        categoria = simpledialog.askstring("Categoría", "¿A qué categoría pertenece la receta?") or "Sin categoría"

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
            "categoria": categoria,
            "ingredientes": ingredientes_receta,
            "costo_total": round(costo_total, 2),
            "precio_sugerido": precio_sugerido
        }
        recipes.append(nueva_receta)
        save_recipes(recipes)
        refresh_list()
        messagebox.showinfo("Éxito", f"Receta guardada.\nCosto: ${costo_total:.2f}\nSugerido: ${precio_sugerido:.2f}")

    def view_recipe():
        selection = recipes_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        receta = recipes[index]
        detalles = f"Receta: {receta['nombre']}\nCategoría: {receta.get('categoria', 'Sin categoría')}\n\nIngredientes:\n"
        for ing in receta["ingredientes"]:
            subtotal = round(ing["cantidad"] * ing["precio"], 2)
            detalles += f"- {ing['nombre']}: {ing['cantidad']} x ${ing['precio']} = ${subtotal}\n"
        detalles += f"\nCosto total: ${receta['costo_total']}\nPrecio sugerido: ${receta['precio_sugerido']}"
        messagebox.showinfo("Detalle de Receta", detalles)

    def simular_receta():
        selection = recipes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una receta para simular.")
            return
        index = selection[0]
        receta = recipes[index]

        cantidad = simpledialog.askinteger("Simulación", f"¿Cuántas unidades de '{receta['nombre']}' deseas producir?")
        if not cantidad or cantidad <= 0:
            return

        resultado = simular_produccion(receta, cantidad)

        mensaje = (
            f"Simulación para {cantidad} unidad(es) de '{receta['nombre']}':\n\n"
            f"📟 Costo total de producción: ${resultado['costo_total']:.2f}\n"
            f"💰 Precio total sugerido: ${resultado['precio_total']:.2f}\n"
            f"📈 Ganancia estimada: ${resultado['ganancia_total']:.2f}"
        )

        messagebox.showinfo("Resultado de Simulación", mensaje)

    def edit_recipe():
        selection = recipes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona una receta para editar.")
            return
        index = selection[0]
        receta = recipes[index]

        nuevo_nombre = simpledialog.askstring("Editar nombre", "Nuevo nombre:", initialvalue=receta["nombre"])
        if not nuevo_nombre:
            return

        nueva_categoria = simpledialog.askstring("Editar categoría", "Nueva categoría:", initialvalue=receta.get("categoria", "Sin categoría")) or "Sin categoría"

        ingredientes_editados = []
        for ing in receta["ingredientes"]:
            nueva_cantidad = simpledialog.askstring("Editar cantidad", f"{ing['nombre']} (actual: {ing['cantidad']}):", initialvalue=str(ing["cantidad"]))
            if nueva_cantidad:
                try:
                    cantidad_float = float(nueva_cantidad)
                    if cantidad_float > 0:
                        ingredientes_editados.append({
                            "nombre": ing["nombre"],
                            "precio": ing["precio"],
                            "cantidad": cantidad_float
                        })
                except ValueError:
                    messagebox.showerror("Error", "Cantidad inválida.")

        nuevo_costo = calcular_costo_total(ingredientes_editados)
        nuevo_precio = calcular_precio_sugerido(nuevo_costo)

        recipes[index] = {
            "nombre": nuevo_nombre,
            "categoria": nueva_categoria,
            "ingredientes": ingredientes_editados,
            "costo_total": round(nuevo_costo, 2),
            "precio_sugerido": nuevo_precio
        }

        save_recipes(recipes)
        refresh_list()
        messagebox.showinfo("Éxito", "Receta actualizada.")

    def delete_recipe():
        selection = recipes_listbox.curselection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona una receta para eliminar.")
            return
        index = selection[0]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar receta '{recipes[index]['nombre']}'?")
        if confirm:
            recipes.pop(index)
            save_recipes(recipes)
            refresh_list()

    def exportar_recetas():
        export_recipes_to_csv(recipes)
        messagebox.showinfo("Exportación exitosa", "Recetas exportadas a 'recetas.csv'.")

    ttk.Button(window, text="Agregar Receta", width=25, command=add_recipe, bootstyle="success-outline").pack(pady=4)
    ttk.Button(window, text="Ver Detalle", width=25, command=view_recipe, bootstyle="secondary").pack(pady=4)
    ttk.Button(window, text="Editar Receta", width=25, command=edit_recipe, bootstyle="warning-outline").pack(pady=4)
    ttk.Button(window, text="Eliminar Receta", width=25, command=delete_recipe, bootstyle="danger-outline").pack(pady=4)
    ttk.Button(window, text="Exportar Recetas a CSV", width=30, command=exportar_recetas, bootstyle="info").pack(pady=10)
    ttk.Button(window, text="Simular Producción", width=30, command=simular_receta, bootstyle="primary").pack(pady=10)

    refresh_list()