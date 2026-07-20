# Panel administrativo Streamlit

El panel permite revisar métricas, solicitudes, perfiles, auditoría y casos derivados.
La atención humana se gestiona desde el panel, pero el envío de WhatsApp siempre pasa
por el backend FastAPI configurado con Kapso; por eso la clave de Kapso no se guarda
en el servicio Streamlit.

## Variables requeridas

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
ADMIN_DASHBOARD_PASSWORD=your-admin-password
BACKEND_API_URL=https://tu-backend.com
```

`ADMIN_DASHBOARD_PASSWORD` debe ser idéntica en el backend y el panel.

## Ejecución local

Desde `creditbot`:

```bash
pip install -r dashboard/requirements.txt
streamlit run dashboard/app.py
```

## Despliegue

El panel se publica como servicio separado del backend:

| Campo | Valor |
|---|---|
| Directorio raíz | `creditbot` |
| Comando de construcción | `pip install -r dashboard/requirements.txt` |
| Comando de inicio | `streamlit run dashboard/app.py --server.port=$PORT --server.address=0.0.0.0 --server.headless=true` |
| Health check | `/_stcore/health` |

## Atención humana

1. Abre **Casos derivados** y selecciona un caso.
2. Escribe la respuesta del asesor.
3. El panel llama a `POST /admin/handoff/{case_id}/reply`.
4. El backend envía el mensaje por Kapso, registra el historial y asigna el caso.

Si el panel no permite enviar, verifica `BACKEND_API_URL`, la contraseña y
`GET /health/whatsapp` en el backend.
