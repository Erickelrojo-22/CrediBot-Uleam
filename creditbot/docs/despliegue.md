# Despliegue de CrediBot

CrediBot se compone de dos servicios: backend FastAPI y panel Streamlit. El backend
es el único servicio que debe tener las credenciales de Kapso.

## Backend en Render

| Campo | Valor |
|---|---|
| Directorio raíz | `creditbot` |
| Comando de construcción | `pip install -r requirements.txt` |
| Comando de inicio | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Health check | `/health` |

Variables de entorno obligatorias:

```env
APP_ENV=production
APP_PUBLIC_URL=https://tu-backend.onrender.com
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
WHATSAPP_PROVIDER=kapso
KAPSO_API_KEY=...
KAPSO_PHONE_NUMBER_ID=...
KAPSO_WEBHOOK_SECRET=...
KAPSO_VALIDATE_WEBHOOK_SIGNATURE=true
ADMIN_DASHBOARD_PASSWORD=...
```

Si se usa sesión compartida en producción, agrega `REDIS_URL`. Las claves de OpenAI
solo son necesarias si se activa la redacción con IA.

## Webhook Kapso

Registra en Kapso la URL:

```text
https://tu-backend.onrender.com/webhook/whatsapp
```

Suscribe el evento `whatsapp.message.received` y usa el mismo secreto configurado
en `KAPSO_WEBHOOK_SECRET`. Consulta `/health/whatsapp` tras desplegar: debe mostrar
`configured: true` antes de probar WhatsApp.

## Panel Streamlit

Despliega el panel como un servicio distinto con estas variables:

```env
SUPABASE_URL=...
SUPABASE_SERVICE_ROLE_KEY=...
ADMIN_DASHBOARD_PASSWORD=...
BACKEND_API_URL=https://tu-backend.onrender.com
```

No copies las credenciales de Kapso al panel.

## Verificación post-despliegue

1. `GET /health`
2. `GET /health/whatsapp`
3. `POST /simulate/message` para verificar el flujo sin WhatsApp
4. Envía un mensaje al número de Kapso
5. Revisa en Supabase la conversación y la solicitud resultante
6. Deriva un caso y responde desde Streamlit

## Cloud Run

El repositorio incluye `Dockerfile` e `infra/cloudrun.yaml`. La misma configuración
aplica en Cloud Run: define las variables como secretos y registra la URL pública
del servicio en Kapso.
