import os
import subprocess
import time
import json
import base64
import io
from typing import Dict, Any

try:
    import pyautogui
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
except ImportError:
    pyautogui = None

try:
    import pygetwindow as gw
except ImportError:
    gw = None

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    import comtypes
    volume_available = True
except ImportError:
    volume_available = False

try:
    import psutil
except ImportError:
    psutil = None

try:
    import pyperclip
except ImportError:
    pyperclip = None

from PIL import Image

# App name mapping
APP_MAP = {
    "chrome": "chrome",
    "google chrome": "chrome",
    "edge": "msedge",
    "microsoft edge": "msedge",
    "firefox": "firefox",
    "opera": "opera",
    "brave": "brave",
    "spotify": "spotify",
    "notepad": "notepad",
    "notepad++": "notepad++",
    "calculator": "calc",
    "calculadora": "calc",
    "explorer": "explorer",
    "explorador": "explorer",
    "word": "winword",
    "excel": "excel",
    "powerpoint": "powerpnt",
    "vscode": "code",
    "visual studio code": "code",
    "discord": "discord",
    "whatsapp": "whatsapp",
    "vlc": "vlc",
    "steam": "steam",
    "epic": "epicgameslauncher",
    "zoom": "zoom",
    "teams": "teams",
    "slack": "slack",
    "filezilla": "filezilla",
    "photoshop": "photoshop",
    "illustrator": "illustrator",
    "premiere": "premiere",
    "after effects": "afterfx",
    "cmd": "cmd",
    "terminal": "cmd",
    "powershell": "powershell",
    "paint": "mspaint",
}


def get_app_command(app_name: str) -> str:
    """Get the system command for an app name."""
    app_lower = app_name.lower().strip()
    if app_lower in APP_MAP:
        return APP_MAP[app_lower]
    return app_name


def open_app(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        app_name = params.get("app_name", "")
        if not app_name:
            return {"success": False, "message": "No se especifico la aplicacion"}

        cmd = get_app_command(app_name)

        # Try common paths
        try:
            subprocess.Popen(f"start {cmd}", shell=True)
            return {"success": True, "message": f"Abriendo {app_name}"}
        except:
            # Try with explorer
            try:
                subprocess.Popen(f"explorer shell:appsFolder\\{cmd}", shell=True)
                return {"success": True, "message": f"Abriendo {app_name}"}
            except:
                return {"success": False, "message": f"No pude abrir {app_name}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def close_app(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        app_name = params.get("app_name", "")
        if not app_name:
            return {"success": False, "message": "No se especifico la aplicacion"}

        app_lower = app_name.lower()
        closed = False

        if psutil:
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if app_lower in proc.info['name'].lower():
                        proc.terminate()
                        closed = True
                except:
                    pass

        # Try with pygetwindow
        if gw and not closed:
            try:
                windows = gw.getWindowsWithTitle(app_name)
                for window in windows:
                    window.close()
                    closed = True
            except:
                pass

        if closed:
            return {"success": True, "message": f"Cerrando {app_name}"}
        return {"success": False, "message": f"No encontre {app_name} abierto"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def open_url(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        url = params.get("url", "")
        if not url:
            return {"success": False, "message": "No se especifico la URL"}

        if not url.startswith(("http://", "https://")):
            url = "https://" + url

        os.system(f'start "" "{url}"')
        return {"success": True, "message": f"Abriendo {url}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def set_volume(params: Dict[str, Any]) -> Dict[str, Any]:
    if not volume_available:
        return {"success": False, "message": "Control de volumen no disponible"}

    try:
        level = params.get("level", 50)
        # Ensure level is between 0 and 100
        level = max(0, min(100, int(level)))

        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)

        # Convert percentage to scalar (0.0 to 1.0)
        volume.SetMasterVolumeLevelScalar(level / 100, None)

        return {"success": True, "message": f"Volumen ajustado a {level}%"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def mute(params: Dict[str, Any]) -> Dict[str, Any]:
    if not volume_available:
        return {"success": False, "message": "Control de volumen no disponible"}

    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(1, None)
        return {"success": True, "message": "Audio silenciado"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def unmute(params: Dict[str, Any]) -> Dict[str, Any]:
    if not volume_available:
        return {"success": False, "message": "Control de volumen no disponible"}

    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, comtypes.CLSCTX_ALL, None)
        volume = interface.QueryInterface(IAudioEndpointVolume)
        volume.SetMute(0, None)
        return {"success": True, "message": "Audio activado"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def shutdown(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        delay = params.get("delay", 30)
        subprocess.Popen(f"shutdown /s /t {delay}", shell=True)
        return {"success": True, "message": f"PC se apagara en {delay} segundos. Escribe 'cancelar apagado' para detenerlo."}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def restart(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        delay = params.get("delay", 30)
        subprocess.Popen(f"shutdown /r /t {delay}", shell=True)
        return {"success": True, "message": f"PC se reiniciara en {delay} segundos. Escribe 'cancelar reinicio' para detenerlo."}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def cancel_shutdown(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        subprocess.Popen("shutdown /a", shell=True)
        return {"success": True, "message": "Apagado/reinicio cancelado"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def lock_screen(params: Dict[str, Any]) -> Dict[str, Any]:
    try:
        import ctypes
        ctypes.windll.user32.LockWorkStation()
        return {"success": True, "message": "Pantalla bloqueada"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def screenshot(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        # Create screenshots directory
        screenshots_dir = os.path.join(os.path.expanduser("~"), "Pictures", "RayScreenshots")
        os.makedirs(screenshots_dir, exist_ok=True)

        filename = f"screenshot_{time.strftime('%Y%m%d_%H%M%S')}.png"
        filepath = os.path.join(screenshots_dir, filename)

        screenshot = pyautogui.screenshot()
        screenshot.save(filepath)

        return {"success": True, "message": f"Captura guardada en {filepath}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def screenshot_base64(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        screenshot = pyautogui.screenshot()
        buffered = io.BytesIO()
        screenshot.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        return {
            "success": True,
            "message": "Captura tomada",
            "screenshot": img_str
        }
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def play_pause(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        pyautogui.press('playpause')
        return {"success": True, "message": "Reproducir/Pausar"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def next_track(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        pyautogui.press('nexttrack')
        return {"success": True, "message": "Siguiente pista"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def prev_track(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        pyautogui.press('prevtrack')
        return {"success": True, "message": "Pista anterior"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def minimize_all(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        pyautogui.keyDown('win')
        pyautogui.keyDown('d')
        pyautogui.keyUp('d')
        pyautogui.keyUp('win')
        return {"success": True, "message": "Mostrando escritorio"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def type_text(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        text = params.get("text", "")
        if not text:
            return {"success": False, "message": "No se especifico texto"}

        pyautogui.typewrite(text, interval=0.01)
        return {"success": True, "message": f"Texto escrito"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def press_key(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        key = params.get("key", "").lower()
        if not key:
            return {"success": False, "message": "No se especifico tecla"}

        # Key mapping for special keys
        key_map = {
            "enter": "enter",
            "return": "enter",
            "space": "space",
            "espacio": "space",
            "tab": "tab",
            "escape": "esc",
            "esc": "esc",
            "backspace": "backspace",
            "delete": "delete",
            "del": "delete",
            "up": "up",
            "down": "down",
            "left": "left",
            "right": "right",
            "arriba": "up",
            "abajo": "down",
            "izquierda": "left",
            "derecha": "right",
            "pageup": "pageup",
            "pagedown": "pagedown",
            "home": "home",
            "end": "end",
            "f1": "f1", "f2": "f2", "f3": "f3", "f4": "f4", "f5": "f5",
            "f6": "f6", "f7": "f7", "f8": "f8", "f9": "f9", "f10": "f10",
            "f11": "f11", "f12": "f12",
            "ctrl": "ctrl",
            "control": "ctrl",
            "alt": "alt",
            "shift": "shift",
            "win": "win",
            "windows": "win",
            "cmd": "win",
            "command": "win",
        }

        mapped_key = key_map.get(key, key)
        pyautogui.press(mapped_key)
        return {"success": True, "message": f"Tecla {key} presionada"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def copy_text(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('c')
        pyautogui.keyUp('c')
        pyautogui.keyUp('ctrl')
        return {"success": True, "message": "Copiado"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def paste_text(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        pyautogui.keyDown('ctrl')
        pyautogui.keyDown('v')
        pyautogui.keyUp('v')
        pyautogui.keyUp('ctrl')
        return {"success": True, "message": "Pegado"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def get_system_info(params: Dict[str, Any]) -> Dict[str, Any]:
    if not psutil:
        return {"success": False, "message": "psutil no disponible"}

    try:
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        info = {
            "cpu_percent": cpu_percent,
            "ram_used": f"{memory.used / (1024**3):.1f} GB",
            "ram_total": f"{memory.total / (1024**3):.1f} GB",
            "ram_percent": memory.percent,
            "disk_used": f"{disk.used / (1024**3):.1f} GB",
            "disk_total": f"{disk.total / (1024**3):.1f} GB",
            "disk_percent": disk.percent
        }

        message = f"CPU: {cpu_percent}% | RAM: {info['ram_used']}/{info['ram_total']} ({info['ram_percent']}%) | Disco: {info['disk_percent']}% usado"

        return {"success": True, "message": message, "info": info}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def mouse_move(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        x = params.get("x", 0)
        y = params.get("y", 0)
        pyautogui.moveTo(x, y)
        return {"success": True, "message": f"Mouse movido a ({x}, {y})"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


def mouse_click(params: Dict[str, Any]) -> Dict[str, Any]:
    if not pyautogui:
        return {"success": False, "message": "PyAutoGUI no disponible"}

    try:
        button = params.get("button", "left")
        pyautogui.click(button=button)
        return {"success": True, "message": f"Clic {button}"}
    except Exception as e:
        return {"success": False, "message": f"Error: {str(e)}"}


# Action dispatcher
ACTIONS = {
    "open_app": open_app,
    "close_app": close_app,
    "open_url": open_url,
    "set_volume": set_volume,
    "mute": mute,
    "unmute": unmute,
    "shutdown": shutdown,
    "restart": restart,
    "cancel_shutdown": cancel_shutdown,
    "lock_screen": lock_screen,
    "screenshot": screenshot,
    "screenshot_base64": screenshot_base64,
    "play_pause": play_pause,
    "next_track": next_track,
    "prev_track": prev_track,
    "minimize_all": minimize_all,
    "type_text": type_text,
    "press_key": press_key,
    "copy": copy_text,
    "paste": paste_text,
    "get_system_info": get_system_info,
    "mouse_move": mouse_move,
    "mouse_click": mouse_click,
}


def execute(action: str, params: Dict[str, Any]) -> Dict[str, Any]:
    if not action:
        return {"success": True, "message": "Sin accion"}

    if action not in ACTIONS:
        return {"success": False, "message": f"Accion '{action}' no soportada"}

    return ACTIONS[action](params)
