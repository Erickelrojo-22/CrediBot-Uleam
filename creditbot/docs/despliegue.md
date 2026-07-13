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
| `OPENAI_API_KEY` | Clave API OpenAI (IA + RAG) |
| `OPENAI_MODEL` | `gpt-4o-mini` (opcional) |

### Webhook en Twilio

Configura:

```text
https://tu-servicio.onrender.com/webhook/whatsapp
```

## CI/CD (Integración y despliegue continuo)

### CI — GitHub Actions

Archivo: `.github/workflows/ci.yml`

- Se ejecuta en cada **push** y **pull request** a `main` o `develop`.
- Instala dependencias desde `creditbot/requirements.txt`.
- Corre `pytest -v`.
- Si falla, el merge/deploy no debe continuar hasta corregir.

Verificar en GitHub → pestaña **Actions** → workflow **CI** en verde.

### CD — Render (auto-deploy)

1. Conecta el repo GitHub a Render.
2. Rama: **`develop`** (o `main` en producción final).
3. **Root Directory:** `creditbot`.
4. Cada push exitoso a la rama redeploya automáticamente.
5. Health check: `GET /health` debe responder `{"status":"ok"}`.

El archivo `render.yaml` define dos servicios:

| Servicio | Comando | Health |
|---|---|---|
| `creditbot` | `uvicorn app.main:app ...` | `/health` |
| `creditbot-dashboard` | `streamlit run dashboard/app.py ...` | `/_stcore/health` |

### Flujo completo

```text
git push origin develop
        │
        ▼
GitHub Actions (CI) ── pytest
        │
        ▼
Render (CD) ── redeploy backend + panel
        │
        ▼
Supabase + Twilio + OpenAI en producción
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
