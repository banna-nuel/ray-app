"""
Skills multimedia — reproducción, pistas, volumen por pasos.
"""
from skills.base import Skill

try:
    import pyautogui
except ImportError:
    pyautogui = None


class PlayPause(Skill):
    name = "PlayPause"
    description = "Pausar o reanudar reproducción"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        if pyautogui:
            pyautogui.press('playpause')
            return {"success": True, "message": "Reproducción pausada/reanudada"}
        return {"success": False, "message": "PyAutoGUI no disponible"}


class NextTrack(Skill):
    name = "NextTrack"
    description = "Siguiente pista"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        if pyautogui:
            pyautogui.press('nexttrack')
            return {"success": True, "message": "Siguiente pista ⏭"}
        return {"success": False, "message": "PyAutoGUI no disponible"}


class PrevTrack(Skill):
    name = "PrevTrack"
    description = "Pista anterior"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        if pyautogui:
            pyautogui.press('prevtrack')
            return {"success": True, "message": "Pista anterior ⏮"}
        return {"success": False, "message": "PyAutoGUI no disponible"}


class VolumeUp(Skill):
    name = "VolumeUp"
    description = "Subir volumen N pasos"

    def __init__(self, steps: int = 1, **kwargs):
        self.steps = max(1, steps)

    def execute(self):
        if pyautogui:
            pyautogui.press('volumeup', presses=self.steps * 2)
            return {"success": True, "message": f"Volumen subido ({self.steps} pasos)"}
        return {"success": False, "message": "PyAutoGUI no disponible"}


class VolumeDown(Skill):
    name = "VolumeDown"
    description = "Bajar volumen N pasos"

    def __init__(self, steps: int = 1, **kwargs):
        self.steps = max(1, steps)

    def execute(self):
        if pyautogui:
            pyautogui.press('volumedown', presses=self.steps * 2)
            return {"success": True, "message": f"Volumen bajado ({self.steps} pasos)"}
        return {"success": False, "message": "PyAutoGUI no disponible"}
