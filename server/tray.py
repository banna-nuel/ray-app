"""
Ray Agent — System Tray App (v2)
Corre el agente en segundo plano, configura automáticamente en primera ejecución.
El usuario NUNCA necesita abrir una terminal.
"""
import pystray
from PIL import Image, ImageDraw
import threading
import webbrowser
import sys
import os
import winreg

# ────────────────────────────────────────────────
# Credenciales públicas de Supabase (anon key)
# ────────────────────────────────────────────────
SUPABASE_URL = "https://wnxuozsztttajoamhmmd.supabase.co"
SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndueHVvenN6dHR0YWpvYW1obW1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ0MDM1MzgsImV4cCI6MjA4OTk3OTUzOH0"
    ".cRIDgZfnjrVuDprxubj_PDYvlN8j62Oyvhn8KhJh4oM"
)

# ────────────────────────────────────────────────
# Rutas
# ────────────────────────────────────────────────
CONFIG_DIR = r"C:\RayApp"
ENV_PATH = os.path.join(CONFIG_DIR, ".env")

if getattr(sys, 'frozen', False):
    BASE_DIR = sys._MEIPASS
    EXE_DIR  = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    EXE_DIR  = BASE_DIR

# Agregar módulos al path
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)


# ────────────────────────────────────────────────
# Primera ejecución — pedir NVIDIA_API_KEY con GUI
# ────────────────────────────────────────────────
def first_time_setup():
    """Verifica si existe .env con NVIDIA_API_KEY. Si no, pide al usuario con ventana gráfica."""
    os.makedirs(CONFIG_DIR, exist_ok=True)

    # ¿Ya tiene configuración?
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            content = f.read()
        if "NVIDIA_API_KEY=" in content and "nvapi-" in content:
            return True  # Ya configurado

    # Primera vez — pedir NVIDIA_API_KEY con tkinter
    nvidia_key = ask_nvidia_key_gui()
    if not nvidia_key:
        return False

    # Guardar .env
    env_content = (
        f"SUPABASE_URL={SUPABASE_URL}\n"
        f"SUPABASE_KEY={SUPABASE_KEY}\n"
        f"NVIDIA_API_KEY={nvidia_key}\n"
    )

    # Conservar ROOM_CODE si existe
    if os.path.exists(ENV_PATH):
        with open(ENV_PATH, 'r') as f:
            for line in f:
                if line.startswith("ROOM_CODE="):
                    env_content += line.strip() + "\n"
                    break

    with open(ENV_PATH, 'w') as f:
        f.write(env_content)

    # También copiar al directorio del proyecto si es dev
    project_env = os.path.join(EXE_DIR, '..', '.env')
    if os.path.exists(os.path.dirname(project_env)):
        try:
            with open(project_env, 'w') as f:
                f.write(env_content)
        except:
            pass

    return True


def ask_nvidia_key_gui():
    """Ventana gráfica para pedir NVIDIA_API_KEY sin terminal."""
    try:
        import tkinter as tk
        from tkinter import messagebox

        root = tk.Tk()
        root.title("⚡ Ray Agent — Configuración")
        root.configure(bg="#0a0a0f")
        root.geometry("480x380")
        root.resizable(False, False)

        # Centrar en pantalla
        root.update_idletasks()
        x = (root.winfo_screenwidth() // 2) - 240
        y = (root.winfo_screenheight() // 2) - 190
        root.geometry(f"+{x}+{y}")

        result = {"key": None}

        # Título
        tk.Label(root, text="⚡ Ray Agent", font=("Segoe UI", 20, "bold"),
                 fg="#6c63ff", bg="#0a0a0f").pack(pady=(20, 5))

        tk.Label(root, text="Configuración de primera vez",
                 font=("Segoe UI", 11), fg="#6b6b8a", bg="#0a0a0f").pack(pady=(0, 15))

        # Instrucciones
        instructions = (
            "Ray necesita una API Key de NVIDIA para funcionar.\n\n"
            "1. Ve a:  https://build.nvidia.com\n"
            "2. Crea una cuenta gratuita\n"
            "3. Haz clic en cualquier modelo → \"Get API Key\"\n"
            "4. Copia la clave (empieza con nvapi-...)"
        )
        tk.Label(root, text=instructions, font=("Segoe UI", 9),
                 fg="#e8e8f0", bg="#0a0a0f", justify="left", anchor="w").pack(padx=30, fill="x")

        # Input
        tk.Label(root, text="NVIDIA API KEY:", font=("Segoe UI", 9, "bold"),
                 fg="#6b6b8a", bg="#0a0a0f", anchor="w").pack(padx=30, fill="x", pady=(15, 3))

        entry = tk.Entry(root, font=("Consolas", 11), bg="#13131f", fg="#e8e8f0",
                         insertbackground="#6c63ff", relief="flat", bd=0,
                         highlightthickness=1, highlightcolor="#6c63ff",
                         highlightbackground="#1e1e35")
        entry.pack(padx=30, fill="x", ipady=8)

        error_label = tk.Label(root, text="", font=("Segoe UI", 9),
                               fg="#ff4444", bg="#0a0a0f")
        error_label.pack(padx=30)

        def on_submit():
            key = entry.get().strip()
            if not key.startswith("nvapi-"):
                error_label.config(text="✗ La clave debe empezar con 'nvapi-'")
                return
            result["key"] = key
            root.destroy()

        def on_close():
            root.destroy()

        btn = tk.Button(root, text="Guardar y Conectar", font=("Segoe UI", 11, "bold"),
                        bg="#6c63ff", fg="white", relief="flat", bd=0, cursor="hand2",
                        activebackground="#5a52e0", activeforeground="white",
                        command=on_submit)
        btn.pack(padx=30, fill="x", ipady=8, pady=(10, 5))

        root.protocol("WM_DELETE_WINDOW", on_close)
        entry.focus_set()
        entry.bind("<Return>", lambda e: on_submit())

        root.mainloop()
        return result["key"]

    except Exception as e:
        # Si tkinter falla (raro en Windows), intentar input básico
        print(f"GUI error: {e}")
        return None


# ────────────────────────────────────────────────
# Icono: círculo violeta con rayo blanco
# ────────────────────────────────────────────────
def create_icon_image():
    img  = Image.new('RGBA', (64, 64), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.ellipse([2, 2, 62, 62], fill='#6c63ff')
    draw.polygon([
        (38, 8), (22, 34), (32, 34),
        (26, 56), (44, 28), (34, 28)
    ], fill='white')
    return img


# ────────────────────────────────────────────────
# Hilo del agente
# ────────────────────────────────────────────────
def run_agent_thread():
    try:
        from agent import main as agent_main
        agent_main()
    except Exception as e:
        import traceback
        log_path = os.path.join(CONFIG_DIR, 'ray_error.log')
        with open(log_path, 'a') as f:
            f.write(f"\n=== ERROR ===\n")
            traceback.print_exc(file=f)


# ────────────────────────────────────────────────
# Acciones del menú
# ────────────────────────────────────────────────
def open_web(icon, item):
    room_code = os.getenv("ROOM_CODE", "")
    webbrowser.open(f"https://ray-app-wine.vercel.app?code={room_code}")

def copy_code(icon, item):
    try:
        import pyperclip
        room_code = os.getenv("ROOM_CODE", "SIN CÓDIGO")
        pyperclip.copy(room_code)
    except:
        pass

def quit_app(icon, item):
    icon.stop()
    sys.exit(0)


# ────────────────────────────────────────────────
# Registro de Windows — inicio automático
# ────────────────────────────────────────────────
def setup_autostart():
    if getattr(sys, 'frozen', False):
        exe_path = sys.executable
    else:
        exe_path = os.path.abspath(__file__)
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "RayAgent", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
    except Exception as e:
        with open(os.path.join(CONFIG_DIR, 'ray_error.log'), 'a') as f:
            f.write(f"Autostart error: {e}\n")


# ────────────────────────────────────────────────
# Entry point
# ────────────────────────────────────────────────
def main():
    # Paso 1: Primera ejecución — mostrar GUI si no hay config
    if not first_time_setup():
        # Usuario canceló
        try:
            import tkinter.messagebox as mb
            mb.showwarning("Ray Agent", "Configuración cancelada.\nRay Agent necesita la NVIDIA API Key para funcionar.")
        except:
            pass
        sys.exit(1)

    # Paso 2: Cargar .env
    from dotenv import load_dotenv
    load_dotenv(dotenv_path=ENV_PATH, override=True)

    # También cargar .env del proyecto (dev)
    project_env = os.path.join(BASE_DIR, '..', '.env')
    if os.path.exists(project_env):
        load_dotenv(dotenv_path=project_env, override=True)

    room_code = os.getenv("ROOM_CODE", "generando...")

    # Paso 3: Configurar inicio automático con Windows
    setup_autostart()

    # Paso 4: Iniciar el agente en hilo daemon
    agent_thread = threading.Thread(target=run_agent_thread, daemon=True)
    agent_thread.start()

    # Paso 5: Abrir panel web automáticamente
    webbrowser.open(f"https://ray-app-wine.vercel.app?code={room_code}")

    # Paso 6: Construir menú de bandeja
    menu = pystray.Menu(
        pystray.MenuItem("⚡ Ray Agent",    None, enabled=False),
        pystray.MenuItem(f"Código: {room_code}", None, enabled=False),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Abrir panel web", open_web),
        pystray.MenuItem("Copiar código",   copy_code),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Salir",           quit_app),
    )

    icon = pystray.Icon(
        "RayAgent",
        create_icon_image(),
        f"Ray Agent — {room_code}",
        menu
    )
    icon.run()


if __name__ == "__main__":
    main()
