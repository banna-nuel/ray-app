// ── Supabase config ──────────────────────────────────────
const SUPABASE_URL = 'https://wnxuozsztttajoamhmmd.supabase.co';
const SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndueHVvenN6dHR0YWpvYW1obW1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ0MDM1MzgsImV4cCI6MjA4OTk3OTUzOH0.cRIDgZfnjrVuDprxubj_PDYvlN8j62Oyvhn8KhJh4oM';

// Esperar a que la lib esté disponible
function waitForSupabase() {
  return new Promise(resolve => {
    if (window.supabase) return resolve(window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY));
    const id = setInterval(() => {
      if (window.supabase) {
        clearInterval(id);
        resolve(window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY));
      }
    }, 50);
  });
}

// Singleton
let _sb = null;
async function getSB() {
  if (!_sb) _sb = await waitForSupabase();
  return _sb;
}

// ── Auth helpers ─────────────────────────────────────────
async function getSession() {
  const sb = await getSB();
  const { data } = await sb.auth.getSession();
  return data.session;
}

async function requireAuth() {
  const session = await getSession();
  if (!session) {
    window.location.href = '/mobile/index.html';
    throw new Error('Not authenticated');
  }
  return session;
}

async function signOut() {
  const sb = await getSB();
  await sb.auth.signOut();
  window.location.href = '/mobile/index.html';
}

// ── URL helpers ──────────────────────────────────────────
function getParam(key) {
  return new URLSearchParams(window.location.search).get(key);
}

// Export
window.RayApp = { getSB, getSession, requireAuth, signOut, getParam };
