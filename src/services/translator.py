import os
import time
from groq import Groq

# Tu clave de API de Groq
GROQ_API_KEY = "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"

client = Groq(
    api_key=GROQ_API_KEY,
    timeout=15.0
)

SYSTEM_PROMPT = """
Eres un traductor experto en cartas de juegos TCG (Trading Card Games), específicamente de Gundam TCG.
Tu tarea es traducir el texto de las cartas del inglés al español aplicando strictly estas reglas:

REGLAS DE TÉRMINOS CLAVE:
1. MANTÉN EN INGLÉS SIN MODIFICAR: Deployed, Unit, Pilot, Base, Blocker, AP, HP, Tap, Untap, Hand, Deck, Trash, Burst, Damage, Repair.
2. Formato de disparadores: Traduce "When Deployed:" como "[When Deployed]:" o "[Deployed]:".
3. Usa lenguaje imperativo y claro para los efectos del juego ("Roba 1 carta", "Otorga", etc.).
4. Devuelve ÚNICAMENTE la traducción al español sin comentarios adicionales.
"""

def translate_card_text(text_en: str) -> str | None:
    if not text_en or text_en.strip() == "" or text_en == "Sin efecto registrado.":
        return text_en

    # Usamos el modelo Qwen disponible en tu desplegable
    model_name = "qwen/qwen3.8-27b"

    for attempt in range(3):
        try:
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": f"Traduce el siguiente efecto de carta al español:\n\n{text_en}"}
                ],
                temperature=0.2,
                max_tokens=300
            )

            if completion.choices and completion.choices[0].message.content:
                return completion.choices[0].message.content.strip()

        except Exception as e:
            error_msg = str(e)
            print(f"[Translator Warning - Intento {attempt+1}]: {error_msg}")
            if "429" in error_msg or "rate_limit" in error_msg.lower():
                time.sleep(2)
            else:
                break

    print("[Translator Error]: No se pudo traducir la carta mediante Groq.")
    return None