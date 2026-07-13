"""Punto de entrada de la aplicación FastAPI."""
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from app.api.routes_admin import router as admin_router
from app.api.routes_health import router as health_router
from app.api.routes_simulator import router as simulator_router
from app.api.routes_webhook import router as webhook_router

app = FastAPI(title="CrediBot", version="0.1.0")


@app.get("/", response_class=HTMLResponse)
def root():
    """Pantalla inicial simple para abrir la URL pública del backend."""
    return """
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>CrediBot</title>
        <style>
          body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f6f7f9;
            color: #17202a;
          }
          main {
            max-width: 860px;
            margin: 0 auto;
            padding: 48px 20px;
          }
          h1 {
            margin-bottom: 8px;
            font-size: 36px;
          }
          p {
            line-height: 1.5;
            color: #46515f;
          }
          .panel {
            background: white;
            border: 1px solid #d9dee7;
            border-radius: 8px;
            padding: 22px;
            margin-top: 24px;
          }
          a {
            display: inline-block;
            margin: 8px 8px 0 0;
            padding: 10px 14px;
            border-radius: 6px;
            background: #1463ff;
            color: white;
            text-decoration: none;
          }
          code {
            background: #eef1f6;
            padding: 2px 5px;
            border-radius: 4px;
          }
        </style>
      </head>
      <body>
        <main>
          <h1>CrediBot</h1>
          <p>
            Backend FastAPI para el agente conversacional de precalificación de crédito
            por WhatsApp. El bot combina flujo guiado, reglas de negocio, IA, RAG,
            registro de conversaciones y derivación a asesor humano.
          </p>
          <section class="panel">
            <h2>Estado del servicio</h2>
            <p>Usa estos accesos para probar o revisar la API desplegada.</p>
            <a href="/health">Health</a>
            <a href="/health/ai">Estado IA</a>
            <a href="/docs">Swagger</a>
            <a href="/webhook/whatsapp">Webhook WhatsApp</a>
          </section>
          <section class="panel">
            <h2>Simulador</h2>
            <p>
              Para probar el bot sin gastar mensajes de WhatsApp, usa
              <code>POST /simulate/message</code> desde Swagger.
            </p>
          </section>
        </main>
      </body>
    </html>
    """

# Registro de routers
app.include_router(health_router)
app.include_router(simulator_router)
app.include_router(webhook_router)
app.include_router(admin_router)
