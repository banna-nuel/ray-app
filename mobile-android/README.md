# Ray Android App

Aplicación Android nativa para controlar tu PC con Ray.

## Como abrir en Android Studio

1. Abre Android Studio
2. Selecciona **"Open"** y navega a la carpeta `mobile-android/`
3. Espera a que Gradle sincronice el proyecto
4. Conecta tu celular o usa un emulador
5. Presiona el botón **Run** (▶️)

## Estructura

```
mobile-android/
├── app/
│   ├── src/main/
│   │   ├── java/com/rayapp/
│   │   │   └── MainActivity.java    # Actividad principal con WebView
│   │   ├── res/
│   │   │   ├── layout/
│   │   │   ├── values/
│   │   │   └── mipmap-*/            # Iconos de la app
│   │   └── assets/
│   │       └── mobile/              # Archivos web de la app
│   │           ├── index.html
│   │           ├── chat.html
│   │           ├── style.css
│   │           └── app.js
│   └── build.gradle.kts
├── build.gradle.kts
└── settings.gradle.kts
```

## Funcionalidades

- ✅ WebView con la interfaz web de Ray
- ✅ Soporte para cámara (escaneo QR)
- ✅ Soporte para micrófono (comandos por voz)
- ✅ Pull-to-refresh
- ✅ Navegación con botón atrás
- ✅ Permisos automáticos

## Generar APK

Build → Build Bundle(s) / APK(s) → Build APK(s)

El APK se guardará en:
`app/build/outputs/apk/debug/app-debug.apk`
