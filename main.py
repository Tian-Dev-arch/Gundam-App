import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent / "src"))

import flet as ft
from src.database.connection import init_db
from src.services.card_service import CardService
from src.ui.components.card_widget import CardWidget

# Definición de Paleta Gundam TCG
GUNDAM_BLUE = "#0055A5"      # Azul Gundam
GUNDAM_PURPLE = "#7C4DFF"    # Púrpura TCG
GUNDAM_RED = "#E53935"       # Rojo acento
GUNDAM_GREEN = "#00C853"     # Verde resaltados
BG_DARK = "#12131C"          # Fondo de app

def main(page: ft.Page):
    # 1. Inicializar SQLite
    init_db()

    # 2. Configuración general
    page.title = "Gundam TCG Translator"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = BG_DARK
    page.window.width = 400
    page.window.height = 700
    page.padding = 16

    # Cargar fuente temática desde Google Fonts
    page.fonts = {
        "GundamFont": "https://github.com/google/fonts/raw/main/ofl/orbitron/Orbitron%5Bwght%5D.ttf"
    }

    # Componentes principales estilizados
    search_input = ft.TextField(
        label="Código de la carta",
        hint_text="Ej: ST01-001, ST05-010",
        autofocus=True,
        capitalization=ft.TextCapitalization.CHARACTERS,
        border_color=GUNDAM_BLUE,
        focused_border_color=GUNDAM_PURPLE,
        label_style=ft.TextStyle(color="#A0A5C0", font_family="GundamFont"),
        text_style=ft.TextStyle(color="white", font_family="GundamFont"),
        expand=True,
    )

    card_container = ft.Column()
    status_text = ft.Text(
        "", 
        color=GUNDAM_GREEN, 
        font_family="GundamFont", 
        size=12,
        text_align=ft.TextAlign.CENTER,
    )

    def handle_search(e):
        card_id = search_input.value
        if not card_id:
            status_text.value = "Por favor ingresa un código."
            status_text.color = GUNDAM_RED
            page.update()
            return

        status_text.value = "Consultando base de datos..."
        status_text.color = GUNDAM_GREEN
        card_container.controls.clear()
        page.update()

        # Buscar carta a través del servicio
        card_data = CardService.get_card(card_id)

        if card_data:
            status_text.value = ""
            card_widget = CardWidget(card_data)
            card_container.controls.append(card_widget)
        else:
            status_text.value = f"No se encontró la carta '{card_id.upper()}'."
            status_text.color = GUNDAM_RED

        page.update()

    search_btn = ft.ElevatedButton(
        content=ft.Row(
            [
                ft.Icon(ft.Icons.SEARCH, color="white", size=18),
                ft.Text("Buscar", font_family="GundamFont", color="white"),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=4,
        ),
        on_click=handle_search,
        style=ft.ButtonStyle(
            bgcolor=GUNDAM_BLUE,
            shape=ft.RoundedRectangleBorder(radius=8),
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        ),
    )

    # Encabezado con Logo, Título Centrado y Degradado Gundam
    header = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Image(
                            src="/mi_logo.png",  # Tu nuevo ícono en assets
                            width=40,
                            height=40,
                        ),
                        border_radius=8,
                        border=ft.Border.all(1, GUNDAM_PURPLE),
                    ),
                    ft.Text(
                        "GUNDAM TCG",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        font_family="GundamFont",
                        color="white",
                    ),
                    ft.Text(
                        "TRANSLATOR",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        font_family="GundamFont",
                        color=GUNDAM_PURPLE,
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            ft.Text(
                "Traductor de cartas de Gundam TCG",
                size=11,
                color="#8A8D9B",
                font_family="GundamFont",
                text_align=ft.TextAlign.CENTER,
            ),
            ft.Container(
                height=3,
                gradient=ft.LinearGradient(
                    colors=[GUNDAM_BLUE, GUNDAM_PURPLE, GUNDAM_RED]
                ),
                margin=ft.Margin.only(top=8, bottom=12),
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Estructura de la pantalla
    page.add(
        header,
        ft.Row([search_input, search_btn], alignment=ft.MainAxisAlignment.CENTER),
        status_text,
        card_container,
    )

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")