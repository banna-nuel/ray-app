import subprocess
import os
import json
import urllib.parse
try:
    import pygetwindow as gw
except ImportError:
    gw = None
try:
    import pyautogui
except ImportError:
    pyautogui = None
try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
except ImportError:
    AudioUtilities = None
try:
    import pyperclip
except ImportError:
    pyperclip = None

def get_volume_interface():
    if not AudioUtilities: return None
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except:
        return None

def execute_action(action_data, confirmed=False):
    action = action_data.get("action")
    params = action_data.get("params", {})
    
    try:
        # --- CONTROL DE VOLUMEN ---
        if action == "set_volume":
            volume_level = params.get("volume", 50)
            volume = get_volume_interface()
            if volume:
                volume.SetMasterVolumeLevelScalar(volume_level / 100.0, None)
                return "ok", None
            return "error", "Pycaw no disponible"

        elif action == "volume_up":
            if pyautogui:
                pyautogui.press('volumeup', presses=5)
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "volume_down":
            if pyautogui:
                pyautogui.press('volumedown', presses=5)
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "mute":
            if pyautogui:
                pyautogui.press('volumemute')
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        # --- SISTEMA ---
        elif action == "shutdown":
            if not confirmed: return "error", "Requiere confirmación explícita"
            subprocess.Popen(["shutdown", "/s", "/t", "5"], shell=True)
            return "ok", None

        elif action == "restart":
            if not confirmed: return "error", "Requiere confirmación explícita"
            subprocess.Popen(["shutdown", "/r", "/t", "5"], shell=True)
            return "ok", None

        # --- MULTIMEDIA ---
        elif action == "pause_media":
            if pyautogui:
                pyautogui.press('playpause')
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "next_track":
            if pyautogui:
                pyautogui.press('nexttrack')
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "prev_track":
            if pyautogui:
                pyautogui.press('prevtrack')
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        # --- PERIFÉRICOS (MOUSE/TECLADO) ---
        elif action == "type_text":
            text = params.get("text", "")
            if pyautogui:
                pyautogui.write(text)
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "press_key":
            key = params.get("key", "")
            if pyautogui:
                pyautogui.press(key)
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "hotkey":
            keys = params.get("keys", [])
            if pyautogui and keys:
                pyautogui.hotkey(*keys)
                return "ok", None
            return "error", "PyAutoGUI o teclas no disponibles"

        elif action == "click":
            x, y = params.get("x"), params.get("y")
            if pyautogui:
                if x is not None and y is not None: pyautogui.click(x, y)
                else: pyautogui.click()
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "move_mouse":
            x, y = params.get("x", 0), params.get("y", 0)
            if pyautogui:
                pyautogui.moveTo(x, y)
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "screenshot":
            if pyautogui:
                os.makedirs(r"C:\RayApp\Screenshots", exist_ok=True)
                path = rf"C:\RayApp\Screenshots\shot_{int(os.time.time())}.png"
                pyautogui.screenshot(path)
                return "ok", f"Captura guardada en: {path}"
            return "error", "PyAutoGUI no disponible"

        # --- VENTANAS ---
        elif action == "minimize_window":
            title = params.get("app_name")
            if gw:
                wins = gw.getWindowsWithTitle(title)
                if wins: wins[0].minimize(); return "ok", None
                return "error", "Ventana no encontrada"
            return "error", "PyGetWindow no disponible"

        elif action == "maximize_window":
            title = params.get("app_name")
            if gw:
                wins = gw.getWindowsWithTitle(title)
                if wins: wins[0].maximize(); return "ok", None
                return "error", "Ventana no encontrada"
            return "error", "PyGetWindow no disponible"

        elif action == "close_window":
            title = params.get("app_name")
            if gw:
                wins = gw.getWindowsWithTitle(title)
                if wins: wins[0].close(); return "ok", None
                return "error", "Ventana no encontrada"
            return "error", "PyGetWindow no disponible"

        # --- ARCHIVOS Y COMANDOS ---
        elif action == "open_file":
            path = params.get("path", "")
            if os.path.exists(path):
                os.startfile(path)
                return "ok", None
            return "error", "Archivo no encontrado"

        elif action == "create_file":
            path = params.get("path", "")
            content = params.get("content", "")
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            return "ok", f"Archivo creado en {path}"

        elif action == "run_command":
            cmd = params.get("command", "")
            subprocess.Popen(cmd, shell=True)
            return "ok", f"Comando ejecutado: {cmd}"

        # --- CLIPBOARD ---
        elif action == "copy_to_clipboard":
            text = params.get("text", "")
            if pyperclip:
                pyperclip.copy(text)
                return "ok", None
            return "error", "Pyperclip no disponible"

        elif action == "get_clipboard":
            if pyperclip:
                content = pyperclip.paste()
                return "ok", content
            return "error", "Pyperclip no disponible"

        # --- ANTERIORES ---
        elif action == "open_app":
            app_name = params.get("app_name")
            if pyautogui:
                pyautogui.press('win'); pyautogui.sleep(0.5)
                pyautogui.write(app_name); pyautogui.sleep(0.5); pyautogui.press('enter')
                return "ok", None
            return "error", "PyAutoGUI no disponible"

        elif action == "open_edge_url":
            url = params.get("url")
            subprocess.Popen(["start", "msedge", url], shell=True)
            return "ok", None

        elif action == "edge_new_tab":
            url = params.get("url")
            subprocess.Popen(["start", "msedge", url], shell=True)
            return "ok", None

        elif action == "unknown":
            return "error", "No sé cómo hacer eso."
        else:
            return "error", f"Acción desconocida: {action}"

    except Exception as e:
        return "error", str(e)
