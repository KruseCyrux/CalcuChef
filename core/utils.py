import json

INGREDIENTS_PATH = "data/ingredients.json"
RECIPES_PATH = "data/recipes.json"

def load_ingredients():
    try:
        with open(INGREDIENTS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def load_recipes():
    try:
        with open(RECIPES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_recipes(recipes):
    with open(RECIPES_PATH, "w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=4, ensure_ascii=False)

def get_price(ingredient_name, ingredients_data):
    for ing in ingredients_data:
        if ing["nombre"].lower() == ingredient_name.lower():
            return ing.get("precio", 0.0)
    return 0.0

def recalculate_all_recipes():
    ingredients = load_ingredients()
    recipes = load_recipes()

    for recipe in recipes:
        total_cost = 0
        for ing in recipe.get("ingredientes", []):
            nombre = ing.get("nombre")
            cantidad = ing.get("cantidad", 0)
            precio_unitario = get_price(nombre, ingredients)
            total_cost += precio_unitario * cantidad
        recipe["costo_total"] = round(total_cost, 2)
    save_recipes(recipes)
    print("✔ Todos los precios de recetas han sido recalculados.")
