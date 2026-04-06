from groq import Groq
import os
import json
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """Eres Ray, un asistente inteligente para controlar Windows.
Interpreta comandos en lenguaje natural y responde SOLO con un JSON sin markdown ni bloques de codigo.

Formato de respuesta obligatorio:
{
  "message": "respuesta amigable en espanol explicando lo que hiciste o por que no puedes hacerlo",
  "action": "nombre_accion o null",
  "params": {}
}

Acciones disponibles:
- open_app: {app_name: string} - Abre una aplicacion por nombre
- close_app: {app_name: string} - Cierra una aplicacion por nombre
- open_url: {url: string} - Abre una URL en el navegador predeterminado
- set_volume: {level: 0-100} - Ajusta el volumen del sistema (0-100)
- mute: {} - Silencia el audio
- unmute: {} - Des-silencia el audio
- shutdown: {delay: number} - Apaga la PC (delay en segundos, default 30)
- restart: {delay: number} - Reinicia la PC (delay en segundos, default 30)
- lock_screen: {} - Bloquea la pantalla
- screenshot: {} - Captura la pantalla y la guarda
- play_pause: {} - Reproduce o pausa la musica/video
- next_track: {} - Siguiente pista
- prev_track: {} - Pista anterior
- minimize_all: {} - Minimiza todas las ventanas (Mostrar escritorio)
- type_text: {text: string} - Escribe texto como si fuera teclado
- press_key: {key: string} - Presiona una tecla especifica
- get_system_info: {} - Obtiene informacion del sistema (CPU, RAM, disco)
- mouse_move: {x: int, y: int} - Mueve el mouse a coordenadas
- mouse_click: {button: "left|right|middle"} - Clic del mouse
- copy: {} - Copiar (Ctrl+C)
- paste: {} - Pegar (Ctrl+V)
- screenshot_base64: {} - Captura pantalla y devuelve en base64

Nombres de apps comunes (mapeo interno):
chrome, edge, firefox, spotify, notepad, notepad++, calculator, explorer, word, excel, powerpoint, vscode, discord, whatsapp, vlc, steam, epic, zoom, teams, slack, filezilla, photoshop, illustrator, premiere

Reglas:
1. Si el usuario pide subir el volumen: usa set_volume con un valor mayor al actual (ej: +20)
2. Si el usuario pide bajar el volumen: usa set_volume con un valor menor
3. Si no entiendes el comando: action = null y explica amablemente
4. Si la accion requiere confirmacion (apagar, reiniciar): incluir advertencia en message
5. Siempre responde en espanol de forma natural y amigable
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
        raw = raw.replace("```json", "").replace("```", "").strip()
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON parse error: {e}")
        print(f"Raw response: {raw}")
        return {
            "message": "Lo siento, no pude entender el comando. Intenta de otra forma.",
            "action": None,
            "params": {}
        }
    except Exception as e:
        print(f"Error interpreting command: {e}")
        return {
            "message": "Hubo un error procesando tu solicitud. Intenta de nuevo.",
            "action": None,
            "params": {}
        }
