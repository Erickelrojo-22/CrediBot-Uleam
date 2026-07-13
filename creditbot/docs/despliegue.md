# Despliegue de CrediBot

CrediBot tiene **dos servicios independientes**:

| Servicio | Qué es | Puerto / URL |
|---|---|---|
| **Backend FastAPI** | Bot de WhatsApp (webhook Twilio) | `https://creditbot-uleam.onrender.com` |
| **Panel Streamlit** | Dashboard administrativo | `https://creditbot-dashboard.onrender.com` |

El archivo `render.yaml` define ambos servicios.

## Backend en Render (bot WhatsApp)

### Pasos

1. Sube el repositorio a GitHub
2. Crea un **Web Service** en [Render](https://render.com)
3. Conecta el repositorio `CrediBot-Uleam`
4. Usa la rama `main`
5. Configura:
   - **Root Directory:** `creditbot`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Health Check Path:** `/health`

### Variables de entorno del backend

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

```text
https://tu-servicio.onrender.com/webhook/whatsapp
```

## Panel Streamlit en Render

### Pasos

1. En Render → **New +** → **Web Service**
2. Mismo repositorio y rama `main`
3. Configura:

| Campo | Valor |
|---|---|
| **Name** | `creditbot-dashboard` |
| **Root Directory** | `creditbot` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run dashboard/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false` |
| **Health Check Path** | `/_stcore/health` |

### Variables de entorno del panel

| Variable | Valor |
|---|---|
| `SUPABASE_URL` | Misma URL del backend |
| `SUPABASE_SERVICE_ROLE_KEY` | Misma Service Role Key |
| `ADMIN_DASHBOARD_PASSWORD` | Contraseña del panel admin |

Guía detallada del panel: [`docs/streamlit_dashboard.md`](streamlit_dashboard.md)

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

## Google Cloud Run (recomendado)

El backend ya incluye `Dockerfile` y plantilla en `infra/cloudrun.yaml`.
El workflow `.github/workflows/deploy.yml` construye la imagen, la sube a Artifact Registry y despliega a Cloud Run.

### Activación en GitHub

1. Crea un service account de GCP con roles: Artifact Registry Writer, Cloud Run Admin, Service Account User
2. Secrets del repositorio:
   - `GCP_SA_KEY` — JSON de la cuenta de servicio
   - `GCP_PROJECT_ID` — ID del proyecto
3. Variables del repositorio:
   - `ENABLE_CLOUD_RUN_DEPLOY=true`
   - Opcionales: `GCP_REGION`, `CLOUD_RUN_SERVICE`, `ARTIFACT_REPO`
4. Crea el repositorio de Artifact Registry (`creditbot`) en la región elegida
5. Configura en Cloud Run las variables/secretos (`SUPABASE_*`, `OPENAI_*`, `REDIS_URL`, Twilio o Meta, `APP_PUBLIC_URL`)

Webhook: `https://TU-SERVICIO.run.app/webhook/whatsapp`

### Redis

Define `REDIS_URL` (Upstash o Memorystore). Sin Redis, los contadores de sesión usan memoria del contenedor (válido en desarrollo; en producción multi-réplica conviene Redis).

### Meta WhatsApp Cloud API

1. `WHATSAPP_PROVIDER=meta`
2. Completa `META_WHATSAPP_TOKEN`, `META_WHATSAPP_PHONE_NUMBER_ID`, `META_WHATSAPP_VERIFY_TOKEN`
3. Opcional: `META_WHATSAPP_APP_SECRET` para validar `X-Hub-Signature-256`
4. En Meta Developers, webhook GET/POST a `/webhook/whatsapp` con el verify token

## Desarrollo local con túnel

Si aún no despliegas, usa ngrok:

```bash
uvicorn app.main:app --reload
ngrok http 8000
```

Luego configura en Twilio (o Meta) la URL de ngrok terminando en `/webhook/whatsapp`.
