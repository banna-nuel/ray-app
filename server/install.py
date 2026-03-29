"""
Ray Agent — Installer
Sets up the environment, credentials, and compiles the app to EXE.
"""
import os
import sys
import subprocess
import shutil
import winreg
import random
import socket

def print_banner():
    print("=" * 60)
    print("         ⚡ RAY AGENT - INSTALADOR DE WINDOWS ⚡")
    print("=" * 60)
    print("Este script configurará Ray en tu PC para control remoto.")
    print()

def get_input(prompt, default=None):
    val = input(f"{prompt} [{default}]: " if default else f"{prompt}: ")
    return val.strip() or default

def setup():
    print_banner()

    # 1. Ask for credentials
    print("--- CONFIGURACIÓN DE CREDENCIALES ---")
    print("Consúltalas en tu panel de Supabase y NVIDIA.")
    
    url = get_input("SUPABASE_URL")
    key = get_input("SUPABASE_KEY (Anon/Public)")
    nvidia = get_input("NVIDIA_API_KEY")

    if not url or not key or not nvidia:
        print("❌ Error: Todas las llaves son obligatorias.")
        return

    # 2. Setup Directory
    target_dir = r"C:\RayApp"
    if not os.path.exists(target_dir):
        try:
            os.makedirs(target_dir)
        except Exception as e:
            print(f"❌ No se pudo crear el directorio {target_dir}. Ejecuta como Administrador.")
            print(f"Error: {e}")
            return

    # 3. Generate Room Code
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    room_code = 'RAY-' + ''.join(random.choice(chars) for _ in range(4))

    # 4. Save .env
    env_content = f"""SUPABASE_URL={url}
SUPABASE_KEY={key}
NVIDIA_API_KEY={nvidia}
ROOM_CODE={room_code}
"""
    env_path = os.path.join(target_dir, ".env")
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"✅ Configuración guardada en {env_path}")

    # 5. Compile to EXE
    print("\n--- COMPILANDO APLICACIÓN (.EXE) ---")
    print("Esto puede tardar un minuto...")
    
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tray_script = os.path.join(current_dir, "tray.py")
    
    # Run PyInstaller
    try:
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name=RayAgent",
            f"--workpath={os.path.join(target_dir, 'build')}",
            f"--distpath={target_dir}",
            "--specpath={}".format(target_dir),
            "--clean",
            tray_script
        ]
        subprocess.run(cmd, check=True)
        print(f"✅ Compilación exitosa: {os.path.join(target_dir, 'RayAgent.exe')}")
    except Exception as e:
        print(f"❌ Error al compilar: {e}")
        print("Asegúrate de tener pyinstaller instalado: pip install pyinstaller")
        return

    # 6. Windows Startup Registry
    print("\n--- REGISTRANDO INICIO AUTOMÁTICO ---")
    exe_path = os.path.join(target_dir, "RayAgent.exe")
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Run",
            0, winreg.KEY_SET_VALUE
        )
        winreg.SetValueEx(key, "RayAgent", 0, winreg.REG_SZ, exe_path)
        winreg.CloseKey(key)
        print("✅ Ray Agent arrancará automáticamente con Windows.")
    except Exception as e:
        print(f"⚠ No se pudo registrar en el inicio automático: {e}")

    # 7. Start the app
    print("\n--- INICIANDO RAY AGENT ---")
    try:
        subprocess.Popen([exe_path], shell=True)
        print("⚡ ¡Ray Agent ya está en ejecución en tu bandeja del sistema!")
    except:
        print("⚠ No se pudo iniciar automáticamente. Búscalo en C:\\RayApp\\RayAgent.exe")

    print("\n" + "=" * 60)
    print(f" 🎉 INSTALACIÓN COMPLETADA CON ÉXITO")
    print(f" TU CÓDIGO DE SALA ES: {room_code}")
    print("=" * 60)
    print("Ya puedes cerrar esta ventana y controlar tu PC desde el móvil.")

if __name__ == "__main__":
    setup()
