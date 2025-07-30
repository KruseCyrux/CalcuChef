import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.ingredients_window import open_ingredients_window
from ui.recipes_window import open_recipes_window
from ui.stats_window import open_stats_window

def launch_main_window():
    root = ttk.Window(themename="flatly")
    root.title("CalcuChef - Calculadora de Cotizaciones de Recetas")
    root.state('zoomed')  # Inicia en modo pantalla completa
    root.resizable(True, True)

    # Contenedor principal centrado
    main_frame = ttk.Frame(root, padding=30)
    main_frame.pack(expand=True)

    # Título
    title_label = ttk.Label(
        main_frame,
        text="CalcuChef",
        font=("Arial", 32, "bold"),
        bootstyle="primary"
    )
    title_label.pack(pady=20)

    # Botones principales
    ingredients_button = ttk.Button(
        main_frame,
        text="Gestión de Ingredientes",
        width=40,
        bootstyle="success",
        command=open_ingredients_window
    )
    ingredients_button.pack(pady=10)

    recipes_button = ttk.Button(
        main_frame,
        text="Gestión de Recetas",
        width=40,
        bootstyle="info",
        command=open_recipes_window
    )
    recipes_button.pack(pady=10)

    stats_button = ttk.Button(
        main_frame,
        text="Estadísticas",
        width=40,
        bootstyle="warning",
        command=open_stats_window
    )
    stats_button.pack(pady=10)

    # Botón de salir
    exit_button = ttk.Button(
        main_frame,
        text="Salir",
        width=40,
        bootstyle="danger",
        command=root.quit
    )
    exit_button.pack(pady=20)

    # Botón de alternar pantalla completa
    def toggle_fullscreen():
        is_fullscreen = root.attributes('-fullscreen')
        root.attributes('-fullscreen', not is_fullscreen)

    fullscreen_button = ttk.Button(
        main_frame,
        text="Alternar Pantalla Completa",
        width=40,
        bootstyle="secondary",
        command=toggle_fullscreen
    )
    fullscreen_button.pack(pady=10)

    root.mainloop()

