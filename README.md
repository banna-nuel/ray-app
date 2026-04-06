# Ray App

Controla tu PC con Windows desde tu celular mediante comandos en lenguaje natural con IA.

## Como funciona

1. Abre la web en tu PC, obtendras un codigo de sala y un QR
2. Desde tu celular, escanea el QR o ingresa el codigo manualmente
3. Escribe comandos en lenguaje natural desde el chat
4. La IA interpreta y ejecuta las acciones automaticamente en tu PC

## Setup rapido

### Supabase

1. Crear proyecto en supabase.com
2. Ejecutar el SQL en el editor SQL de Supabase:

```sql
CREATE TABLE rooms (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  created_at timestamptz DEFAULT now(),
  room_code text UNIQUE NOT NULL,
  pc_name text,
  is_online boolean DEFAULT false,
  last_seen timestamptz DEFAULT now()
);

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

ALTER PUBLICATION supabase_realtime ADD TABLE rooms;
ALTER PUBLICATION supabase_realtime ADD TABLE commands;
ALTER TABLE rooms DISABLE ROW LEVEL SECURITY;
ALTER TABLE commands DISABLE ROW LEVEL SECURITY;
```

### Groq (gratis)

1. Crear cuenta en console.groq.com
2. Generar API key
3. Copiar a .env como GROQ_API_KEY

## Correr localmente

### Web del PC

```bash
cd web
npm install
npm run dev
```

Abrir http://localhost:4321

### App movil

Abrir `mobile/index.html` en el navegador del celular o simular un dispositivo movil.

### Agente Python

```bash
cd agent
pip install -r requirements.txt
cp ../.env.example .env
# Editar .env con tus credenciales
python main.py
```

## Deploy en Vercel

1. Subir a GitHub
2. Importar en vercel.com
3. Vercel detecta la config automaticamente

## Capacidades

- Abrir y cerrar aplicaciones
- Controlar mouse y teclado
- Subir/bajar volumen, silenciar
- Abrir URLs en el navegador
- Bloquear pantalla
- Apagar y reiniciar PC
- Captura de pantalla
- Reproducir/pausar media, siguiente/anterior pista
- Minimizar todas las ventanas
- Escribir texto en el PC
- Obtener info del sistema (CPU, RAM, disco)
