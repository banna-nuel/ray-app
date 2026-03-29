import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Global Configuration Path (Windows standard)
CONFIG_PATH = r"C:\RayApp"
ENV_PATH = os.path.join(CONFIG_PATH, ".env")

# Fallback for local dev
if not os.path.exists(CONFIG_PATH):
    ENV_PATH = os.path.join(os.path.dirname(__file__), '..', '.env')

SYSTEM_PROMPT = """
Eres Ray, un asistente de IA inteligente para controlar Windows remotamente.
Eres directo, amigable y eficiente. Responde siempre en español.

SIEMPRE responde SOLO con este JSON (sin markdown, sin texto extra):
{
  "message": "<tu respuesta conversacional>",
  "skill": "<NombreSkill o null>",
  "params": {}
}

Skills disponibles:
- SetVolume: { "level": 0-100 } — establecer volumen exacto
- GetVolume: {} — obtener volumen actual
- Mute: {} — silenciar audio
- Unmute: {} — activar audio
- Shutdown: { "delay": 30 } — apagar PC (delay en segundos)
- Restart: { "delay": 30 } — reiniciar PC (delay en segundos)
- CancelShutdown: {} — cancelar apagado programado
- LockScreen: {} — bloquear pantalla
- Screenshot: {} — captura de pantalla
- GetSystemInfo: {} — info de CPU, RAM, disco
- OpenURL: { "url": "string", "browser": "edge" } — abrir URL
- NewTab: { "url": "string" } — nueva pestaña
- GoogleSearch: { "query": "string" } — buscar en Google
- YouTubeSearch: { "query": "string" } — buscar en YouTube
- PlayPause: {} — pausar/reanudar música
- NextTrack: {} — siguiente canción
- PrevTrack: {} — canción anterior
- VolumeUp: { "steps": 1 } — subir volumen
- VolumeDown: { "steps": 1 } — bajar volumen
- OpenApp: { "app_name": "string" } — abrir aplicación
- CloseApp: { "app_name": "string" } — cerrar aplicación
- MinimizeAll: {} — minimizar todo (escritorio)
- MaximizeWindow: { "app_name": "string" } — maximizar ventana
- SwitchWindow: {} — cambiar ventana (Alt+Tab)

Ejemplos:
"sube el volumen a 50" → {"message": "Poniendo volumen al 50%", "skill": "SetVolume", "params": {"level": 50}}
"abre spotify" → {"message": "Abriendo Spotify 🎵", "skill": "OpenApp", "params": {"app_name": "spotify"}}
"apaga el pc en 5 minutos" → {"message": "PC se apagará en 5 minutos", "skill": "Shutdown", "params": {"delay": 300}}
"busca gatitos en youtube" → {"message": "Buscando gatitos en YouTube 🐱", "skill": "YouTubeSearch", "params": {"query": "gatitos"}}
"hola" → {"message": "¡Hola! ¿En qué te ayudo hoy?", "skill": null, "params": {}}
"cómo estás" → {"message": "¡Funcionando al 100%! ¿Quieres que haga algo por ti?", "skill": null, "params": {}}

Si el usuario no pide una acción concreta, "skill" debe ser null.
NUNCA inventes skills que no estén en la lista.
"""


def interpret_command(text):
    load_dotenv(ENV_PATH, override=True)

    api_key = os.getenv("NVIDIA_API_KEY")
    if not api_key:
        raise ValueError("NVIDIA_API_KEY must be set in .env")

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key
    )

    try:
        completion = client.chat.completions.create(
            model="moonshotai/kimi-k2.5",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": text}
            ],
            temperature=0.6,
            max_tokens=512
        )
        raw = completion.choices[0].message.content
        if raw is None:
            return {
                "message": "No pude procesar tu mensaje. ¿Puedes intentarlo de nuevo?",
                "skill": None,
                "params": {},
                "status": "ok"
            }
        raw = raw.strip()
        raw = raw.replace("```json", "").replace("```", "").strip()
        parsed = json.loads(raw)

        return {
            "message": parsed.get("message", "Entendido."),
            "skill": parsed.get("skill", None),
            "params": parsed.get("params", {}),
            "status": "ok"
        }
    except json.JSONDecodeError:
        return {
            "message": raw if raw else "No entendí tu mensaje, ¿puedes reformularlo?",
            "skill": None,
            "params": {},
            "status": "ok"
        }
    except Exception as e:
        print(f"Error calling NVIDIA API: {e}")
        return {
            "message": "Tuve un problema conectándome. Intenta de nuevo en un momento.",
            "skill": None,
            "params": {},
            "status": "error"
        }
