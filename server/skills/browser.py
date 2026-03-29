"""
Skills de navegador — abrir URLs, buscar en Google/YouTube.
"""
import subprocess
import webbrowser
import urllib.parse
from skills.base import Skill


class OpenURL(Skill):
    name = "OpenURL"
    description = "Abrir URL en el navegador"

    def __init__(self, url: str = "", browser: str = "edge", **kwargs):
        self.url = url
        self.browser = browser.lower()

    def execute(self):
        if not self.url:
            return {"success": False, "message": "No se proporcionó una URL"}
        try:
            if self.browser == "chrome":
                subprocess.Popen(["start", "chrome", self.url], shell=True)
            elif self.browser == "edge":
                subprocess.Popen(["start", "msedge", self.url], shell=True)
            else:
                webbrowser.open(self.url)
            return {"success": True, "message": f"Abriendo {self.url}"}
        except Exception as e:
            return {"success": False, "message": f"Error abriendo URL: {e}"}


class NewTab(Skill):
    name = "NewTab"
    description = "Abrir nueva pestaña en el navegador activo"

    def __init__(self, url: str = "about:blank", **kwargs):
        self.url = url

    def execute(self):
        try:
            subprocess.Popen(["start", "msedge", self.url], shell=True)
            return {"success": True, "message": f"Nueva pestaña: {self.url}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}


class GoogleSearch(Skill):
    name = "GoogleSearch"
    description = "Buscar en Google"

    def __init__(self, query: str = "", **kwargs):
        self.query = query

    def execute(self):
        if not self.query:
            return {"success": False, "message": "No se proporcionó búsqueda"}
        url = f"https://www.google.com/search?q={urllib.parse.quote(self.query)}"
        try:
            subprocess.Popen(["start", "msedge", url], shell=True)
            return {"success": True, "message": f"Buscando: {self.query}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}


class YouTubeSearch(Skill):
    name = "YouTubeSearch"
    description = "Buscar en YouTube"

    def __init__(self, query: str = "", **kwargs):
        self.query = query

    def execute(self):
        if not self.query:
            return {"success": False, "message": "No se proporcionó búsqueda"}
        url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(self.query)}"
        try:
            subprocess.Popen(["start", "msedge", url], shell=True)
            return {"success": True, "message": f"Buscando en YouTube: {self.query}"}
        except Exception as e:
            return {"success": False, "message": f"Error: {e}"}
