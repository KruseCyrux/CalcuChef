import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from funciones.recetas import obtener_recetas, eliminar_receta

def mostrar_recetas():
    ventana = ttk.Toplevel(title="Listado de Recetas", themename="flatly")
    ventana.geometry("700x500")

    ttk.Label(ventana, text="Recetas Guardadas", font=("Segoe UI", 18), bootstyle="primary").pack(pady=10)

    listbox = ttk.Listbox(ventana, width=80, heigh=15, bootstyle="info")
    listbox.pack(pady=10)

    recetas = obtener_recetas()
    for receta in recetas:
        listbox.insert("end", f"{receta['nombre']} - ${receta['costo total']} | Sugerido: ${receta['precio_sugerido']}")

    def eliminar():
        seleccion = listbox.curselection()
        if not seleccion:
            messagebox.showwarning("Advertencia", "Selecciona una receta para eliminar.")
            return
        
        index = seleccion[0]
        receta = recetas[index]
        confirmar = messagebox.askyesno("Confirmar", f"¿Eliminar '{receta['nombre']}'?")
        if confirmar:
            eliminar_receta(index)
            listbox.delete(index)
            messagebox.showinfo("Eliminado", "Receta eliminada correctamente.")

    ttk.Button(ventana, text="Eliminar Receta", command=eliminar, bootstyle="danger-outline").pack(pady=10)
    ttk.Button(ventana, text="Cerrar", command=ventana.destroy, bootstyle="secondary").pack(pady=5)