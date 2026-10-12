import flet as ft
from ui.theme import CARD_BG, ACCENT_COLOR, PRIMARY_COLOR, MUTED_TEXT

class CardWidget(ft.Container):
    def __init__(self, card_data: dict, on_favorite_toggle=None):
        self.card_data = card_data
        self.on_favorite_toggle = on_favorite_toggle
        is_fav = self.card_data.get("is_favorite", False)

        super().__init__(
            padding=16,
            bgcolor=CARD_BG,
            border_radius=12,
            border=ft.Border.all(1, PRIMARY_COLOR),
            content=ft.Column(
                spacing=8,
                controls=[
                    # Cabecera: Nombre y Botón de Favorito
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(
                                self.card_data.get("name_en", "Desconocido"),
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                expand=True
                            ),
                            ft.IconButton(
                                icon=ft.Icons.FAVORITE if is_fav else ft.Icons.FAVORITE_BORDER,
                                icon_color=ft.Colors.RED_400 if is_fav else MUTED_TEXT,
                                on_click=self.on_favorite_toggle
                            )
                        ]
                    ),
                    
                    # Ficha técnica (ID, Tipo, Coste)
                    ft.Row(
                        wrap=True,
                        controls=[
                            ft.Chip(label=ft.Text(f"ID: {self.card_data.get('card_id')}")),
                            ft.Chip(label=ft.Text(f"Tipo: {self.card_data.get('type')}")),
                            ft.Chip(label=ft.Text(f"Coste: {self.card_data.get('cost')}")),
                        ]
                    ),
                    ft.Divider(color=ft.Colors.GREY_700),

                    # Texto Original (Inglés)
                    ft.Text("Efecto Original (EN):", size=12, weight=ft.FontWeight.BOLD, color=ACCENT_COLOR),
                    ft.Text(self.card_data.get("text_en", ""), size=13, italic=True, color=MUTED_TEXT),
                    
                    ft.Container(height=8),

                    # Traducción (Español)
                    ft.Text("Traducción (ES):", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_400),
                    ft.Text(self.card_data.get("text_es", ""), size=14, weight=ft.FontWeight.W_500)
                ]
            )
        )