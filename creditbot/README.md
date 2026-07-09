# CrediBot

Agente conversacional de precalificación de crédito por WhatsApp.

**Stack:** Python, FastAPI, Supabase, WhatsApp Cloud API.

## Estructura del proyecto

```text
creditbot/
├── app/
│   ├── main.py
│   ├── core/
│   ├── api/
│   ├── schemas/
│   ├── services/
│   ├── repositories/
│   └── tests/
├── docs/
├── supabase/
├── requirements.txt
└── .env.example
```

## Instalación

```bash
cd creditbot
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

## Ejecución

```bash
uvicorn app.main:app --reload
```
