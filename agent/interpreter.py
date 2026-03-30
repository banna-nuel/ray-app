from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """
Eres Ray, asistente de IA para controlar Windows.
Responde ÚNICAMENTE con JSON válido, sin markdown ni texto adicional:
{
  "message": "respuesta al usuario en español",
  "action": "nombre_accion o null",
  "params": {}
}

Acciones disponibles:
- open_app: params: {app_name: string}
- close_app: params: {app_name: string}
- open_url: params: {url: string}
- set_volume: params: {level: 0-100}
- mute: params: {}
- shutdown: params: {delay: 30}
- restart: params: {delay: 30}
- lock_screen: params: {}
- screenshot: params: {}
- play_pause: params: {}
- next_track: params: {}
- prev_track: params: {}
- minimize_all: params: {}
- type_text: params: {text: string}
- press_key: params: {key: string}
- get_system_info: params: {}

Responde siempre en español. Si no hay acción que ejecutar, action es null.
Sé conciso y amigable.
"""


def interpret(text: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=256
        )
        raw = response.choices[0].message.content.strip()
        # Strip markdown if present
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except json.JSONDecodeError:
        return {
            "message": "Entendido, pero no pude procesar la respuesta. Intenta de nuevo.",
            "action": None,
            "params": {}
        }
    except Exception as e:
        return {
            "message": f"Error al interpretar: {str(e)}",
            "action": None,
            "params": {}
        }
