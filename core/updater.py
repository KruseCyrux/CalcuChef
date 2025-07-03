from core.data_manager import load_recipes, save_recipes
from core.calculator import calcular_costo_total, calcular_precio_sugerido

def actualizar_precios_recetas(nombre_ingrediente, nuevo_precio):
    recetas = load_recipes()
    recetas_actualizadas = []

    for receta in recetas:
        actualizado = False
        for ing in receta["ingeredientes"]:
            if ing["nombre"] == nombre_ingrediente:
                ing["precio"] = nuevo_precio
                actualizado = True

        if actualizado:
            receta["costo_total"] = round(calcular_costo_total(receta["ingredientes"]), 2)
            receta["precio_sugerido"] = calcular_precio_sugerido(receta["costo_total"])
            recetas_actualizadas.append(receta)

        save_recipes(recetas)
        return len(recetas_actualizadas)            