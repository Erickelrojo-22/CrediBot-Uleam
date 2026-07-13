# Meta WhatsApp Cloud API — flujo real (Fase A)

CrediBot usa **Meta Cloud API** como canal WhatsApp del flujo real
(consentimiento → cédula → score → precalificación → handoff).

La Fase A ejecuta el **mismo flujo de negocio** que producción. La diferencia
con Fase B (número público) es solo el alcance de destinatarios y la verificación
empresarial de Meta.

## Qué necesitas

1. Cuenta en [Meta for Developers](https://developers.facebook.com)
2. App tipo **Business** con producto **WhatsApp**
3. Número de prueba que Meta asigna (o número propio si ya tienes Fase B)
4. Hasta **5 números** en la lista de destinatarios de prueba (equipo + profesor)
5. Backend en Render: `https://credibot-uleam-gjj2.onrender.com`

## Pasos en Meta

1. Crea la app → agrega **WhatsApp** → **API Setup**
2. Copia:
   - **Temporary access token** (o System User token si ya tienes)
   - **Phone number ID**
3. En **To**, agrega y verifica los celulares del equipo
4. En **Configuration → Webhooks**:
   - Callback URL: `https://credibot-uleam-gjj2.onrender.com/webhook/whatsapp`
   - Verify token: el mismo valor que pondrás en `META_WHATSAPP_VERIFY_TOKEN`
   - Suscribe el campo `messages`

## Variables en Render (backend)

| Variable | Valor |
|---|---|
| `WHATSAPP_PROVIDER` | `meta` |
| `META_WHATSAPP_TOKEN` | token de acceso |
| `META_WHATSAPP_PHONE_NUMBER_ID` | Phone number ID |
| `META_WHATSAPP_VERIFY_TOKEN` | string secreto que inventes |
| `META_WHATSAPP_APP_SECRET` | opcional (firma `X-Hub-Signature-256`) |
| `APP_PUBLIC_URL` | `https://credibot-uleam-gjj2.onrender.com` |
| `ADMIN_DASHBOARD_PASSWORD` | misma clave del panel Streamlit |

Verifica:

```text
GET https://credibot-uleam-gjj2.onrender.com/health/whatsapp
```

Debe responder `"provider": "meta"` y `"configured": true`.

## Panel Streamlit (asesor)

| Variable | Valor |
|---|---|
| `BACKEND_API_URL` | `https://credibot-uleam-gjj2.onrender.com` |
| `ADMIN_DASHBOARD_PASSWORD` | igual que en el backend |
| `SUPABASE_URL` / `SUPABASE_SERVICE_ROLE_KEY` | las de siempre |

El asesor responde en **Casos derivados** → el panel llama
`POST /admin/handoff/{id}/reply` → el backend envía por Meta.

## Fase B (número abierto al público)

Solo cuando Meta Business esté verificado y tengas número propio + token permanente.
El código no cambia: solo las credenciales y el alcance de destinatarios.

## Prueba rápida

1. Desde un celular whitelisted, escribe al número WhatsApp de la app Meta
2. Completa el menú (`1` precalificar…)
3. Pide asesor (`3` o “hablar con asesor”)
4. En Streamlit, abre el caso y responde
5. Confirma que el mensaje llega al WhatsApp del cliente
