# CalcuChef 🍽️🧮

**CalcuChef** es una aplicación de escritorio hecha en Python, diseñada para ayudar a restaurantes y cocineros profesionales a calcular el costo total de sus recetas, basándose en precios de ingredientes, cantidades y márgenes de ganancia.

## 🚀 Funcionalidades

- Gestión de ingredientes (agregar, editar, eliminar)
- Creación de recetas con sus respectivos ingredientes y cantidades
- Cálculo de costos por receta y por porción
- Cálculo automático del precio de venta sugerido según margen de ganancia
- Almacenamiento local de datos en archivos JSON
- Interfaz gráfica amigable e intuitiva (Tkinter)

## 📁 Estructura del Proyecto

CalcuChef/
│
├── main.py
├── README.md
├── ui/
├── core/
├── data/
└── assets/

## 🛠️ Tecnologías utilizadas

- Python 3.x
- Tkinter (para la interfaz gráfica)
- Archivos JSON (para guardar datos)

## 📌 Estado del proyecto

🚧 Session 1 - Interfaz principal
- Se creo el archivo 'main.py' como punto de entrada del programa
- Se implemento una ventana principal con 'Tkinder', incluyendo:
    - Boton para ir a la gestion de ingredientes
    - Boton para ir a la gestion de recetas
    - Boton para salir del programa
- Las acciones aun no estan conectadas; se mostraran como ventanas informativas temporales

## 🧩 Sesión 2 – Gestión de Ingredientes

- Se creó la ventana de gestión de ingredientes (ingredients_window.py).
- Se puede agregar, editar y eliminar ingredientes con nombre y precio.
- Los ingredientes se guardan y leen desde un archivo JSON (data/ingredients.json).
- Se agregó conexión desde la ventana principal