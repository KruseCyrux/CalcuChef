import json
import os

DATA_PATH = "data/ingredients.json"

def load_ingredients():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def save_ingredients(ingredients):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(ingredients, f, indent=4, ensure_ascii=False)