import os
import json
import requests
from typing import Optional, Dict, Any, List

REMOTE_CARDS_URL = "https://raw.githubusercontent.com/yzRobo/gcg-api/main/data/cards.json"

class APIService:
    _cached_cards: Optional[List[Dict[str, Any]]] = None

    @classmethod
    def _fetch_cards_dataset(cls) -> List[Dict[str, Any]]:
        """
        Descarga o lee la base de datos de cartas.
        """
        if cls._cached_cards is not None and len(cls._cached_cards) > 0:
            return cls._cached_cards

        # 1. Intentar descargar desde GitHub
        try:
            response = requests.get(REMOTE_CARDS_URL, timeout=8)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    cls._cached_cards = data
                    print(f"[APIService]: Base de datos remota cargada ({len(cls._cached_cards)} cartas).")
                    return cls._cached_cards
        except Exception as e:
            print(f"[APIService Warning]: No se pudo conectar a GitHub: {e}")

        # 2. Respaldo local
        local_path = os.path.join("data", "cards.json")
        if os.path.exists(local_path):
            try:
                with open(local_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        cls._cached_cards = data
                        print(f"[APIService]: Respaldo local cargado ({len(cls._cached_cards)} cartas).")
                        return cls._cached_cards
            except Exception as e:
                print(f"[APIService Local Error]: {e}")

        cls._cached_cards = []
        return cls._cached_cards

    @staticmethod
    def _build_card_dict(card: Dict[str, Any], default_id: str) -> Dict[str, Any]:
        """
        Mapea las claves específicas del JSON de gcg-api a la estructura interna de la App.
        """
        return {
            "card_id": card.get("card_number") or card.get("product_id") or default_id.upper(),
            "name_en": card.get("name") or "Desconocido",
            "type": card.get("card_type") or card.get("type") or "Unit",
            "cost": card.get("cost") or 0,
            "text_en": card.get("effect") or card.get("description") or "Sin efecto registrado.",
            "image_url": card.get("image_url") or ""
        }

    @classmethod
    def fetch_card_from_api(cls, card_id: str) -> Optional[Dict[str, Any]]:
        """
        Busca la carta comparando el código de forma flexible.
        """
        target_raw = card_id.strip().upper()
        target_clean = target_raw.replace("-", "").replace(" ", "")
        
        cards = cls._fetch_cards_dataset()

        for card in cards:
            possible_keys = [
                str(card.get("card_number", "")),
                str(card.get("product_id", "")),
                str(card.get("id", "")),
                str(card.get("card_code", ""))
            ]

            for raw_code in possible_keys:
                if not raw_code:
                    continue

                c_clean = raw_code.strip().upper().replace("-", "").replace(" ", "")

                if c_clean == target_clean:
                    return cls._build_card_dict(card, card_id)

        return None