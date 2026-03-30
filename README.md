# Ray App

Controla tu PC con Windows desde el celular usando inteligencia artificial.

## Arquitectura

```
web/      → Astro + Tailwind  (abre en el PC, muestra código QR)
mobile/   → HTML vanilla      (app del celular en el navegador)
agent/    → Python            (corre en el PC, ejecuta comandos)
```

## Setup rápido

### 1. Supabase

Crea un proyecto en [supabase.com](https://supabase.com) y ejecuta este SQL:

```sql
-- Salas de conexión
CREATE TABLE rooms (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at timestamptz DEFAULT now(),
  room_code text UNIQUE NOT NULL,
  pc_name text,
  user_id uuid,
  is_online boolean DEFAULT false,
  last_seen timestamptz DEFAULT now()
);

-- Comandos
CREATE TABLE commands (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at timestamptz DEFAULT now(),
  room_id uuid REFERENCES rooms(id) ON DELETE CASCADE,
  input text NOT NULL,
  message text,
  action text,
  params jsonb DEFAULT '{}',
  status text DEFAULT 'pending',
  result text
);

-- Habilitar Realtime
ALTER PUBLICATION supabase_realtime ADD TABLE rooms;
ALTER PUBLICATION supabase_realtime ADD TABLE commands;

-- RLS deshabilitado (simplificado)
ALTER TABLE rooms DISABLE ROW LEVEL SECURITY;
ALTER TABLE commands DISABLE ROW LEVEL SECURITY;
```

Copia la **URL** y el **anon key** del proyecto.

### 2. Groq API

- Crea cuenta en [console.groq.com](https://console.groq.com) (gratis)
- Genera una API key

### 3. Variables de entorno

Copia `.env.example` a `.env` y completa los valores:

```
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJ...
GROQ_API_KEY=gsk_...
```

### 4. Web del PC (Vercel)

```bash
cd web
npm install
npm run dev     # desarrollo local
```

En Vercel:
- Root directory: `web/`
- El `vercel.json` ya está configurado

### 5. App móvil

Los archivos de `mobile/` son HTML estático. Vercel los servirá en `/mobile/`.

Para acceder desde el celular: `https://tu-dominio.vercel.app/mobile/index.html`

### 6. Agente Python (PC)

```bash
cd agent
pip install -r requirements.txt
python main.py
```

El agente:
- Genera un código de sala (ej. `RAY-4FA9`) si no hay uno en `.env`
- Actualiza Supabase cada 30 segundos (heartbeat)
- Escucha comandos y los ejecuta con IA (Groq + Llama 3.3)

## Flujo completo

1. El PC abre `https://tu-dominio.vercel.app` → ve código RAY-XXXX y QR
2. Corre `python agent/main.py` en el PC
3. El celular abre la app, escanea el QR o ingresa el código
4. Chat en tiempo real — el celular envía comandos, el PC los ejecuta

## Comandos disponibles

| Comando de ejemplo | Acción |
|---|---|
| "Abre Chrome" | `open_app` |
| "Sube el volumen al 80%" | `set_volume` |
| "Bloquea la pantalla" | `lock_screen` |
| "Cuánta RAM está usando?" | `get_system_info` |
| "Pon la siguiente canción" | `next_track` |
| "Apaga el PC en 1 minuto" | `shutdown` |
| "Abre youtube.com" | `open_url` |
