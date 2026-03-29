"""
Ray Agent — Instalador de Primera Vez
========================================
Corre este script UNA SOLA VEZ para configurar Ray Agent en tu PC.
Solo necesitas tu NVIDIA_API_KEY. Todo lo demás está incluido.

Uso:
    python setup_first_time.py
"""
import os
import sys
import shutil
import subprocess

# ─────────────────────────────────────────────────
# CREDENCIALES DE SUPABASE (públicas / anon key)
# No necesitas configurarlas, ya están incluidas.
# ─────────────────────────────────────────────────
SUPABASE_URL = "https://wnxuozsztttajoamhmmd.supabase.co"
SUPABASE_KEY = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    ".eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndueHVvenN6dHR0YWpvYW1obW1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ0MDM1MzgsImV4cCI6MjA4OTk3OTUzOH0"
    ".cRIDgZfnjrVuDprxubj_PDYvlN8j62Oyvhn8KhJh4oM"
)


def banner(text):
    print()
    print("=" * 55)
    print(f"  {text}")
    print("=" * 55)


def step(n, text):
    print(f"\n[{n}/5] {text}")


def main():
    banner("⚡ Ray Agent — Instalador")

    # ────────────────────────────────────────────
    # PASO 1 — Obtener NVIDIA_API_KEY del usuario
    # ────────────────────────────────────────────
    step(1, "Configurar NVIDIA API Key")
    print("""
  Ray usa la IA de NVIDIA para entender tus comandos.
  Necesitas una cuenta gratuita en:

      https://build.nvidia.com

  Una vez dentro:
    1. Haz clic en cualquier modelo (ej. Kimi K2)
    2. Haz clic en "Get API Key"
    3. Copia la clave (empieza con "nvapi-...")
    """)

    nvidia_key = ""
    while not nvidia_key.startswith("nvapi-"):
        nvidia_key = input("  Pega tu NVIDIA_API_KEY aquí: ").strip()
        if not nvidia_key.startswith("nvapi-"):
            print("  ✗ La clave debe empezar con 'nvapi-'. Intenta de nuevo.\n")

    print("  ✓ Clave válida recibida.")

    # ────────────────────────────────────────────
    # PASO 2 — Crear archivo .env
    # ────────────────────────────────────────────
    step(2, "Guardando configuración")

    server_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(server_dir, '..')
    env_path = os.path.normpath(os.path.join(project_dir, '.env'))

    env_content = f"""SUPABASE_URL={SUPABASE_URL}
SUPABASE_KEY={SUPABASE_KEY}
NVIDIA_API_KEY={nvidia_key}
"""

    # Si ya existe un .env con ROOM_CODE, conservarlo
    existing_room = ""
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            for line in f:
                if line.startswith("ROOM_CODE="):
                    existing_room = line.strip()
                    break

    if existing_room:
        env_content += f"{existing_room}\n"

    with open(env_path, 'w') as f:
        f.write(env_content)

    print(f"  ✓ .env guardado en: {env_path}")

    # ────────────────────────────────────────────
    # PASO 3 — Instalar dependencias
    # ────────────────────────────────────────────
    step(3, "Instalando dependencias")
    deps = [
        "pystray", "pillow", "pyperclip",
        "pyinstaller", "pycaw", "comtypes",
        "python-dotenv", "supabase", "openai",
        "pyautogui", "pygetwindow"
    ]
    print(f"  Instalando: {', '.join(deps)}")
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install"] + deps + ["--quiet"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"  ⚠ Algunos paquetes fallaron (puede continuar):")
        print(f"    {result.stderr[:200]}")
    else:
        print("  ✓ Dependencias instaladas.")

    # ────────────────────────────────────────────
    # PASO 4 — Compilar el .exe
    # ────────────────────────────────────────────
    step(4, "Compilando RayAgent.exe (tarda ~2 min)")
    try:
        from build import build as run_build
        exe_path = run_build()
    except Exception as e:
        print(f"  ✗ Error al compilar: {e}")
        sys.exit(1)

    # ────────────────────────────────────────────
    # PASO 5 — Copiar al escritorio y ejecutar
    # ────────────────────────────────────────────
    step(5, "Instalando en tu escritorio")

    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    dest    = os.path.join(desktop, "RayAgent.exe")

    try:
        shutil.copy2(exe_path, dest)
        print(f"  ✓ RayAgent.exe copiado al escritorio: {dest}")
    except Exception as e:
        print(f"  ⚠ No se pudo copiar al escritorio: {e}")
        dest = exe_path  # Usar el original si falla

    # Ejecutar automáticamente
    try:
        subprocess.Popen([dest], creationflags=subprocess.DETACHED_PROCESS)
        print("  ✓ Ray Agent iniciado.")
    except Exception as e:
        print(f"  ⚠ No se pudo iniciar automáticamente: {e}")
        print(f"  → Ábrelo manualmente: {dest}")

    # ────────────────────────────────────────────
    # Mensaje final
    # ────────────────────────────────────────────
    print()
    print("=" * 55)
    print("  ✅ Ray Agent instalado correctamente")
    print("=" * 55)
    print("""
  El ícono ⚡ aparecerá en tu bandeja del sistema
  (esquina inferior derecha, junto al reloj).

  Desde ahí puedes:
    • Ver tu código de vinculación
    • Abrir el panel web
    • Copiar el código para la app móvil

  Ray arrancará automáticamente con Windows.
  ¡Ya no necesitas abrir CMD nunca más!
    """)
    input("  Presiona Enter para cerrar este instalador...")


if __name__ == "__main__":
    main()
