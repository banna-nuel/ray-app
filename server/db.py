import os
from dotenv import load_dotenv
from supabase import create_client, Client

# Cargar .env desde la raíz del proyecto
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env'))

def get_client() -> Client:
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    if not url or not key:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")
    return create_client(url, key)

def get_room_by_code(room_code):
    """Find a room by its code."""
    client = get_client()
    try:
        response = client.table("rooms").select("*").eq("room_code", room_code).execute()
        if response.data and len(response.data) > 0:
            return response.data[0]
    except Exception as e:
        print(f"Error fetching room: {e}")
    return None

def upsert_room(room_code, pc_name=None, is_online=True):
    """Create or update a room by its code."""
    client = get_client()
    data = {
        "room_code": room_code,
        "is_online": is_online,
        "last_seen": "now()" if is_online else None
    }
    if pc_name:
        data["pc_name"] = pc_name
        
    try:
        # Upsert by room_code (unique index)
        response = client.table("rooms").upsert(data, on_conflict="room_code").execute()
        return response.data[0] if response.data else None
    except Exception as e:
        print(f"Error upserting room: {e}")
        return None

def get_pending_commands(room_id):
    """Fetch pending commands for a room."""
    client = get_client()
    try:
        response = (client.table("commands")
                    .select("*")
                    .eq("room_id", room_id)
                    .eq("status", "pending")
                    .order("created_at")
                    .execute())
        return response.data or []
    except Exception as e:
        print(f"Error fetching commands: {e}")
        return []

def update_command(command_id, message, action, params, result, status):
    """Update a command with the result."""
    client = get_client()
    data = {
        "message": message,
        "action": action,
        "params": params if isinstance(params, dict) else {},
        "result": result,
        "status": status
    }
    try:
        client.table("commands").update(data).eq("id", command_id).execute()
    except Exception as e:
        print(f"Error updating command: {e}")


