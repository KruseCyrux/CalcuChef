import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ui.ingredients_window import open_ingredients_window
from ui.recipes_window import open_recipes_window
from ui.stats_window import open_stats_window
from ui.backup_window import open_backup_window  # ← Asegúrate de tener este archivo

def launch_main_window():
    # Tema inicial (claro)
    current_theme = {"name": "flatly"}  # Usamos un dict para que sea mutable
    root = ttk.Window(themename=current_theme["name"])
    root.title("CalcuChef - Calculadora de Cotizaciones de Recetas")
    root.state('zoomed')
    root.resizable(True, True)

    # Barra superior con switch de modo oscuro
    top_bar = ttk.Frame(root, padding=10)
    top_bar.pack(side="top", fill="x")

    ttk.Label(top_bar, text="Modo Oscuro:", bootstyle="inverse").pack(side="left", padx=(0, 5))

    def toggle_theme():
        if current_theme["name"] == "flatly":  # Claro → Oscuro
            root.style.theme_use("darkly")
            current_theme["name"] = "darkly"
        else:  # Oscuro → Claro
            root.style.theme_use("flatly")
            current_theme["name"] = "flatly"

    theme_switch = ttk.Checkbutton(
        top_bar,
        bootstyle="round-toggle",
        command=toggle_theme
    )
    theme_switch.pack(side="left")

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

    # Botón de respaldo de datos
    backup_button = ttk.Button(
        main_frame,
        text="Respaldo de Datos",
        width=40,
        bootstyle="secondary",
        command=open_backup_window
    )
    backup_button.pack(pady=10)

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

    # Botón de salir
    exit_button = ttk.Button(
        main_frame,
        text="Salir",
        width=40,
        bootstyle="danger",
        command=root.quit
    )
    exit_button.pack(pady=20)

    root.mainloop()