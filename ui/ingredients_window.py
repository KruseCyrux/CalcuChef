import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox
from core.data_manager import load_ingredients, save_ingredients
from core.exporter import export_ingredients_to_csv
from core.updater import actualizar_precios_recetas


def open_ingredients_window():
    ventana = ttk.Toplevel()
    ventana.title("Gestión de Ingredientes")
    ventana.geometry("500x400")
    ventana.state("zoomed")   # maximizar ventana secundaria
    ventana.resizable(True, True)

    ingredientes = load_ingredients()

    # Treeview solo con columnas Nombre y Precio
    lista = ttk.Treeview(ventana, columns=("Nombre", "Precio"), show="headings", bootstyle="info")
    lista.heading("Nombre", text="Nombre")
    lista.heading("Precio", text="Precio")
    lista.column("Nombre", width=300, anchor="w")
    lista.column("Precio", width=150, anchor="center")
    lista.pack(pady=10, fill="both", expand=True)

    def refrescar():
        lista.delete(*lista.get_children())
        for ing in ingredientes:
            lista.insert("", "end", values=(ing["nombre"], f"${ing['precio']:.2f}"))

    def agregar_ingrediente():
        nombre = simpledialog.askstring("Agregar Ingrediente", "Nombre del ingrediente:")
        if not nombre:
            return
        try:
            precio = float(simpledialog.askstring("Agregar Ingrediente", "Precio por unidad:"))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        ingredientes.append({"nombre": nombre, "precio": precio})
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
            nuevo_precio = float(simpledialog.askstring("Editar Ingrediente", "Precio por unidad:", initialvalue=str(ing["precio"])))
        except (TypeError, ValueError):
            messagebox.showerror("Error", "El precio debe ser un número válido.")
            return

        ingredientes[idx] = {"nombre": nuevo_nombre, "precio": nuevo_precio}
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
        messagebox.showinfo(
            "Actualización completada",
            f"Precio de '{ing['nombre']}' actualizado a ${nuevo_precio:.2f}.\n"
            f"{recetas_afectadas} receta(s) afectada(s) y recalculada(s)."
        )

    def exportar_ingredientes():
        export_ingredients_to_csv(ingredientes)
        messagebox.showinfo("Exportación exitosa", "Ingredientes exportados a 'ingredientes.csv'.")

    # Botones en Frame para ordenarlos mejor
    frame_botones = ttk.Frame(ventana)
    frame_botones.pack(pady=10)

    ttk.Button(frame_botones, text="Agregar", bootstyle="success", command=agregar_ingrediente).grid(row=0, column=0, padx=5)
    ttk.Button(frame_botones, text="Editar", bootstyle="warning", command=editar_ingrediente).grid(row=0, column=1, padx=5)
    ttk.Button(frame_botones, text="Eliminar", bootstyle="danger", command=eliminar_ingrediente).grid(row=0, column=2, padx=5)
    ttk.Button(frame_botones, text="Actualizar Precio", bootstyle="info", command=actualizar_precio).grid(row=0, column=3, padx=5)
    ttk.Button(frame_botones, text="Exportar a CSV", bootstyle="secondary", command=exportar_ingredientes).grid(row=0, column=4, padx=5)

    refrescar()
