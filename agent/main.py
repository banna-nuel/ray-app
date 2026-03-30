import os
import time
import socket
import random
import string
from dotenv import load_dotenv

load_dotenv()

from db import get_client, upsert_room, get_pending_commands, update_command
from interpreter import interpret
from executor import execute


def generate_room_code() -> str:
    chars = string.ascii_uppercase + string.digits
    return "RAY-" + "".join(random.choices(chars, k=4))


def get_or_create_code() -> str:
    """Read from .env, or generate and persist a new one."""
    code = os.getenv("ROOM_CODE", "").strip()
    if code:
        return code

    code = generate_room_code()
    env_path = os.path.join(os.path.dirname(__file__), ".env")
    with open(env_path, "a") as f:
        f.write(f"\nROOM_CODE={code}\n")
    os.environ["ROOM_CODE"] = code
    return code


def main():
    room_code = get_or_create_code()
    pc_name = socket.gethostname()

    print("=" * 50)
    print("  Ray Agent")
    print(f"  Sala  : {room_code}")
    print(f"  PC    : {pc_name}")
    print("=" * 50)
    print()

    # Create/update room in Supabase
    result = upsert_room(room_code, pc_name, True)
    if not result.data:
        print("✗ No se pudo conectar con Supabase.")
        print("  Verifica SUPABASE_URL y SUPABASE_KEY en .env")
        return

    room_id = result.data[0]["id"]
    print(f"  Agente en línea. Escuchando comandos...")
    print(f"  Ctrl+C para salir")
    print()

    heartbeat_counter = 0

    try:
        while True:
            # Heartbeat every ~30s (15 iterations × 2s sleep)
            heartbeat_counter += 1
            if heartbeat_counter >= 15:
                upsert_room(room_code, pc_name, True)
                heartbeat_counter = 0

            # Fetch pending commands
            cmds = get_pending_commands(room_id)

            for cmd in (cmds.data or []):
                print(f"  → {cmd['input']}")

                # Interpret with Groq
                result = interpret(cmd["input"])
                message = result.get("message", "")
                action = result.get("action")
                params = result.get("params", {})

                # Execute action if any
                exec_result = ""
                if action and action != "null":
                    exec_result_dict = execute(action, params)
                    exec_result = str(exec_result_dict)

                    # Append system info to message if available
                    if exec_result_dict.get("data"):
                        info = exec_result_dict["data"]
                        info_str = " | ".join(f"{k}: {v}" for k, v in info.items())
                        message += f"\n{info_str}"

                # Update command in Supabase
                update_command(
                    cmd["id"],
                    message,
                    action or "chat",
                    "done",
                    exec_result
                )
                print(f"  Ray: {message}")
                print()

            time.sleep(2)

    except KeyboardInterrupt:
        print("\n  Desconectando...")
        upsert_room(room_code, pc_name, False)
        print("  Agente detenido.")


if __name__ == "__main__":
    main()
