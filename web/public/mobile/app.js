import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2.39.0/+esm';

const SUPABASE_URL = 'https://wnxuozsztttajoamhmmd.supabase.co';
const SUPABASE_ANON_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndueHVvenN6dHR0YWpvYW1obW1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ0MDM1MzgsImV4cCI6MjA4OTk3OTUzOH0.cRIDgZfnjrVuDprxubj_PDYvlN8j62Oyvhn8KhJh4oM';

const supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);

let currentRoomId = null;
let currentRoomCode = null;
let commandSubscription = null;

// Get room by code
export async function getRoom(roomCode) {
  const { data, error } = await supabase
    .from('rooms')
    .select('*')
    .eq('room_code', roomCode.toUpperCase())
    .single();

  if (error) return null;
  return data;
}

// Connect to room
export async function connectToRoom(roomCode) {
  const room = await getRoom(roomCode);
  if (!room) return false;

  currentRoomId = room.id;
  currentRoomCode = room.room_code;
  localStorage.setItem('ray_current_room', roomCode);
  localStorage.setItem('ray_room_id', room.id);

  return true;
}

// Send command
export async function sendCommand(input) {
  if (!currentRoomId) {
    currentRoomId = localStorage.getItem('ray_room_id');
  }

  if (!currentRoomId) return null;

  const { data, error } = await supabase
    .from('commands')
    .insert({
      room_id: currentRoomId,
      input: input,
      status: 'pending'
    })
    .select()
    .single();

  if (error) {
    console.error('Error sending command:', error);
    return null;
  }

  return data;
}

// Get command history
export async function getHistory() {
  if (!currentRoomId) {
    currentRoomId = localStorage.getItem('ray_room_id');
  }

  if (!currentRoomId) return [];

  const { data, error } = await supabase
    .from('commands')
    .select('*')
    .eq('room_id', currentRoomId)
    .order('created_at', { ascending: false })
    .limit(50);

  if (error) return [];
  return data.reverse();
}

// Subscribe to command updates
export function subscribeToCommands(roomId, onUpdate) {
  if (commandSubscription) {
    commandSubscription.unsubscribe();
  }

  commandSubscription = supabase
    .channel(`commands:${roomId}`)
    .on('postgres_changes', {
      event: '*',
      schema: 'public',
      table: 'commands',
      filter: `room_id=eq.${roomId}`
    }, (payload) => {
      onUpdate(payload.new);
    })
    .subscribe();

  return commandSubscription;
}

// Subscribe to room updates
export function subscribeToRoom(roomId, onUpdate) {
  return supabase
    .channel(`room-status:${roomId}`)
    .on('postgres_changes', {
      event: 'UPDATE',
      schema: 'public',
      table: 'rooms',
      filter: `id=eq.${roomId}`
    }, (payload) => {
      onUpdate(payload.new);
    })
    .subscribe();
}

// Get current room info
export function getCurrentRoom() {
  return {
    roomId: currentRoomId || localStorage.getItem('ray_room_id'),
    roomCode: currentRoomCode || localStorage.getItem('ray_current_room')
  };
}

// Disconnect
export function disconnect() {
  currentRoomId = null;
  currentRoomCode = null;
  localStorage.removeItem('ray_current_room');
  localStorage.removeItem('ray_room_id');

  if (commandSubscription) {
    commandSubscription.unsubscribe();
    commandSubscription = null;
  }
}
