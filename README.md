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

```
CalcuChef/
│
├── main.py
├── README.md
├── ui/
├── core/
├── data/
└── assets/
```

## 🛠️ Tecnologías utilizadas

- Python 3.x
- Tkinter (para la interfaz gráfica)
- Archivos JSON (para guardar datos)

## 📌 Estado del proyecto

## 🚧 Sesión 1 - Interfaz principal

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
- Se agregó conexión desde la ventana principal

## 🛠️ Sesión 3 – Gestión de Recetas

- Se creó la ventana para crear y ver recetas.
- Al crear una receta, se pueden seleccionar ingredientes y cantidades.
- Se calcula automáticamente el costo total y un precio sugerido de venta.
- Las recetas se almacenan en el archivo `recipes.json`.
- Se agregó el módulo `calculator.py` para manejar los cálculos.

## 🧩 Sesión 4 – Edición y Eliminación de Recetas

- Se agregó la posibilidad de editar recetas guardadas:
  - Cambiar nombre.
  - Modificar cantidades de ingredientes.
  - Recalcular automáticamente costo total y precio sugerido.
- Se implementó la función de eliminar recetas con confirmación.
- La interfaz de recetas ahora es más completa y funcional.

## 🧩 Sesión 5 – Exportacion a CSV

- Se agrego funcionalidad para exportar datos a archivos `.csv`.
- Desde cada ventana (ingredientes y recetas), se puede generar un archivo compatible con Excel o Google Sheets.
- El archivo `exporter.py` centraliza la logica de exportacion.

## 🧩 Sesion 6 - Actualizacion de precios

- Se añadio la opcion de actualizar el precio de un ingrediente desde la interfaz.
- Al cambiar el precio, todas las recetas que contiene dicho ingrediente se actualizan automaticamente:
- Se recalcula su costo total.
- Se ajusta el precio sugerido.
- Se creo el archivo 'updater.py' para manejar estas operaciones de forma centralizada

## 🛠️ Sesión 7 – Simulación de Producción y Ganancias

- Se agregó una función que permite simular la producción de múltiples unidades de una receta.
- El usuario puede ver:
  - Costo total de producción
  - Precio total sugerido
  - Ganancia estimada
- Se creó el archivo `simulator.py` para manejar esta lógica.

## 📊 Sesión 8 – Estadísticas visuales

- Se creó una nueva ventana que muestra datos clave:
  - Ingrediente más usado en recetas
  - Receta más rentable
  - Total invertido en ingredientes
  - Gráfica de precios sugeridos por receta
- Se agregó el archivo `stats.py` para manejar estadísticas.

## 🔍 Sesión 9 – Búsqueda y Categorías

- Se añadió funcionalidad de búsqueda por nombre de receta.
- Se permite filtrar recetas por categoría.
- Al agregar o editar recetas, ahora se incluye una categoría personalizada.
- La categoría se muestra en la vista de detalles y lista general.

## 🧩 Sesión Extra A - Mejora visual con ttkbootstrap

- Se reemplazó el uso tradicional de tkinter y ttk por ttkbootstrap.
- Se integró un tema moderno y profesional: "superhero" (puede cambiarse fácilmente por otro).
- Se mejoraron todos los botones, etiquetas y cuadros de texto para usar estilos visuales de ttkbootstrap.
- Se aplicaron colores, padding y espaciado inteligente para una mejor distribución visual.
- Se agregaron mensajes más claros, encabezados estilizados y controles visuales mejorados.

## 📘 Sesión Extra B - Inventario De Insumos
`ui/recipes_window.py`
- Se rediseñó la interfaz de la ventana de recetas:
- Se agregó una barra de búsqueda por nombre usando tk.StringVar().
- Se conectó dicha barra a un evento <KeyRelease> para actualizar en tiempo real el listado mostrado.
- Se incorporó un Treeview para mostrar las recetas de forma más clara y estructurada.
- Se eliminó la lista sin formato previa para reemplazarla por la tabla dinámica.
- Se mejoró la experiencia visual con ttkbootstrap.