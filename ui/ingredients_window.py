import tkinter as tk
from tkinter import simpledialog, messagebox
from core.data_manager import load_ingredients, save_ingredients

def open_ingredients_window():
    window = tk.Toplevel()
    window.title("Gestión de Ingredientes")
    window.geometry("400x400")

    ingredients = load_ingredients()

    listbox = tk.Listbox(window, width=50)
    listbox.pack(pady=10)

    def refresh_list():
        listbox.delete(0, tk.END)
        for i, ing in enumerate(ingredients):
            listbox.insert(tk.END, f"{i+1}. {ing['nombre']} - ${ing['precio']}/unidad")

    def add_ingredient():
        nombre = simpledialog.askstring("Agregar Ingrediente", "Nombre del ingrediente:")
        if nombre:
            try:
                precio = float(simpledialog.askstring("Agregar Ingrediente", "Precio por unidad:"))
                ingredients.append({"nombre": nombre, "precio": precio})
                save_ingredients(ingredients)
                refresh_list()
            except ValueError:
                messagebox.showerror("Error", "El precio debe ser un número.")

    def delete_ingredient():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona un ingrediente para eliminar.")
            return
        index = selection[0]
        confirm = messagebox.askyesno("Confirmar", f"¿Eliminar '{ingredients[index]['nombre']}'?")
        if confirm:
            ingredients.pop(index)
            save_ingredients(ingredients)
            refresh_list()

    def edit_ingredient():
        selection = listbox.curselection()
        if not selection:
            messagebox.showwarning("Atención", "Selecciona un ingrediente para editar.")
            return
        index = selection[0]
        ing = ingredients[index]
        nuevo_nombre = simpledialog.askstring("Editar", "Nuevo nombre:", initialvalue=ing["nombre"])
        try:
            nuevo_precio = float(simpledialog.askstring("Editar", "Nuevo precio:", initialvalue=ing["precio"]))
            ingredients[index] = {"nombre": nuevo_nombre, "precio": nuevo_precio}
            save_ingredients(ingredients)
            refresh_list()
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")

    tk.Button(window, text="Agregar", width=15, command=add_ingredient).pack(pady=5)
    tk.Button(window, text="Editar", width=15, command=edit_ingredient).pack(pady=5)
    tk.Button(window, text="Eliminar", width=15, command=delete_ingredient).pack(pady=5)

    refresh_list()