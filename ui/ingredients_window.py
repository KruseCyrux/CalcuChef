import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
from core.data_manager import load_ingredients, save_ingredients
from core.exporter import export_ingredients_to_csv
from core.updater import actualizar_precios_recetas

def open_ingredients_window():
    try:
        ingredientes = load_ingredients()
    except Exception as e:
        messagebox.showerror("Error al cargar ingredientes", f"No se pudieron cargar los ingredientes.\n\nDetalles: {str(e)}")
        return
    
    window = tk.Toplevel()
    window.title("Gestión de Ingredientes")
    window.geometry("400x400")

    ingredientes = load_ingredients()

    lista = ttk.Treeview(
        ventana,
        columns=("Nombre", "Precio", "Cantidad", "Mínimo"),
        show="headings",
        bootstyle="info"
    )
    lista.heading("Nombre", text="Nombre")
    lista.heading("Precio", text="Precio")
    lista.heading("Cantidad", text="Cantidad")
    lista.heading("Mínimo", text="Mínimo")

    lista.column("Nombre", width=300, anchor="w")
    lista.column("Precio", width=100, anchor="center")
    lista.column("Cantidad", width=100, anchor="center")
    lista.column("Mínimo", width=100, anchor="center")
    lista.pack(pady=10, fill="both", expand=True)

    def mostrar_alertas_stock_bajo():
        ingredientes_bajo_stock = [
            ing["nombre"]
            for ing in ingredientes
            if ing.get("cantidad", 0) <= ing.get("umbral", 0)
        ]
        if ingredientes_bajo_stock:
            mensaje = "Los siguientes ingredientes tienen bajo stock:\n\n"
            mensaje += "\n".join(f"• {nombre}" for nombre in ingredientes_bajo_stock)
            messagebox.showwarning("Stock Bajo", mensaje)

    def refrescar():
        lista.delete(*lista.get_children())
        for ing in ingredientes:
            lista.insert("", "end", values=(
                ing["nombre"],
                f"${ing['precio']:.2f}",
                ing.get("cantidad", 0),
                ing.get("umbral", 0)
            ))

    def agregar_ingrediente():
        nombre = simpledialog.askstring("Agregar Ingrediente", "Nombre del ingrediente:")
        if not nombre:
            return
        try:
            precio = float(simpledialog.askstring("Agregar Ingrediente", "Precio por unidad:"))
            cantidad = float(simpledialog.askstring("Agregar Ingrediente", "Cantidad disponible:", initialvalue="0"))
            umbral = float(simpledialog.askstring("Agregar Ingrediente", "Umbral mínimo:", initialvalue="0"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Todos los valores deben ser números válidos.")
            return

        ingredientes.append({
            "nombre": nombre,
            "precio": precio,
            "cantidad": cantidad,
            "umbral": umbral
        })
        save_ingredients(ingredientes)
        refrescar()

    def eliminar_ingrediente():
        seleccion = lista.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un ingrediente para eliminar.")
            return
        idx = lista.index(seleccion[0])
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar '{ingredientes[idx]['nombre']}'?")
        if confirm:
            ingredientes.pop(idx)
            save_ingredients(ingredientes)
            refrescar()

    def editar_ingrediente():
        seleccion = lista.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un ingrediente para editar.")
            return
        idx = lista.index(seleccion[0])
        ing = ingredientes[idx]

        nuevo_nombre = simpledialog.askstring("Editar Ingrediente", "Nombre:", initialvalue=ing["nombre"])
        if not nuevo_nombre:
            return
        try:
            nuevo_precio = float(simpledialog.askstring("Editar Ingrediente", "Precio:", initialvalue=str(ing["precio"])))
            nueva_cantidad = float(simpledialog.askstring("Editar Ingrediente", "Cantidad disponible:", initialvalue=str(ing.get("cantidad", 0))))
            nuevo_umbral = float(simpledialog.askstring("Editar Ingrediente", "Umbral mínimo:", initialvalue=str(ing.get("umbral", 0))))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Todos los valores deben ser números válidos.")
            return

        ingredientes[idx] = {
            "nombre": nuevo_nombre,
            "precio": nuevo_precio,
            "cantidad": nueva_cantidad,
            "umbral": nuevo_umbral
        }
        save_ingredients(ingredientes)
        refrescar()

    def actualizar_precio():
        seleccion = lista.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un ingrediente para actualizar precio.")
            return
        idx = lista.index(seleccion[0])
        ing = ingredientes[idx]

        nuevo_precio = simpledialog.askfloat("Actualizar Precio", f"Ingrese nuevo precio para '{ing['nombre']}' (actual: ${ing['precio']:.2f}):")
        if nuevo_precio is None:
            return

        ingredientes[idx]["precio"] = nuevo_precio
        save_ingredients(ingredientes)

        recetas_afectadas = actualizar_precios_recetas(ing["nombre"], nuevo_precio)
        refrescar()

        # Verificar si está bajo stock después de la actualización
        if ingredientes[idx].get("cantidad", 0) <= ingredientes[idx].get("umbral", 0):
            messagebox.showwarning("Stock Bajo", f"'{ing['nombre']}' tiene bajo stock.")

        messagebox.showinfo(
            "Actualización completada",
            f"Precio de '{ing['nombre']}' actualizado a ${nuevo_precio:.2f}.\n"
            f"{recetas_afectadas} receta(s) afectada(s) y recalculada(s)."
        )

    def exportar_ingredientes():
        export_ingredients_to_csv(ingredientes)
        messagebox.showinfo("Exportación exitosa", "Ingredientes exportados a 'ingredientes.csv'.")

    def reabastecer_ingrediente():
        seleccion = lista.selection()
        if not seleccion:
            messagebox.showwarning("Atención", "Selecciona un ingrediente para reabastecer.")
            return
        idx = lista.index(seleccion[0])
        ing = ingredientes[idx]

        try:
            cantidad_extra = float(simpledialog.askstring("Reabastecer", f"Ingrese cantidad a añadir a '{ing['nombre']}':"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "Debe ingresar un número válido.")
            return

        ingredientes[idx]["cantidad"] = ingredientes[idx].get("cantidad", 0) + cantidad_extra
        save_ingredients(ingredientes)
        refrescar()
        messagebox.showinfo("Reabastecido", f"'{ing['nombre']}' incrementado en {cantidad_extra} unidades.")

    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(pady=10)

    ttk.Button(frame_botones, text="Agregar", bootstyle="success", command=agregar_ingrediente).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Editar", bootstyle="warning", command=editar_ingrediente).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", bootstyle="danger", command=eliminar_ingrediente).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Actualizar Precio", bootstyle="info", command=actualizar_precio).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botones, text="Reabastecer", bootstyle="secondary", command=reabastecer_ingrediente).grid(row=0, column=4, padx=5)
    ttk.Button(frame_botones, text="Exportar a CSV", bootstyle="light", command=exportar_ingredientes).grid(row=0, column=5, padx=5)

    refrescar()
    mostrar_alertas_stock_bajo()
