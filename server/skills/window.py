"""
Skills de ventanas — abrir/cerrar apps, minimizar, maximizar.
"""
import subprocess
from skills.base import Skill

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    import pygetwindow as gw
except ImportError:
    gw = None


# Mapeo de nombres comunes a ejecutables de Windows
APP_MAP = {
    "chrome":     "chrome.exe",
    "google":     "chrome.exe",
    "edge":       "msedge.exe",
    "spotify":    "spotify.exe",
    "notepad":    "notepad.exe",
    "bloc de notas": "notepad.exe",
    "calculator": "calc.exe",
    "calculadora": "calc.exe",
    "explorer":   "explorer.exe",
    "explorador": "explorer.exe",
    "word":       "winword.exe",
    "excel":      "excel.exe",
    "powerpoint": "powerpnt.exe",
    "vscode":     "code.exe",
    "visual studio code": "code.exe",
    "discord":    "discord.exe",
    "whatsapp":   "whatsapp.exe",
    "telegram":   "telegram.exe",
    "teams":      "teams.exe",
    "zoom":       "zoom.exe",
    "paint":      "mspaint.exe",
    "cmd":        "cmd.exe",
    "terminal":   "wt.exe",
    "steam":      "steam.exe",
    "obs":        "obs64.exe",
    "vlc":        "vlc.exe",
}


class OpenApp(Skill):
    name = "OpenApp"
    description = "Abrir aplicación por nombre"

    def __init__(self, app_name: str = "", **kwargs):
        self.app_name = app_name.lower().strip()

    def execute(self):
        if not self.app_name:
            return {"success": False, "message": "No se proporcionó nombre de app"}

        exe = APP_MAP.get(self.app_name)

        if exe:
            # Intentar abrir directamente por ejecutable
            try:
                subprocess.Popen([exe], shell=True)
                return {"success": True, "message": f"Abriendo {self.app_name.title()}"}
            except Exception:
                pass

        # Fallback: buscar en el menú de inicio con pyautogui
        if pyautogui:
            try:
                pyautogui.press('win')
                pyautogui.sleep(0.5)
                pyautogui.write(self.app_name, interval=0.03)
                pyautogui.sleep(0.8)
                pyautogui.press('enter')
                return {"success": True, "message": f"Abriendo {self.app_name.title()}"}
            except Exception as e:
                return {"success": False, "message": f"Error: {e}"}

        return {"success": False, "message": "No se pudo abrir la aplicación"}


class CloseApp(Skill):
    name = "CloseApp"
    description = "Cerrar aplicación por nombre de ventana"

    def __init__(self, app_name: str = "", **kwargs):
        self.app_name = app_name.strip()

    def execute(self):
        if not self.app_name:
            return {"success": False, "message": "No se proporcionó nombre de app"}
        if not gw:
            return {"success": False, "message": "PyGetWindow no disponible"}
        try:
            windows = gw.getWindowsWithTitle(self.app_name)
            if not windows:
                # Intentar búsqueda parcial
                all_wins = gw.getAllWindows()
                windows = [w for w in all_wins if self.app_name.lower() in w.title.lower() and w.title]
            if windows:
                for w in windows:
                    w.close()
                return {"success": True, "message": f"Cerrando {self.app_name}"}
            return {"success": False, "message": f"No se encontró ventana: {self.app_name}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}


class MinimizeAll(Skill):
    name = "MinimizeAll"
    description = "Minimizar todas las ventanas (mostrar escritorio)"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        if pyautogui:
            pyautogui.hotkey('win', 'd')
            return {"success": True, "message": "Todas las ventanas minimizadas"}
        return {"success": False, "message": "PyAutoGUI no disponible"}


class MaximizeWindow(Skill):
    name = "MaximizeWindow"
    description = "Maximizar ventana por nombre"

    def __init__(self, app_name: str = "", **kwargs):
        self.app_name = app_name.strip()

    def execute(self):
        if not gw:
            return {"success": False, "message": "PyGetWindow no disponible"}
        try:
            all_wins = gw.getAllWindows()
            windows = [w for w in all_wins if self.app_name.lower() in w.title.lower() and w.title]
            if windows:
                windows[0].maximize()
                windows[0].activate()
                return {"success": True, "message": f"Ventana '{self.app_name}' maximizada"}
            return {"success": False, "message": f"No se encontró: {self.app_name}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}


class SwitchWindow(Skill):
    name = "SwitchWindow"
    description = "Cambiar entre ventanas (Alt+Tab)"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        if pyautogui:
            pyautogui.hotkey('alt', 'tab')
            return {"success": True, "message": "Cambiando ventana"}
        return {"success": False, "message": "PyAutoGUI no disponible"}
