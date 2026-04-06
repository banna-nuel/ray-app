from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()

_supabase_client = None


def get_client():
    global _supabase_client
    if _supabase_client is None:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_KEY")
        if not url or not key:
            raise ValueError("SUPABASE_URL y SUPABASE_KEY deben estar en .env")
        _supabase_client = create_client(url, key)
    return _supabase_client


def upsert_room(room_code: str, pc_name: str = None, is_online: bool = True):
    """Create or update a room."""
    client = get_client()

    data = {
        "room_code": room_code,
        "pc_name": pc_name,
        "is_online": is_online
    }

    # Check if room exists
    result = client.table("rooms").select("id").eq("room_code", room_code).execute()

    if result.data:
        # Update existing room
        room_id = result.data[0]["id"]
        client.table("rooms").update(data).eq("id", room_id).execute()
        return room_id
    else:
        # Create new room
        result = client.table("rooms").insert(data).execute()
        return result.data[0]["id"] if result.data else None


def get_room_by_code(room_code: str):
    """Get room by code."""
    client = get_client()
    result = client.table("rooms").select("*").eq("room_code", room_code.upper()).execute()
    return result.data[0] if result.data else None


def get_room_by_id(room_id: str):
    """Get room by ID."""
    client = get_client()
    result = client.table("rooms").select("*").eq("id", room_id).execute()
    return result.data[0] if result.data else None


def get_pending_commands(room_id: str):
    """Get pending commands for a room."""
    client = get_client()
    result = client.table("commands") \
        .select("*") \
        .eq("room_id", room_id) \
        .eq("status", "pending") \
        .execute()
    return result.data


def update_command(command_id: str, message: str = None, action: str = None,
                   status: str = None, result: str = None):
    """Update a command."""
    client = get_client()

    data = {}
    if message is not None:
        data["message"] = message
    if action is not None:
        data["action"] = action
    if status is not None:
        data["status"] = status
    if result is not None:
        data["result"] = result

    client.table("commands").update(data).eq("id", command_id).execute()
