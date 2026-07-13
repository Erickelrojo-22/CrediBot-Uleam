# Panel administrativo Streamlit

El panel administrativo permite consultar la informacion registrada por CrediBot en Supabase: metricas generales, solicitudes de credito, casos derivados y usuarios.

La vista **Casos Derivados / Atención Humana** funciona como bandeja tipo WhatsApp: muestra el
motivo, resumen para asesor, chat en vivo y permite **responder por Twilio** desde el panel.

## Requisitos

- Python 3.11+
- Dependencias instaladas desde `requirements.txt`
- Proyecto Supabase con el esquema de `supabase/schema.sql`
- Archivo `.env` configurado en la carpeta `creditbot`

## Instalacion

Desde la carpeta `creditbot`:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

En Linux/macOS:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

## Variables necesarias (panel + respuestas Twilio)

Edita `creditbot/.env` y configura:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
ADMIN_DASHBOARD_PASSWORD=tu_clave_admin

TWILIO_ACCOUNT_SID=your-twilio-account-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
```

**Importante:** para que el bot reciba mensajes entrantes, las mismas variables `TWILIO_*` deben estar en el **backend Render** (`credibot-uleam-gjj2`) con `APP_PUBLIC_URL` y webhook en Twilio Sandbox.

El panel envía respuestas **directo por Twilio** (más rápido). Si no hay Twilio en el panel, intenta el respaldo `BACKEND_API_URL` + `ADMIN_DASHBOARD_PASSWORD` (el backend también necesita Twilio).

Plantilla Streamlit Secrets: `dashboard/.streamlit/secrets.toml.example`

## Ejecutar el panel

Desde la carpeta `creditbot`:

```bash
streamlit run dashboard/app.py
```

Streamlit abrira el panel en una URL local, normalmente:

```text
http://localhost:8501
```

## Despliegue en Render

El panel se despliega como un **segundo Web Service** separado del backend del bot.

| Campo Render | Valor |
|---|---|
| **Name** | `creditbot-dashboard` |
| **Root Directory** | `creditbot` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run dashboard/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true --browser.gatherUsageStats=false` |
| **Health Check Path** | `/_stcore/health` |

Variables de entorno en Render (servicio **dashboard**):

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_ROLE_KEY=tu-service-role-key
ADMIN_DASHBOARD_PASSWORD=tu_clave_admin
TWILIO_ACCOUNT_SID=tu-account-sid
TWILIO_AUTH_TOKEN=tu-auth-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
BACKEND_API_URL=https://credibot-uleam-gjj2.onrender.com
```

Variables en Render (servicio **backend** del bot):

```env
WHATSAPP_PROVIDER=twilio
TWILIO_ACCOUNT_SID=tu-account-sid
TWILIO_AUTH_TOKEN=tu-auth-token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
APP_PUBLIC_URL=https://credibot-uleam-gjj2.onrender.com
ADMIN_DASHBOARD_PASSWORD=tu_clave_admin
```

Al abrir la URL de Render, ingresa la contraseña configurada en `ADMIN_DASHBOARD_PASSWORD`.

## Despliegue en Streamlit Community Cloud

En `https://share.streamlit.io`, usa estos valores:

| Campo | Valor |
|---|---|
| **Repository** | `MantaVIbers/CrediBot-Uleam` |
| **Branch** | `main` |
| **Main file path** | `creditbot/dashboard/app.py` |
| **App URL** | `credibot-dashboard` o el nombre disponible que prefieras |

En **Advanced settings**, pega los secretos en formato TOML (ver `secrets.toml.example`):

```toml
SUPABASE_URL = "https://tu-proyecto.supabase.co"
SUPABASE_SERVICE_ROLE_KEY = "tu-service-role-key"
ADMIN_DASHBOARD_PASSWORD = "tu_clave_admin"
TWILIO_ACCOUNT_SID = "ACxxxxxxxx"
TWILIO_AUTH_TOKEN = "tu-token"
TWILIO_WHATSAPP_FROM = "whatsapp:+14155238886"
```

## Flujo de prueba

1. Abre la URL local de Streamlit.
2. Ingresa la clave configurada en `ADMIN_DASHBOARD_PASSWORD`.
3. Revisa la pagina principal con metricas generales.
4. Abre `Atención Humana` / `Casos Derivados`.
5. Verifica el banner de configuración (Twilio listo).
6. Selecciona un contacto por nombre/teléfono y responde.
7. Usa `Cerrar caso` cuando el asesor haya atendido la derivación.

## Problemas comunes

| Problema | Causa probable | Solucion |
|---|---|---|
| Banner: falta Twilio | No hay `TWILIO_*` en el panel | Agrega las 3 variables en `.env` o Secrets |
| Twilio rechazó el envío | Sandbox sin join o número mal formado | Haz `join` al Sandbox y usa teléfono E.164 |
| El cliente no recibe | Backend sin webhook Twilio | Configura webhook en Twilio → `/webhook/whatsapp` |
| No se pudo consultar Supabase | URL o Service Role Key incorrectas | Revisa `SUPABASE_URL` y `SUPABASE_SERVICE_ROLE_KEY` |
