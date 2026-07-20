# Endpoints de CrediBot

## Salud

| Método | Ruta | Uso |
|---|---|---|
| `GET` | `/health` | Estado general del backend. |
| `GET` | `/health/ai` | Estado de la capa de IA sin exponer la clave. |
| `GET` | `/health/whatsapp` | Estado de Kapso y variables faltantes sin exponer secretos. |

`/health/whatsapp` devuelve, entre otros, `provider: "kapso"`, `configured`,
`missing_env` y `webhook_path`.

## Simulador local

### `POST /simulate/message`

Prueba el flujo sin enviar mensajes de WhatsApp.

```json
{
  "phone": "593999999999",
  "message": "Hola"
}
```

## Webhook de Kapso

### `GET /webhook/whatsapp`

Indica que la ruta está lista para ser registrada en Kapso.

### `POST /webhook/whatsapp`

Recibe el evento nativo `whatsapp.message.received` de Kapso. Debe incluir:

- `Content-Type: application/json`
- `X-Webhook-Event: whatsapp.message.received`
- `X-Webhook-Signature`: HMAC SHA-256 del cuerpo con `KAPSO_WEBHOOK_SECRET`

El endpoint acepta mensajes de texto individuales y lotes de Kapso. Los demás eventos
se reconocen y se ignoran sin afectar la conversación.

## Administración

Las rutas administrativas requieren el encabezado
`X-Admin-Password: <ADMIN_DASHBOARD_PASSWORD>`.

| Método | Ruta | Uso |
|---|---|---|
| `GET` | `/admin/requests` | Solicitudes de crédito. |
| `GET` | `/admin/handoff` | Casos abiertos de asesoría. |
| `POST` | `/admin/handoff/{case_id}/reply` | Envía la respuesta del asesor mediante Kapso. |
| `POST` | `/admin/handoff/{case_id}/close` | Cierra el caso. |
| `GET` | `/admin/conversations/{phone}` | Usuario, conversación e historial. |

Con el servidor levantado, la documentación interactiva está disponible en
`/docs` y `/redoc`.
