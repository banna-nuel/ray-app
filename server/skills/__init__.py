from skills.system import SetVolume, GetVolume, Mute, Unmute, Shutdown, Restart, CancelShutdown, LockScreen, Screenshot, GetSystemInfo
from skills.browser import OpenURL, NewTab, GoogleSearch, YouTubeSearch
from skills.media import PlayPause, NextTrack, PrevTrack, VolumeUp, VolumeDown
from skills.window import OpenApp, CloseApp, MinimizeAll, MaximizeWindow, SwitchWindow

SKILLS_MAP = {
    "SetVolume": SetVolume,
    "GetVolume": GetVolume,
    "Mute": Mute,
    "Unmute": Unmute,
    "Shutdown": Shutdown,
    "Restart": Restart,
    "CancelShutdown": CancelShutdown,
    "LockScreen": LockScreen,
    "Screenshot": Screenshot,
    "GetSystemInfo": GetSystemInfo,
    "OpenURL": OpenURL,
    "NewTab": NewTab,
    "GoogleSearch": GoogleSearch,
    "YouTubeSearch": YouTubeSearch,
    "PlayPause": PlayPause,
    "NextTrack": NextTrack,
    "PrevTrack": PrevTrack,
    "VolumeUp": VolumeUp,
    "VolumeDown": VolumeDown,
    "OpenApp": OpenApp,
    "CloseApp": CloseApp,
    "MinimizeAll": MinimizeAll,
    "MaximizeWindow": MaximizeWindow,
    "SwitchWindow": SwitchWindow,
}


def execute_skill(skill_name, params):
    """Ejecuta una skill por nombre con los parámetros dados."""
    if skill_name not in SKILLS_MAP:
        return {"success": False, "message": f"Skill '{skill_name}' no encontrada"}
    skill_class = SKILLS_MAP[skill_name]
    try:
        skill = skill_class(**params)
        return skill.execute()
    except Exception as e:
        return {"success": False, "message": f"Error ejecutando {skill_name}: {e}"}
