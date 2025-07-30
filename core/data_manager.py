import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "Data", "ingredients.json")
RECIPES_PATH = os.path.join(BASE_DIR, "..", "Data", "recipes.json")

def load_ingredients():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ingredients(ingredients):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, indent=4, ensure_ascii=False)

def load_recipes():
    if not os.path.exists(RECIPES_PATH):
        return []
    with open(RECIPES_PATH, "r", encoding="utf-8") as f:
        recetas = json.load(f)
        for r in recetas:
            if "categoria" not in r:
                r["categoria"] = "Sin categoría"
        return recetas

def save_recipes(recipes):
    with open(RECIPES_PATH, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=4, ensure_ascii=False)
