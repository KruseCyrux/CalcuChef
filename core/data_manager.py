import json
import os

DATA_PATH = "data/ingredients.json"
RECIPES_PATH = "data/recipes.json"

def load_ingredients():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ingredients(ingredients):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, indent=4, ensure_ascii=False)

def load_recipes():
    try:
        with open("data/recetas.json", "r", encoding="utf-8") as f:
            recetas = json.load(f)
            # Asegurar compatibilidad con versiones anteriores
            for r in recetas:
                if "categoria" not in r:
                    r["categoria"] = "Sin categoría"
            return recetas
    except FileNotFoundError:
        return []

def save_recipes(recipes):
    with open(RECIPES_PATH, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=4, ensure_ascii=False)