"""
Ray Agent — Build Script
Compila tray.py a un ejecutable Windows sin ventana de CMD.
"""
import subprocess
import sys
import os
import shutil


def build():
    server_dir = os.path.dirname(os.path.abspath(__file__))
    env_path   = os.path.join(server_dir, '..', '.env')
    env_path   = os.path.normpath(env_path)

    print("=" * 55)
    print("  ⚡ Ray Agent — Compilador")
    print("=" * 55)
    print(f"  Directorio: {server_dir}")
    print(f"  .env:       {env_path}")
    print()

    if not os.path.exists(env_path):
        print("✗ ERROR: No se encontró el archivo .env")
        sys.exit(1)

    # Limpiar builds anteriores
    for folder in ['build', 'dist']:
        path = os.path.join(server_dir, folder)
        if os.path.exists(path):
            shutil.rmtree(path)
    spec = os.path.join(server_dir, 'RayAgent.spec')
    if os.path.exists(spec):
        os.remove(spec)

    add_data = f"{env_path};."

    # Módulos locales del servidor
    local_modules = ["agent.py", "db.py", "ai_interpreter.py", "executor.py"]

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name=RayAgent",
        "--icon=logo.ico",
        f"--add-data={add_data}",
    ]

    for mod in local_modules:
        mod_path = os.path.join(server_dir, mod)
        if os.path.exists(mod_path):
            cmd.append(f"--add-data={mod_path};.")

    # Excluir librerías pesadas que PyInstaller arrastra innecesariamente
    excludes = [
        "tensorflow", "torch", "numpy", "pandas", "scipy",
        "matplotlib", "sklearn", "cv2", "transformers",
        "torchaudio", "torchvision", "tensorboard",
        "keras", "jax", "IPython", "notebook", "jupyterlab",
        "pytest", "unittest",
    ]
    for exc in excludes:
        cmd.append(f"--exclude-module={exc}")

    cmd += [
        "--hidden-import=pystray._win32",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=pyperclip",
        "--hidden-import=pycaw",
        "--hidden-import=pycaw.pycaw",
        "--hidden-import=comtypes",
        "--hidden-import=comtypes.client",
        "--hidden-import=dotenv",
        "--hidden-import=openai",
        "--hidden-import=httpx",
        "--hidden-import=httpx._transports",
        "--hidden-import=httpcore",
        "--hidden-import=pyautogui",
        "--hidden-import=pygetwindow",
        "--hidden-import=supabase",
        "--hidden-import=gotrue",
        "--hidden-import=postgrest",
        "--hidden-import=realtime",
        "--hidden-import=storage3",
        "--hidden-import=supafunc",
        "--collect-all=pystray",
        "--collect-all=supabase",
        "--collect-all=gotrue",
        "--collect-all=postgrest",
        "--collect-all=realtime",
        "--collect-all=storage3",
        "--collect-all=supafunc",
        "--noupx",
        "tray.py"
    ]

    print("  Compilando... (puede tardar 2-5 minutos)\n")
    result = subprocess.run(cmd, cwd=server_dir)

    if result.returncode == 0:
        exe_src = os.path.join(server_dir, 'dist', 'RayAgent.exe')
        print()
        print("=" * 55)
        print("  ✓ Compilación exitosa")
        print(f"  Ejecutable: {exe_src}")
        print("=" * 55)

        # Copiar al escritorio
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        dest = os.path.join(desktop, "RayAgent.exe")
        try:
            shutil.copy2(exe_src, dest)
            print(f"  ✓ Copiado al escritorio: {dest}")
        except Exception as e:
            print(f"  ⚠ No se pudo copiar al escritorio: {e}")
            dest = exe_src

        return dest
    else:
        print("✗ Error durante la compilación.")
        sys.exit(1)


if __name__ == "__main__":
    build()
