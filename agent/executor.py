import subprocess
import os
import ctypes
import pyautogui
import psutil

try:
    import pygetwindow as gw
    HAS_GW = True
except Exception:
    HAS_GW = False

try:
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
    from ctypes import cast, POINTER
    from comtypes import CLSCTX_ALL
    HAS_AUDIO = True
except Exception:
    HAS_AUDIO = False

APP_MAP = {
    "chrome": "chrome.exe",
    "google chrome": "chrome.exe",
    "edge": "msedge.exe",
    "microsoft edge": "msedge.exe",
    "spotify": "spotify.exe",
    "notepad": "notepad.exe",
    "bloc de notas": "notepad.exe",
    "calculator": "calc.exe",
    "calculadora": "calc.exe",
    "explorer": "explorer.exe",
    "explorador": "explorer.exe",
    "word": "winword.exe",
    "excel": "excel.exe",
    "vscode": "code.exe",
    "visual studio code": "code.exe",
    "discord": "discord.exe",
    "whatsapp": "WhatsApp.exe",
    "vlc": "vlc.exe",
    "paint": "mspaint.exe",
    "task manager": "taskmgr.exe",
    "administrador de tareas": "taskmgr.exe",
}

pyautogui.FAILSAFE = False


def execute(action: str, params: dict) -> dict:
    try:
        if action == "open_app":
            name = params.get("app_name", "").lower()
            exe = APP_MAP.get(name, params.get("app_name", ""))
            subprocess.Popen(exe, shell=True)
            return {"success": True}

        elif action == "close_app":
            name = params.get("app_name", "").lower()
            killed = False
            for proc in psutil.process_iter(['name']):
                try:
                    if name in proc.info['name'].lower():
                        proc.kill()
                        killed = True
                except Exception:
                    pass
            return {"success": killed}

        elif action == "open_url":
            url = params.get("url", "")
            subprocess.Popen(f'start "" "{url}"', shell=True)
            return {"success": True}

        elif action == "set_volume":
            if not HAS_AUDIO:
                return {"success": False, "error": "pycaw no disponible"}
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            level = max(0.0, min(1.0, int(params.get("level", 50)) / 100))
            volume.SetMasterVolumeLevelScalar(level, None)
            return {"success": True}

        elif action == "mute":
            pyautogui.press('volumemute')
            return {"success": True}

        elif action == "shutdown":
            delay = params.get("delay", 30)
            subprocess.run(f"shutdown /s /t {delay}", shell=True)
            return {"success": True}

        elif action == "restart":
            delay = params.get("delay", 30)
            subprocess.run(f"shutdown /r /t {delay}", shell=True)
            return {"success": True}

        elif action == "lock_screen":
            ctypes.windll.user32.LockWorkStation()
            return {"success": True}

        elif action == "screenshot":
            path = r"C:\RayApp\screenshots"
            os.makedirs(path, exist_ok=True)
            from datetime import datetime
            filename = f"{path}\\{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            pyautogui.screenshot(filename)
            return {"success": True, "path": filename}

        elif action == "play_pause":
            pyautogui.press('playpause')
            return {"success": True}

        elif action == "next_track":
            pyautogui.press('nexttrack')
            return {"success": True}

        elif action == "prev_track":
            pyautogui.press('prevtrack')
            return {"success": True}

        elif action == "minimize_all":
            pyautogui.hotkey('win', 'd')
            return {"success": True}

        elif action == "type_text":
            pyautogui.write(params.get("text", ""), interval=0.03)
            return {"success": True}

        elif action == "press_key":
            pyautogui.press(params.get("key", ""))
            return {"success": True}

        elif action == "get_system_info":
            disk_path = "C:\\"
            info = {
                "cpu": f"{psutil.cpu_percent(interval=0.5):.1f}%",
                "ram": f"{psutil.virtual_memory().percent:.1f}%",
                "disk": f"{psutil.disk_usage(disk_path).percent:.1f}%"
            }
            return {"success": True, "data": info}

        return {"success": False, "error": f"Acción desconocida: {action}"}

    except Exception as e:
        return {"success": False, "error": str(e)}
