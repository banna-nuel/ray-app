#!/usr/bin/env python3
"""
Ray Agent - Control PC via chat commands
"""

import os
import time
import random
import string
import atexit
import platform
from datetime import datetime
from dotenv import load_dotenv

from db import upsert_room, get_pending_commands, update_command
from interpreter import interpret
from executor import execute

load_dotenv()

# Configuration
HEARTBEAT_INTERVAL = 2  # seconds
COMMAND_CHECK_INTERVAL = 1  # seconds


def generate_room_code():
    """Generate a random room code."""
    chars = string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(4))
    return f"RAY-{code}"


def get_or_create_room_code():
    """Get room code from .env or generate a new one."""
    room_code = os.getenv("ROOM_CODE", "").strip()

    if room_code:
        return room_code

    # Generate new code
    room_code = generate_room_code()

    # Save to .env
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    with open(env_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    found = False
    for i, line in enumerate(lines):
        if line.startswith('ROOM_CODE='):
            lines[i] = f'ROOM_CODE={room_code}\n'
            found = True
            break

    if not found:
        lines.append(f'ROOM_CODE={room_code}\n')

    with open(env_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    return room_code


def process_command(command):
    """Process a single command."""
    command_id = command["id"]
    input_text = command["input"]

    print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Comando recibido: {input_text}")

    try:
        # Interpret command with AI
        interpretation = interpret(input_text)

        action = interpretation.get("action")
        params = interpretation.get("params", {})
        message = interpretation.get("message", "Listo")

        print(f"  Accion: {action}")
        print(f"  Params: {params}")

        # Execute the action
        if action:
            result = execute(action, params)
            print(f"  Resultado: {result}")
        else:
            result = {"success": True, "message": message}

        # Update command in database
        update_command(
            command_id=command_id,
            message=message,
            action=action,
            status="done",
            result=result.get("message", "")
        )

        print(f"  Respuesta: {message}")

    except Exception as e:
        print(f"  Error: {e}")
        update_command(
            command_id=command_id,
            message="Error al procesar el comando",
            status="error",
            result=str(e)
        )


def main():
    """Main loop."""
    print("=" * 50)
    print("Ray Agent - Control Remoto con IA")
    print("=" * 50)

    # Get room code
    room_code = get_or_create_room_code()
    pc_name = platform.node() or platform.system()

    print(f"\nPC: {pc_name}")
    print(f"Codigo de sala: {room_code}")
    print(f"\nInicializando...")

    try:
        # Register room
        room_id = upsert_room(room_code, pc_name, is_online=True)
        print(f"Sala registrada (ID: {room_id})")

        # Set offline on exit
        def set_offline():
            print("\nCerrando agente...")
            try:
                upsert_room(room_code, pc_name, is_online=False)
            except:
                pass

        atexit.register(set_offline)

        print("\nAgente listo. Esperando comandos...")
        print("Presiona Ctrl+C para salir\n")

        last_heartbeat = 0
        last_check = 0

        while True:
            current_time = time.time()

            # Send heartbeat every HEARTBEAT_INTERVAL seconds
            if current_time - last_heartbeat >= HEARTBEAT_INTERVAL:
                upsert_room(room_code, pc_name, is_online=True)
                last_heartbeat = current_time

            # Check for new commands every COMMAND_CHECK_INTERVAL seconds
            if current_time - last_check >= COMMAND_CHECK_INTERVAL:
                try:
                    commands = get_pending_commands(room_id)
                    for command in commands:
                        process_command(command)
                except Exception as e:
                    print(f"Error checking commands: {e}")

                last_check = current_time

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\n\nDeteniendo agente...")
    except Exception as e:
        print(f"\nError fatal: {e}")
        raise


if __name__ == "__main__":
    main()
