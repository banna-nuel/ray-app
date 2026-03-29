import { createClient } from '@supabase/supabase-js'

// Public credentials (anon key — safe to expose in frontend)
const supabaseUrl = import.meta.env.PUBLIC_SUPABASE_URL
  || 'https://wnxuozsztttajoamhmmd.supabase.co'

const supabaseAnonKey = import.meta.env.PUBLIC_SUPABASE_ANON_KEY
  || 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6IndueHVvenN6dHR0YWpvYW1obW1kIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzQ0MDM1MzgsImV4cCI6MjA4OTk3OTUzOH0.cRIDgZfnjrVuDprxubj_PDYvlN8j62Oyvhn8KhJh4oM'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)
