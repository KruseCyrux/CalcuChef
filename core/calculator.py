def calcular_costo_total(ingredientes_receta):
    total = 0
    for item in ingredientes_receta:
        precio = item["precio"]
        cantidad = item["cantidad"]
        total += precio * cantidad
    return total

def calcular_precio_sugerido(costo_total, margen=0.30):
    return round(costo_total * (1 + margen), 2)
