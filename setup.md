# Guía de setup — CrediBot-Uleam

Configuración completa del proyecto: entorno local, Supabase, Twilio, OpenAI y Render.

> **Seguridad:** no subas claves reales a GitHub. El archivo `creditbot/.env` está en `.gitignore`.
> En esta guía, las **claves secretas** van marcadas para que las pegues tú desde tu `.env` local
> o desde los paneles de Supabase / Twilio / OpenAI.

---

## 1. Requisitos

| Herramienta | Versión |
|---|---|
| Python | 3.12+ |
| Git | cualquier reciente |
| Cuenta Supabase | proyecto PostgreSQL |
| Cuenta Twilio | WhatsApp Sandbox o número aprobado |
| Cuenta OpenAI | API key (IA + RAG) |
| Render (opcional) | despliegue en nube |

---

## 2. Clonar e instalar

```bash
git clone https://github.com/MantaVibers/CrediBot-Uleam.git
cd CrediBot-Uleam/creditbot
python -m venv .venv
```

**Windows (PowerShell):**

```powershell
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

**Linux / macOS:**

```bash
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## 3. Archivo `.env` completo

Crea o edita `creditbot/.env` con este contenido.
**Pega tus claves** donde dice `[TU_CLAVE_...]`.

```env
APP_NAME=CrediBot
APP_ENV=production
APP_DEBUG=true
APP_PUBLIC_URL=https://credibot-uleam.onrender.com

SUPABASE_URL=https://vhxpidjdbrpxtwztyuzf.supabase.co
SUPABASE_SERVICE_ROLE_KEY=[TU_CLAVE_SUPABASE_SERVICE_ROLE]

TWILIO_ACCOUNT_SID=[TU_TWILIO_ACCOUNT_SID]
TWILIO_AUTH_TOKEN=[TU_TWILIO_AUTH_TOKEN]
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
TWILIO_VALIDATE_SIGNATURE=true

DEFAULT_COUNTRY_CODE=593

ADMIN_DASHBOARD_PASSWORD=[TU_PASSWORD_PANEL_STREAMLIT]

OPENAI_API_KEY=[TU_OPENAI_API_KEY]
OPENAI_MODEL=gpt-4o-mini
OPENAI_ENABLE_AI=true
```

### Desarrollo local (alternativa)

Si pruebas en tu PC con `uvicorn --reload` y ngrok:

```env
APP_ENV=development
APP_PUBLIC_URL=http://localhost:8000
TWILIO_VALIDATE_SIGNATURE=false
```

### Dónde obtener cada clave

| Variable | Dónde copiarla |
|---|---|
| `SUPABASE_URL` | Supabase → Project Settings → API → Project URL |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase → Project Settings → API → `service_role` (secreta) |
| `TWILIO_ACCOUNT_SID` | Twilio Console → Account Info |
| `TWILIO_AUTH_TOKEN` | Twilio Console → Account Info |
| `TWILIO_WHATSAPP_FROM` | Twilio → Messaging → WhatsApp Sandbox (ej. `whatsapp:+14155238886`) |
| `OPENAI_API_KEY` | https://platform.openai.com/api-keys |
| `ADMIN_DASHBOARD_PASSWORD` | La defines tú (acceso al panel Streamlit) |

> **Nota:** Ya tienes un `.env` local funcional en `creditbot/.env`. Para rellenar esta guía
> rápido, abre ese archivo y copia las líneas de `SUPABASE_SERVICE_ROLE_KEY`, `TWILIO_*` y
> `OPENAI_API_KEY` en los placeholders de arriba.

---

## 4. Supabase (base de datos)

En **SQL Editor**, ejecutar **en este orden**:

1. `creditbot/supabase/schema.sql`
2. `creditbot/supabase/seed_credit_profiles.sql` (21 perfiles del buró simulado)
3. `creditbot/supabase/seed_rag_documents.sql` (chunks para RAG)

Luego, indexar embeddings RAG (requiere `OPENAI_API_KEY` en `.env`):

```bash
cd creditbot
python scripts/index_rag.py
```

Debe mostrar: `Listo. 5 chunks indexados.`

---

## 5. Ejecutar backend local

```bash
cd creditbot
uvicorn app.main:app --reload
```

| URL | Uso |
|---|---|
| http://localhost:8000/docs | Swagger / API |
| http://localhost:8000/health | Health check |
| POST http://localhost:8000/simulate/message | Simular chat sin Twilio |

**Ejemplo simulador:**

```bash
curl -X POST http://localhost:8000/simulate/message \
  -H "Content-Type: application/json" \
  -d "{\"phone\":\"593999999999\",\"message\":\"Hola\"}"
```

---

## 6. Panel Streamlit

```bash
cd creditbot
streamlit run dashboard/app.py
```

Usa `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY` y `ADMIN_DASHBOARD_PASSWORD` del `.env`.

Páginas: métricas, solicitudes, usuarios, casos derivados, **Auditoría IA**.

---

## 7. Twilio WhatsApp

1. Twilio Console → **Messaging** → **Try WhatsApp** (Sandbox) o número aprobado.
2. Une tu WhatsApp al sandbox (código que indica Twilio).
3. Webhook **When a message comes in**:

```text
https://credibot-uleam.onrender.com/webhook/whatsapp
```

Método: **POST**.

En local sin Render, usa ngrok:

```bash
ngrok http 8000
```

Webhook: `https://TU-ID.ngrok.io/webhook/whatsapp` y `APP_PUBLIC_URL` igual.

---

## 8. Render (producción)

| Campo | Valor |
|---|---|
| Repositorio | `MantaVibers/CrediBot-Uleam` |
| Rama | `develop` |
| Root Directory | `creditbot` |
| Build | `pip install -r requirements.txt` |
| Start | `uvicorn app.main:app --host 0.0.0.0 --port $PORT` |
| Auto-Deploy | On Commit |

Copia **todas** las variables del `.env` (sección 3) en Render → **Environment**.

Health check: `GET /health` → `{"status":"ok"}`.

Referencia adicional: `creditbot/docs/despliegue.md` y `creditbot/render.yaml`.

---

## 9. Pruebas

```bash
cd creditbot
pytest -v
```

Deben pasar **87 tests**. CI en GitHub Actions (rama `develop`).

---

## 10. Demo rápida WhatsApp

1. Escribe **Hola** → menú.
2. **1** → precalificar (prueba: *cinco mil*, *un año*, cédula `0912345675`).
3. **2** → modo IA (*¿Qué es score excelente?*).
4. **3** → derivar a asesor.

Cédula **sin perfil en buró** (ej. `0901023457`): el bot sigue el flujo y responde
*observado* con *sin historial crediticio registrado*.

---

## 11. Documentación del proyecto

| Archivo | Contenido |
|---|---|
| `creditbot/docs/ia_tools_rag.md` | Cálculos, tools, RAG, CI/CD |
| `creditbot/docs/bitacora_desarrollo.md` | Historial de desarrollo |
| `creditbot/docs/flujo_conversacional.md` | Estados del bot |
| `creditbot/docs/despliegue.md` | Render y variables |
| `informe_credibot_uleam.md` | Plantilla informe académico (si existe) |

---

## 12. Checklist final

- [ ] `.env` creado con todas las variables
- [ ] Supabase: schema + seeds + RAG indexado
- [ ] `pytest -v` en verde
- [ ] Render desplegado con `OPENAI_API_KEY`
- [ ] Webhook Twilio apuntando a `/webhook/whatsapp`
- [ ] Health check OK en producción

---

*Última actualización: julio 2026 — rama `develop`.*
