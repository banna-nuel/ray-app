"""
Skills de sistema Windows — volumen, apagado, captura, info.
"""
import os
import time
import subprocess
import ctypes
from skills.base import Skill

try:
    import pyautogui
except ImportError:
    pyautogui = None

try:
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    HAS_PYCAW = True
except ImportError:
    HAS_PYCAW = False

try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False


def _get_volume_interface():
    """Obtener interfaz de audio del sistema."""
    if not HAS_PYCAW:
        return None
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        return cast(interface, POINTER(IAudioEndpointVolume))
    except Exception:
        return None


# ─────────────────── VOLUMEN ───────────────────


class SetVolume(Skill):
    name = "SetVolume"
    description = "Establecer volumen del sistema (0-100)"

    def __init__(self, level: int = 50, **kwargs):
        self.level = max(0, min(100, level))

    def execute(self):
        vol = _get_volume_interface()
        if vol:
            vol.SetMasterVolumeLevelScalar(self.level / 100.0, None)
            return {"success": True, "message": f"Volumen al {self.level}%", "data": self.level}
        return {"success": False, "message": "No se pudo acceder al control de audio"}


class GetVolume(Skill):
    name = "GetVolume"
    description = "Obtener volumen actual del sistema"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        vol = _get_volume_interface()
        if vol:
            current = int(vol.GetMasterVolumeLevelScalar() * 100)
            return {"success": True, "message": f"Volumen actual: {current}%", "data": current}
        return {"success": False, "message": "No se pudo leer el volumen"}


class Mute(Skill):
    name = "Mute"
    description = "Silenciar audio"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        vol = _get_volume_interface()
        if vol:
            vol.SetMute(True, None)
            return {"success": True, "message": "Audio silenciado"}
        if pyautogui:
            pyautogui.press('volumemute')
            return {"success": True, "message": "Audio silenciado"}
        return {"success": False, "message": "No se pudo silenciar"}


class Unmute(Skill):
    name = "Unmute"
    description = "Activar audio"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        vol = _get_volume_interface()
        if vol:
            vol.SetMute(False, None)
            return {"success": True, "message": "Audio activado"}
        return {"success": False, "message": "No se pudo activar el audio"}


# ─────────────────── SISTEMA ───────────────────


class Shutdown(Skill):
    name = "Shutdown"
    description = "Apagar PC con delay en segundos"

    def __init__(self, delay: int = 30, **kwargs):
        self.delay = delay

    def execute(self):
        subprocess.Popen(["shutdown", "/s", "/t", str(self.delay)], shell=True)
        mins = self.delay // 60
        secs = self.delay % 60
        t = f"{mins} min {secs}s" if mins else f"{secs} segundos"
        return {"success": True, "message": f"PC se apagará en {t}. Usa CancelShutdown para cancelar."}


class Restart(Skill):
    name = "Restart"
    description = "Reiniciar PC con delay en segundos"

    def __init__(self, delay: int = 30, **kwargs):
        self.delay = delay

    def execute(self):
        subprocess.Popen(["shutdown", "/r", "/t", str(self.delay)], shell=True)
        return {"success": True, "message": f"PC se reiniciará en {self.delay} segundos."}


class CancelShutdown(Skill):
    name = "CancelShutdown"
    description = "Cancelar apagado/reinicio programado"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        subprocess.Popen(["shutdown", "/a"], shell=True)
        return {"success": True, "message": "Apagado/reinicio cancelado."}


class LockScreen(Skill):
    name = "LockScreen"
    description = "Bloquear pantalla de Windows"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        try:
            ctypes.windll.user32.LockWorkStation()
            return {"success": True, "message": "Pantalla bloqueada."}
        except Exception as e:
            return {"success": False, "message": f"No se pudo bloquear: {e}"}


class Screenshot(Skill):
    name = "Screenshot"
    description = "Tomar captura de pantalla"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        if not pyautogui:
            return {"success": False, "message": "PyAutoGUI no disponible"}
        try:
            folder = r"C:\RayApp\Screenshots"
            os.makedirs(folder, exist_ok=True)
            filename = f"ray_shot_{int(time.time())}.png"
            path = os.path.join(folder, filename)
            pyautogui.screenshot(path)
            return {"success": True, "message": f"Captura guardada: {path}", "data": path}
        except Exception as e:
            return {"success": False, "message": f"Error al capturar: {e}"}


class GetSystemInfo(Skill):
    name = "GetSystemInfo"
    description = "Obtener info del sistema (CPU, RAM, disco)"

    def __init__(self, **kwargs):
        pass

    def execute(self):
        if not HAS_PSUTIL:
            return {"success": False, "message": "psutil no instalado"}
        try:
            cpu = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('C:\\')
            info = (
                f"🖥 CPU: {cpu}%\n"
                f"🧠 RAM: {ram.percent}% ({ram.used // (1024**3)}/{ram.total // (1024**3)} GB)\n"
                f"💾 Disco C: {disk.percent}% ({disk.used // (1024**3)}/{disk.total // (1024**3)} GB)\n"
                f"🔋 Batería: {psutil.sensors_battery().percent}%" if psutil.sensors_battery() else ""
            )
            return {"success": True, "message": info, "data": {
                "cpu": cpu, "ram_percent": ram.percent, "disk_percent": disk.percent
            }}
        except Exception as e:
            return {"success": False, "message": f"Error obteniendo info: {e}"}
