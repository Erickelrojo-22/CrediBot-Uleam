# CrediBot

Agente conversacional de precalificación de crédito por WhatsApp. Guía a cada
persona en un flujo controlado, solicita consentimiento antes de consultar su
perfil ficticio, aplica reglas crediticias deterministas y deriva los casos que
requieren atención humana.

La IA solo mejora la redacción de respuestas seguras: no decide score, elegibilidad,
tasas, montos ni transiciones de estado.

## Stack

- Python + FastAPI
- Supabase (persistencia, perfiles ficticios y auditoría)
- OpenAI (redacción conversacional opcional)
- Kapso (WhatsApp)
- Redis opcional (sesión activa)
- Streamlit (panel administrativo)

## Requisitos

- Python 3.11+
- Proyecto Supabase con `supabase/schema.sql` y `supabase/seed_credit_profiles.sql`
- Cuenta/proyecto Kapso con un número WhatsApp conectado
- API key de OpenAI solo si se desea activar la redacción con IA

## Instalación y ejecución

```bash
cd creditbot
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload
```

El servidor queda disponible en `http://localhost:8000`, con documentación en
`http://localhost:8000/docs`.

## Configuración

Completa `creditbot/.env` sin versionar secretos:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key

OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4
OPENAI_ENABLE_AI=true

WHATSAPP_PROVIDER=kapso
KAPSO_API_KEY=your-kapso-api-key
KAPSO_PHONE_NUMBER_ID=your-whatsapp-business-phone-number-id
KAPSO_WEBHOOK_SECRET=your-webhook-secret
KAPSO_VALIDATE_WEBHOOK_SIGNATURE=true

ADMIN_DASHBOARD_PASSWORD=your-admin-password
```

Guía de conexión: [`docs/kapso_setup.md`](docs/kapso_setup.md).

## Pruebas sin WhatsApp

```http
POST /simulate/message
Content-Type: application/json

{
  "phone": "593999999999",
  "message": "Hola"
}
```

El simulador permite validar el flujo completo sin enviar mensajes ni consumir
capacidad de Kapso.

## Panel Streamlit

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

El panel requiere Supabase, `BACKEND_API_URL` y `ADMIN_DASHBOARD_PASSWORD` para
que un asesor responda; las respuestas salen por el backend y Kapso.

## Pruebas automatizadas

```bash
pytest -q
```

## Documentación

- [`docs/flujo_conversacional.md`](docs/flujo_conversacional.md)
- [`docs/endpoints.md`](docs/endpoints.md)
- [`docs/kapso_setup.md`](docs/kapso_setup.md)
- [`docs/streamlit_dashboard.md`](docs/streamlit_dashboard.md)
- [`docs/despliegue.md`](docs/despliegue.md)

## Declaración de uso de IA

- OpenAI se usa únicamente para redactar respuestas conversacionales a partir de
  resultados seguros generados por el backend.
- La elegibilidad, tasas, cuotas y monto máximo se calculan en reglas Python.
- Todos los perfiles de crédito y cédulas son ficticios, para fines académicos.
