import csv

def export_ingredients_to_csv(ingredients, filename="ingredientes.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre", "Precio por unidad"])
        for ing in ingredients:
            nombre = ing.get("nombre", "N/A")
            precio = ing.get("precio", 0)
            writer.writerow([nombre, precio])

def export_recipes_to_csv(recipes, filename="recetas.csv"):
    with open(filename, mode="w", newline='', encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Nombre de receta", "Ingredientes", "Costo total", "Precio sugerido"])

        for receta in recipes:
            nombre = receta.get("nombre", "Sin nombre")
            ingredientes = receta.get("ingredientes", [])
            costo_total = receta.get("costo_total", 0)
            precio_sugerido = receta.get("precio_sugerido", 0)

            ingredientes_str = ", ".join([
                f"{ing.get('nombre', '???')} ({ing.get('cantidad', 0)})"
                for ing in ingredientes
            ])

            writer.writerow([nombre, ingredientes_str, costo_total, precio_sugerido])
