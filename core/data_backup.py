import json
import os
from core.data_manager import load_ingredients
from core.data_manager import load_recipes

BACKUP_PATH = "data_backup.json"

def exportar_datos():
    data = {
        "ingredientes": load_ingredients(),
        "recetas": load_recipes()
    }
    with open(BACKUP_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    return BACKUP_PATH

def importar_datos():
    if not os.path.exists(BACKUP_PATH):
        raise FileNotFoundError("No se encontró el archivo de respaldo.")

    with open(BACKUP_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Importar ingredientes
    with open("data/ingredientes.json", "w", encoding="utf-8") as f:
        json.dump(data.get("ingredientes", []), f, indent=4, ensure_ascii=False)

    # Importar recetas
    with open("data/recetas.json", "w", encoding="utf-8") as f:
        json.dump(data.get("recetas", []), f, indent=4, ensure_ascii=False)

    return True
