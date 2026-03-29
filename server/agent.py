"""
Ray App — PC Agent (v5 — Skills System)
Runs on the PC, listens for commands via Supabase and executes them.
No login required. Works via ROOM_CODE.
"""
import os
import sys
import time
import signal
import threading
import socket
import webbrowser
import random
from dotenv import load_dotenv, set_key

# Load environment
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path, override=True)

from db import get_client, upsert_room, get_pending_commands, update_command, get_room_by_code
from ai_interpreter import interpret_command
from skills import execute_skill

POLL_INTERVAL = 2
HEARTBEAT_INTERVAL = 30

running = True
room = None

def generate_room_code():
    chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    return 'RAY-' + ''.join(random.choice(chars) for _ in range(4))

def get_or_create_code():
    code = os.getenv("ROOM_CODE")
    if not code:
        code = generate_room_code()
        set_key(dotenv_path, "ROOM_CODE", code)
        print(f"✨ Nuevo código generado: {code}")
    return code

def signal_handler(sig, frame):
    global running
    print("\n⏹ Deteniendo agente...")
    running = False

signal.signal(signal.SIGINT, signal_handler)

def heartbeat_loop(room_code):
    """Periodically update room status."""
    while running:
        try:
            upsert_room(room_code, is_online=True)
        except Exception as e:
            print(f"  ⚠ Error en heartbeat: {e}")
            
        for _ in range(HEARTBEAT_INTERVAL):
            if not running: break
            time.sleep(1)

def process_command(cmd, current_room):
    """Process a single pending command using the skills system."""
    cmd_id = cmd["id"]
    input_text = cmd["input"]

    print(f"  📨 Comando: \"{input_text}\"")

    try:
        get_client().table("commands").update({"status": "processing"}).eq("id", cmd_id).execute()

        # Interpret with AI
        ai_response = interpret_command(input_text)
        message = ai_response.get("message", "Hecho.")
        skill_name = ai_response.get("skill", None)
        params = ai_response.get("params", {})

        result = "ok"
        status = "done"
        action = skill_name or "chat"

        # Execute skill if one was identified
        if skill_name:
            skill_result = execute_skill(skill_name, params)
            if skill_result["success"]:
                # Append skill feedback to the AI message
                if skill_result.get("message") and skill_result["message"] != message:
                    message = f"{message}\n✓ {skill_result['message']}"
            else:
                status = "error"
                result = skill_result.get("message", "Error desconocido")
                message = f"Lo siento, falló: {result}"

        # Update Supabase
        update_command(cmd_id, message, action, params, result, status)
        print(f"  ✓ Ray: {message}")

    except Exception as e:
        print(f"  ⚠ Error procesando comando: {e}")

def main():
    global room
    
    room_code = get_or_create_code()
    pc_name = socket.gethostname()

    print("=" * 50)
    print("  ⚡ Ray App — Agente de PC (Sin Login)")
    print("=" * 50)
    print(f"  Sala: {room_code}")
    print(f"  PC:   {pc_name}")
    print()

    # Initial sync
    room = upsert_room(room_code, pc_name=pc_name, is_online=True)
    if not room:
        print("✗ No se pudo conectar con Supabase. Revisa tu conexión/configuración.")
        sys.exit(1)

    # Open Dashboard in Browser automatically
    # Update this URL based on your Vercel deployment if needed
    web_url = f"https://ray-app-wine.vercel.app/pc/?code={room_code}"
    print(f"  🌐 Abriendo panel web: {web_url}")
    try:
        webbrowser.open(web_url)
    except:
        pass

    # Start Heartbeat
    threading.Thread(target=heartbeat_loop, args=(room_code,), daemon=True).start()

    print(f"  ✓ Agente en línea y escuchando...")
    print(f"  (Presiona Ctrl+C para salir)")
    print()

    # Main Poll Loop
    try:
        while running:
            cmds = get_pending_commands(room["id"])
            for c in cmds:
                process_command(c, room)
            
            for _ in range(POLL_INTERVAL):
                if not running: break
                time.sleep(1)
    finally:
        upsert_room(room_code, is_online=False)
        print("  ✓ Agente desconectado.")

if __name__ == "__main__":
    main()

