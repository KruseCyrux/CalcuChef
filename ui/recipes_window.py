import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox, ttk
from core.data_manager import load_ingredients, load_recipes, save_recipes
from core.calculator import calcular_costo_total, calcular_precio_sugerido
from core.simulator import simular_produccion
from core.exporter import export_recipes_to_csv

def open_recipes_window():
    window = tk.Toplevel()
    window.title("Gestión de Recetas")
    window.geometry("500x600")
    window.state("zoomed")
    window.resizable(True, True)

    try:
        ingredients = load_ingredients()
        recipes = load_recipes()
    except Exception as e:
        messagebox.showerror("Error al cargar datos", f"Ocurrió un error al cargar los datos:\n{e}")
        window.destroy()
        return

    search_var = tk.StringVar()
    category_var = tk.StringVar()

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
        try:
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
                        else:
                            messagebox.showwarning("Advertencia", "La cantidad debe ser mayor que cero.")
                    except ValueError:
                        messagebox.showerror("Error", f"'{cantidad}' no es una cantidad válida.")

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
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error al agregar la receta:\n{e}")

    def view_recipe():
        try:
            selection = recipes_listbox.curselection()
            if not selection:
                messagebox.showinfo("Aviso", "Selecciona una receta para ver detalles.")
                return
            index = selection[0]
            receta = recipes[index]
            detalles = f"Receta: {receta['nombre']}\nCategoría: {receta.get('categoria', 'Sin categoría')}\n\nIngredientes:\n"
            for ing in receta["ingredientes"]:
                subtotal = round(ing["cantidad"] * ing["precio"], 2)
                detalles += f"- {ing['nombre']}: {ing['cantidad']} x ${ing['precio']} = ${subtotal}\n"
            detalles += f"\nCosto total: ${receta['costo_total']}\nPrecio sugerido: ${receta['precio_sugerido']}"
            messagebox.showinfo("Detalle de Receta", detalles)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo mostrar la receta:\n{e}")

    def simular_receta():
        try:
            selection = recipes_listbox.curselection()
            if not selection:
                messagebox.showwarning("Advertencia", "Selecciona una receta para simular.")
                return
            index = selection[0]
            receta = recipes[index]

            cantidad = simpledialog.askinteger("Simulación", f"¿Cuántas unidades de '{receta['nombre']}' deseas producir?")
            if not cantidad or cantidad <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser mayor a cero.")
                return

            resultado = simular_produccion(receta, cantidad)

            mensaje = (
                f"Simulación para {cantidad} unidad(es) de '{receta['nombre']}':\n\n"
                f"📟 Costo total de producción: ${resultado['costo_total']:.2f}\n"
                f"💰 Precio total sugerido: ${resultado['precio_total']:.2f}\n"
                f"📈 Ganancia estimada: ${resultado['ganancia_total']:.2f}"
            )

            messagebox.showinfo("Resultado de Simulación", mensaje)
        except Exception as e:
            messagebox.showerror("Error en Simulación", f"Ocurrió un error al simular:\n{e}")

    def edit_recipe():
        try:
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
                        else:
                            messagebox.showwarning("Cantidad inválida", "Debe ser mayor a 0.")
                    except ValueError:
                        messagebox.showerror("Error", f"Cantidad inválida para {ing['nombre']}.")

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
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo editar la receta:\n{e}")

    def delete_recipe():
        try:
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
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar la receta:\n{e}")

    def recalcular_costos_recetas():
        try:
            for receta in recipes:
                nuevos_ingredientes = []
                for ing in receta["ingredientes"]:
                    base = next((i for i in ingredients if i["nombre"] == ing["nombre"]), None)
                    if base:
                        nuevos_ingredientes.append({
                            "nombre": ing["nombre"],
                            "precio": base["precio"],
                            "cantidad": ing["cantidad"]
                        })
                receta["ingredientes"] = nuevos_ingredientes
                receta["costo_total"] = round(calcular_costo_total(nuevos_ingredientes), 2)
                receta["precio_sugerido"] = calcular_precio_sugerido(receta["costo_total"])
            save_recipes(recipes)
            refresh_list()
            messagebox.showinfo("Actualizado", "Todos los costos fueron recalculados con los precios actuales.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudieron recalcular los costos:\n{e}")

    def exportar_recetas():
        try:
            export_recipes_to_csv(recipes)
            messagebox.showinfo("Exportación exitosa", "Recetas exportadas a 'recetas.csv'.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo exportar:\n{e}")

    # Botones
    ttk.Button(window, text="Agregar Receta", width=25, command=add_recipe, bootstyle="success-outline").pack(pady=4)
    ttk.Button(window, text="Ver Detalle", width=25, command=view_recipe, bootstyle="secondary").pack(pady=4)
    ttk.Button(window, text="Editar Receta", width=25, command=edit_recipe, bootstyle="warning-outline").pack(pady=4)
    ttk.Button(window, text="Eliminar Receta", width=25, command=delete_recipe, bootstyle="danger-outline").pack(pady=4)
    ttk.Button(window, text="Exportar Recetas a CSV", width=30, command=exportar_recetas, bootstyle="info").pack(pady=10)
    ttk.Button(window, text="Simular Producción", width=30, command=simular_receta, bootstyle="primary").pack(pady=10)
    ttk.Button(window, text="🔄 Recalcular Costos", width=30, command=recalcular_costos_recetas, bootstyle="dark-outline").pack(pady=10)

    refresh_list()