import tkinter as tk
from tkinter import simpledialog, messagebox
from core.data_manager import load_ingredients, load_recipes, save_recipes
from core.calculator import calcular_costo_total, calcular_precio_sugerido
from core.simulator import simular_produccion
from core.exporter import export_recipes_to_csv

def open_recipes_window():
    window = tk.Toplevel()
    window.title("Gestión de Recetas")
    window.geometry("500x550")

    try:
        ingredients = load_ingredients()
    except Exception as e:
        messagebox.showerror(
            "Error al cargar ingredientes",
            f"No se pudieron cargar los ingredientes.\n\nDetalles: {str(e)}"
        )
        return

    ingredients = load_ingredients()
    recipes = load_recipes()

    recipes_listbox = tk.Listbox(window, width=60)
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

    def view_recipe():
        selection = recipes_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        receta = recipes[index]
        detalles = f"Receta: {receta['nombre']}\n\nIngredientes:\n"
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
            f"🧾 Costo total de producción: ${resultado['costo_total']:.2f}\n"
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

        ingredientes_editados = []
        for ing in receta["ingredientes"]:
            nueva_cantidad = simpledialog.askstring(
                "Editar cantidad",
                f"{ing['nombre']} (actual: {ing['cantidad']}):",
                initialvalue=str(ing["cantidad"])
            )
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

        # Actualizar receta
        recipes[index] = {
            "nombre": nuevo_nombre,
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

    # BOTONES
    tk.Button(window, text="Agregar Receta", width=25, command=add_recipe).pack(pady=4)
    tk.Button(window, text="Ver Detalle", width=25, command=view_recipe).pack(pady=4)
    tk.Button(window, text="Editar Receta", width=25, command=edit_recipe).pack(pady=4)
    tk.Button(window, text="Eliminar Receta", width=25, command=delete_recipe).pack(pady=4)
    tk.Button(window, text="Exportar Recetas a CSV", width=30, command=exportar_recetas).pack(pady=10)
    tk.Button(window, text="Simular Producción", width=30, command=simular_receta).pack(pady=10)

    refresh_list()
