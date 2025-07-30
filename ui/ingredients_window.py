import json
import os
import ttkbootstrap as tkk
from ttkbootstrap.constants import *
from tkinter import simpledialog, messagebox

from utils.data_manager import load_ingredients, save_ingredients
from utils.calculator import calcular_costo_unitario

def open_ingredients_window():
    ingredients = load_ingredients()


    ventana = ttk.Toplevel(title="Gestion de Ingredientes", themename="flatly")
    ventana.geometry("500x400")
    ventana.resizable(False, False)

    ingredients = load_ingredients()

    lista = ttk.Treeview(ventana, columns=("Precio", "Unidad"), show="headings", bootstyle="info")
    lista.heading("Precio", text="Precio")
    lista.heading("Unidad", text="Unidad")
    lista.column("Precio", width=100, anchor="center")
    lista.column("Unidad", width=100, anchor="center")
    lista.pack(pady=10, fill="both", expand="True")


    def refrescar():
        lista.delete(*lista.get_children())
        for ing in ingredientes:
            lista.insert("", "end", text=ing["nombre"],
                         values=(f"${ing['precio']:.2f}", ing["unidad"]))


    def agregar_ingrediente():
                nombre = simpledialog.askstring("Nombre", "Nombre del ingrediente:")
                if not nombre:
                    return
                try:
                    precio = float(simpledialog.askstring("Precio", "Precio del Ingrediente:"))
                    unidad = simpledialog.askstring("Unidad (ej: kg, L, pieza)", "Unidad:")
                    if not unidad:
                        unidad = "unidad"
                except:
                    messagebox.showerror("Error", "Datos invalidos.")
                    return
                
                ingredientes.append({"nombre": nombre, "precio": precio, "unidad": unidad})
                save_ingredients(ingredientes)
                refrescar()


    def eliminar_ingrediente():
                seleccion = lista.selection()
                if not seleccion:
                    messagebox.showwarning("Atencion", "Selecciona un ingrediente para eliminar.")
                    return
                idx = lista.index(seleccion)
                del ingredientes[idx]
                save_ingredients(ingredientes)
                refrescar()


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

     # Botones
            frame_botones = ttk.Frame(ventana)
            frame_botones.pack(pady=10)

            ttk.Button(frame_botones, text="Agregar", bootstyle="success", command=agregar_ingrediente).grid(row=0, column=0, padx=10)
            ttk.Button(frame_botones, text="Eliminar", bootstyle="danger", command=eliminar_ingrediente).grid(row=0, column=1, padx=10)
            ttk.Button(frame_botones, text="Cerrar", bootstyle="secondary", command=ventana.destroy).grid(row=0, column=2, padx=10)

    refrescar()