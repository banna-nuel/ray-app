from supabase import create_client
from dotenv import load_dotenv
from datetime import datetime, timezone
import os

load_dotenv()


def get_client():
    return create_client(
        os.getenv("SUPABASE_URL"),
        os.getenv("SUPABASE_KEY")
    )


def upsert_room(room_code: str, pc_name: str, online: bool):
    client = get_client()
    return client.table("rooms").upsert({
        "room_code": room_code,
        "pc_name": pc_name,
        "is_online": online,
        "last_seen": datetime.now(timezone.utc).isoformat()
    }, on_conflict="room_code").execute()


def get_pending_commands(room_id: str):
    client = get_client()
    return client.table("commands") \
        .select("*") \
        .eq("room_id", room_id) \
        .eq("status", "pending") \
        .order("created_at") \
        .execute()


def update_command(command_id: str, message: str,
                   action: str, status: str, result: str = ""):
    client = get_client()
    client.table("commands").update({
        "message": message,
        "action": action,
        "status": status,
        "result": result
    }).eq("id", command_id).execute()
