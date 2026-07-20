# Configuración de WhatsApp con Kapso

CrediBot usa **Kapso** como proveedor único de WhatsApp. Kapso gestiona el número,
el envío de mensajes y la entrega de eventos al webhook del backend.

## Datos necesarios

En el dashboard de Kapso, copia los valores del proyecto y del número conectado:

| Variable | Origen |
|---|---|
| `KAPSO_API_KEY` | Integrations → API Keys |
| `KAPSO_PHONE_NUMBER_ID` | Número de WhatsApp conectado |
| `KAPSO_WEBHOOK_SECRET` | Secreto configurado al crear el webhook |

Configura en `creditbot/.env`:

```env
WHATSAPP_PROVIDER=kapso
KAPSO_API_KEY=...
KAPSO_PHONE_NUMBER_ID=...
KAPSO_WEBHOOK_SECRET=...
KAPSO_VALIDATE_WEBHOOK_SIGNATURE=true
KAPSO_GRAPH_API_VERSION=v24.0
```

No compartas estos valores en el repositorio ni en el chat.

## Registrar el webhook

1. Despliega el backend o expónlo temporalmente con un túnel HTTPS.
2. En Kapso, crea un webhook asociado al número de WhatsApp.
3. Usa la URL `https://tu-dominio.com/webhook/whatsapp`.
4. Suscribe únicamente el evento `whatsapp.message.received`.
5. Define y guarda el mismo secreto en `KAPSO_WEBHOOK_SECRET`.

Kapso firma el cuerpo de cada evento con `X-Webhook-Signature`; CrediBot valida
esa firma antes de procesar el mensaje. El backend también admite entregas agrupadas
del evento, aunque para la demostración se recomienda no activar buffering.

## Comprobación

1. Consulta `GET /health/whatsapp`: debe indicar `provider: kapso` y `configured: true`.
2. Envía `Hola` al número conectado en Kapso.
3. Verifica que CrediBot responda y que el turno quede en Supabase.
4. Solicita un asesor y responde desde el panel Streamlit; el panel llama al backend,
   que envía el mensaje por Kapso y lo registra en el historial.

## Errores frecuentes

| Problema | Acción |
|---|---|
| `configured: false` | Completa las variables indicadas por `missing_env`. |
| Respuesta 403 del webhook | Revisa que el secreto de Kapso y `KAPSO_WEBHOOK_SECRET` coincidan. |
| No llegan eventos | Confirma la URL HTTPS, el evento suscrito y que el servicio esté activo. |
| No se envía una respuesta | Revisa `KAPSO_API_KEY`, `KAPSO_PHONE_NUMBER_ID` y los logs del backend. |
