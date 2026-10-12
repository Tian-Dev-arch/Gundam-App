from typing import Optional, Dict, Any
from src.database.repository import CardRepository
from src.services.api_service import APIService
from src.services.translator import translate_card_text

class CardService:

    @classmethod
    def get_card(cls, card_id: str) -> Optional[Dict[str, Any]]:
        card_id_clean = card_id.strip().upper()

        # 1. Buscar primero en la Base de Datos SQLite (Offline)
        local_card = CardRepository.get_card_by_id(card_id_clean)
        if local_card:
            print(f"[CardService] Carta {card_id_clean} encontrada en SQLite.")
            return local_card

        # 2. Si no está en SQLite, consultar la API remota real
        print(f"[CardService] Consultando API remota para {card_id_clean}...")
        api_card = APIService.fetch_card_from_api(card_id_clean)

        if not api_card:
            return None

        # 3. Traducir el texto de la carta al español
        text_es = translate_card_text(api_card["text_en"])

        # 4. Estructurar los datos completos
        card_data = {
            "card_id": api_card["card_id"],
            "name_en": api_card["name_en"],
            "type": api_card["type"],
            "cost": api_card["cost"],
            "text_en": api_card["text_en"],
            "text_es": text_es,
            "is_favorite": False
        }

        # 5. Guardar en SQLite para futuras búsquedas rápidas offline
        CardRepository.save_card(card_data)

        return card_data