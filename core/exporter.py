import csv

def export_ingredients_to_csv(ingredients, filename="ingredientes.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Precio por unidad"])
        for ing in ingredients:
            writer.writerow([ing["Nombre"], ing["precio"]])

def export_recipes_to_csv(recipes, filename="recetas.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre de receta", "Ingredientes", "Costo total", "Precio sugerido"])
        for receta in recipes:
            ingredientes_texto = ", ".join(
                [f"{ing['nombre']} ({ing['cantidad']})" for ing in receta["ingredientes"]]
            )
            writer.writerow([receta["nombre"], ingredientes_texto, receta["costo_total"], receta["precio_sugerido"]])