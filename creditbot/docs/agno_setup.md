# Agno en CrediBot

Agno entiende texto libre y redacta reintentos naturales. La máquina de estados conserva el control de datos, montos, resultados y derivaciones.

Las tools auditables viven en `app/tools/credit_tools.py`. Los últimos mensajes de Supabase se usan como memoria acotada de la conversación. Si OpenAI o Agno no están disponibles, CrediBot responde con mensajes deterministas y el flujo continúa.
