from collections import Counter
from core.data_manager import load_recipes, load_ingredients

def obtener_ingrediente_mas_usado():
    recetas = load_recipes()
    conteo = Counter()
    for receta in recetas:
        for ing in receta["ingredientes"]:
            conteo[ing["nombre"]] += 1
    return conteo.most_common(1)[0] if conteo else None

def obtener_receta_mas_rentable():
    recetas = load_recipes()
    if not recetas:
        return None
    return max(recetas, key=lambda r: r["precio_sugerido"] - r["costo_total"])

def total_invertido_en_ingredientes():
    ingredientes = load_ingredients()
    return sum(i["precio"] for i in ingredientes)

def precios_de_recetas():
    recetas = load_recipes()
    return [(r["nombre"], r["precio_sugerido"]) for r in recetas]