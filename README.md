# Ray App ⚡

Controla tu PC de forma remota desde tu celular usando IA.

## Estructura

```
ray-app/
├── server/              # Agente Python (tray app + skills)
│   ├── tray.py          # App de bandeja del sistema
│   ├── agent.py         # Listener de comandos
│   ├── ai_interpreter.py# IA con NVIDIA API
│   ├── skills/          # Sistema modular de skills
│   ├── build.py         # Compilador del .exe
│   └── requirements.txt
├── ray-app-web/         # Frontend Astro (Vercel)
│   └── src/pages/
│       ├── index.astro        # Web PC: código + QR
│       └── app/
│           ├── index.astro    # Login/Registro
│           ├── dashboard.astro# Lista de PCs + escáner QR
│           └── chat.astro     # Chat con IA
├── ray-app-android/     # App Android (WebView)
├── vercel.json
├── .env
└── README.md
```

## Uso

### PC
1. Descarga y ejecuta `RayAgent.exe`
2. En la primera ejecución, ingresa tu NVIDIA API Key
3. El código de sala aparece automáticamente en el navegador

### Celular
1. Abre ray-app-wine.vercel.app/app
2. Crea una cuenta o inicia sesión
3. Escanea el QR del PC o ingresa el código manualmente
4. Envía comandos por texto o voz

## Skills disponibles
- SetVolume, GetVolume, Mute, Unmute
- Shutdown, Restart, LockScreen, Screenshot
- OpenApp, CloseApp, MinimizeAll, MaximizeWindow
- OpenURL, GoogleSearch, YouTubeSearch
- PlayPause, NextTrack, PrevTrack, VolumeUp, VolumeDown
