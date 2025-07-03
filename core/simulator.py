def simular_produccion(receta, cantidad):
    if cantidad <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")

    costo_total = receta["costo_total"] * cantidad
    precio_total = receta["precio_sugerido"] * cantidad
    ganancia_total = precio_total - costo_total

    return {
        "costo_total": round(costo_total, 2),
        "precio_total": round(precio_total, 2),
        "ganancia_total": round(ganancia_total, 2)
    }
