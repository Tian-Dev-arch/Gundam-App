import sqlite3
import os

DB_PATH = os.path.join("data", "gundam_tcg.db")

def get_connection():
    """Retorna una conexión a la base de datos SQLite."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Permite acceder a las columnas por nombre de atributo
    return conn

def init_db():
    """Inicializa la estructura de las tablas en la base de datos."""
    os.makedirs("data", exist_ok=True)
    conn = get_connection()
    cursor = conn.cursor()

    # Tabla principal de Cartas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            card_id TEXT PRIMARY KEY,
            name_en TEXT NOT NULL,
            type TEXT,
            cost TEXT,
            power TEXT,
            text_en TEXT,
            text_es TEXT,
            translated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Tabla para Lista de Favoritos / Mazo del Usuario
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS favorites (
            card_id TEXT PRIMARY KEY,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (card_id) REFERENCES cards (card_id)
        )
    """)

    conn.commit()
    conn.close()