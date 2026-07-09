# Despliegue de CrediBot

## Render (recomendado para MVP)

El archivo `render.yaml` incluye una configuración base.

### Pasos

1. Sube el repositorio a GitHub
2. Crea un **Web Service** en [Render](https://render.com)
3. Conecta el repositorio `CrediBot-Uleam`
4. Usa la rama `develop` o `main`
5. Configura:
   - **Root Directory:** `creditbot`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Variables de entorno en Render

| Variable | Valor |
|---|---|
| `APP_ENV` | `production` |
| `APP_PUBLIC_URL` | `https://tu-servicio.onrender.com` |
| `TWILIO_VALIDATE_SIGNATURE` | `true` |
| `SUPABASE_URL` | URL de Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | Service Role Key |
| `TWILIO_ACCOUNT_SID` | Account SID |
| `TWILIO_AUTH_TOKEN` | Auth Token |
| `TWILIO_WHATSAPP_FROM` | `whatsapp:+14155238886` o tu número |

### Webhook en Twilio

Configura:

```text
https://tu-servicio.onrender.com/webhook/whatsapp
```

## Railway

1. Crea un proyecto nuevo
2. Selecciona el repositorio
3. Define `creditbot` como directorio raíz si aplica
4. Start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

5. Agrega las mismas variables de entorno

## Verificación post-despliegue

1. `GET https://tu-servicio.onrender.com/health`
2. `GET https://tu-servicio.onrender.com/webhook/whatsapp`
3. Envía un mensaje real desde WhatsApp Sandbox
4. Consulta `GET /admin/requests` para validar persistencia

## Desarrollo local con túnel

Si aún no despliegas, usa ngrok:

```bash
uvicorn app.main:app --reload
ngrok http 8000
```

Luego configura en Twilio la URL de ngrok terminando en `/webhook/whatsapp`.
