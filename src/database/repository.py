from database.connection import get_connection

class CardRepository:
    @staticmethod
    def get_card_by_id(card_id: str):
        """Busca una carta localmente por su ID."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM cards WHERE card_id = ?", (card_id.upper(),))
        row = cursor.fetchone()
        conn.close()
        return dict(row) if row else None

    @staticmethod
    def save_card(card_data: dict):
        """Guarda o actualiza la información y traducción de una carta."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO cards (card_id, name_en, type, cost, power, text_en, text_es)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(card_id) DO UPDATE SET
                name_en=excluded.name_en,
                type=excluded.type,
                cost=excluded.cost,
                power=excluded.power,
                text_en=excluded.text_en,
                text_es=excluded.text_es
        """, (
            card_data["card_id"].upper(),
            card_data.get("name_en", ""),
            card_data.get("type", ""),
            card_data.get("cost", ""),
            card_data.get("power", ""),
            card_data.get("text_en", ""),
            card_data.get("text_es", "")
        ))
        conn.commit()
        conn.close()

    @staticmethod
    def add_to_favorites(card_id: str):
        """Añade una carta a la lista de favoritos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT OR IGNORE INTO favorites (card_id) VALUES (?)", (card_id.upper(),))
        conn.commit()
        conn.close()

    @staticmethod
    def remove_from_favorites(card_id: str):
        """Elimina una carta de favoritos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM favorites WHERE card_id = ?", (card_id.upper(),))
        conn.commit()
        conn.close()

    @staticmethod
    def is_favorite(card_id: str) -> bool:
        """Verifica si una carta está en favoritos."""
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1 FROM favorites WHERE card_id = ?", (card_id.upper(),))
        row = cursor.fetchone()
        conn.close()
        return row is not None