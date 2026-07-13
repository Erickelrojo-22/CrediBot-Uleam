# INFORME TÉCNICO — CrediBot-Uleam

> **Instrucciones para ChatGPT (generación del PDF)**  
> Convierte este documento en un **informe académico formal en PDF** (15–25 páginas aprox.).  
> - Idioma: **español**.  
> - Formato sugerido: márgenes 2.5 cm, fuente Arial o Calibri 11 pt, interlineado 1.5.  
> - Incluir **portada** con los datos de la sección 0 (completar campos marcados con `[COMPLETAR]`).  
> - Incluir **índice** automático, numeración de páginas y encabezados jerárquicos.  
> - Convertir los diagramas en texto (`text`) a **diagramas visuales** o cajas esquemáticas.  
> - Las tablas deben quedar bien formateadas.  
> - Al final, agregar **anexos** con capturas sugeridas (placeholders) que el equipo debe insertar.  
> - Tono: académico, claro, orientado a evaluación de proyecto de software.

---

## 0. Portada (completar antes del PDF)

| Campo | Valor |
|---|---|
| **Universidad** | [COMPLETAR: Universidad Laica Eloy Alfaro de Manabí — ULEAM] |
| **Facultad / Carrera** | [INGENIERIA EN SOFTWARE] |
| **Asignatura** | [MODELADO AGIL DEL SOFTWARE] |
| **Docente** | [ISRAEL GOMEZ] |
| **Proyecto** | CrediBot — Agente conversacional de precalificación crediticia por WhatsApp |
| **Equipo / Integrantes** | [ANDY GARCIA, ROBERT GARCIA, JORK LUCAS, ERICK MOREIRA, CARLOS ORTIZ] |
| **Repositorio GitHub** | https://github.com/MantaVibers/CrediBot-Uleam |
| **Rama de trabajo** | `develop` |
| **URL producción** | https://credibot-uleam.onrender.com |
| **Ciudad** | Manta, Ecuador |

---

## 1. Resumen ejecutivo

**CrediBot** es un agente conversacional desplegado en la nube que guía a usuarios por
WhatsApp para **precalificar** solicitudes de crédito de forma simulada (contexto académico).
El sistema combina:

- Un **motor de reglas deterministas** (Python puro) para scores, tasas, montos y cuotas.
- **Integración con OpenAI** para interpretar lenguaje natural y responder preguntas
  sobre políticas mediante **RAG** (Retrieval-Augmented Generation).
- Un **agente con function calling** que invoca tools auditables de negocio.
- Persistencia en **Supabase** (PostgreSQL), mensajería vía **Twilio WhatsApp**,
  despliegue en **Render** y **CI/CD** con GitHub Actions.

El resultado de precalificación puede ser **preaprobado**, **observado** o **no cumple**,
con monto máximo, cuota estimada y TEA referencial. Toda invocación de tools queda
registrada en `tool_audit_logs` con la cédula enmascarada.

**Estado del proyecto:** funcional en producción, **87 pruebas automatizadas en verde**,
pipeline CI activo en GitHub Actions, auto-deploy configurado en Render.

---

## 2. Introducción

### 2.1 Contexto

Las instituciones financieras utilizan procesos de evaluación crediticia que combinan
datos del solicitante, historial en burós y reglas de negocio. En entornos académicos
es necesario simular este flujo sin acceder a datos reales, manteniendo trazabilidad,
explicabilidad y buenas prácticas de ingeniería de software.

### 2.2 Problema

Se requiere un sistema conversacional accesible (WhatsApp) que:

1. Recoja datos del solicitante de forma guiada.
2. Valide identidad (cédula ecuatoriana).
3. Obtenga consentimiento antes de consultar un buró simulado.
4. Calcule una precalificación con reglas claras y reproducibles.
5. Integre inteligencia artificial de forma **controlada** (sin que el LLM invente montos).
6. Quede desplegado en la nube con integración y despliegue continuo.

### 2.3 Alcance

**Incluido:**

- Backend FastAPI con webhook Twilio WhatsApp.
- Buró simulado con 21 perfiles crediticios ficticios.
- Motor de crédito determinista.
- IA: normalización de texto, RAG, agente con tools.
- Panel administrativo Streamlit (métricas, solicitudes, auditoría IA).
- CI (GitHub Actions) y CD (Render).

**Excluido (demo académica):**

- Aprobación real de crédito.
- Integración con burós comerciales (Equifax, etc.).
- App móvil nativa.

---

## 3. Objetivos

### 3.1 Objetivo general

Desarrollar e implementar un agente conversacional de precalificación crediticia por
WhatsApp, desplegado en la nube, que integre reglas de negocio deterministas, tools
auditables, RAG documentado e IA conversacional.

### 3.2 Objetivos específicos

1. Diseñar e implementar un **motor de cálculo crediticio** determinista y testeable.
2. Implementar **tools del agente** con auditoría en base de datos (`tool_audit_logs`).
3. Configurar **RAG** sobre documento de política de crédito con embeddings e indexación.
4. Integrar **OpenAI** para normalización de lenguaje natural en todo el flujo.
5. Desplegar el sistema en **Render** con base de datos **Supabase**.
6. Configurar **CI/CD** con GitHub Actions (tests automáticos) y auto-deploy.
7. Documentar arquitectura, flujo y evidencias para evaluación académica.

---

## 4. Metodología de desarrollo

### 4.1 Enfoque

Desarrollo iterativo e incremental con:

- **Conventional Commits** en español.
- Rama de integración `develop` y rama estable `main`.
- Entregas por funcionalidad (schema → dominio → servicios → conversación → IA → DevOps).
- Pruebas automatizadas con **pytest** en cada commit relevante.

### 4.2 Herramientas de gestión

| Herramienta | Uso |
|---|---|
| Git / GitHub | Control de versiones y colaboración |
| GitHub Actions | Integración continua (CI) |
| Render | Despliegue continuo (CD) |
| Supabase SQL Editor | Migraciones y seeds |
| Twilio Console | Configuración webhook WhatsApp |

### 4.3 Cronología resumida de entregas

| Fase | Entregable | Evidencia |
|---|---|---|
| 1 | Esquema BD v2 + seed 21 perfiles | `supabase/schema.sql`, `seed_credit_profiles.sql` |
| 2 | Dominio: cédula + reglas crédito | `app/domain/` |
| 3 | Repositorios Supabase | `app/repositories/` |
| 4 | Servicio precalificación v2 | `precalificacion_service.py` |
| 5 | Flujo conversacional cédula/consentimiento | `conversation_service.py` |
| 6 | Auditoría tools | `audit_repository.py`, `tool_audit_logs` |
| 7 | CI/CD + Docker | `.github/workflows/ci.yml`, `Dockerfile` |
| 8 | Despliegue Render + fixes producción | `docs/despliegue.md` |
| 9 | OpenAI en todo el flujo | `ai_input_service.py` |
| 10 | RAG Supabase + indexación | `rag_service.py`, `scripts/index_rag.py` |
| 11 | Agente function calling | `agent_service.py` |
| 12 | Panel auditoría IA | `dashboard/pages/5_Auditoria_IA.py` |

---

## 5. Arquitectura del sistema

### 5.1 Diagrama de arquitectura en la nube

```text
WhatsApp (Twilio Sandbox)
        │ POST /webhook/whatsapp
        ▼
Render — FastAPI (rama develop)
        │
        ├── Supabase (PostgreSQL)
        │     ├── users, conversations, messages
        │     ├── credit_requests, credit_profiles
        │     ├── tool_audit_logs
        │     └── rag_documents, rag_chunks
        │
        ├── OpenAI API
        │     ├── Chat Completions (normalización, agente)
        │     └── Embeddings (RAG)
        │
        └── GitHub Actions (CI): pytest en cada push/PR
```

### 5.2 Arquitectura por capas (backend)

```text
Canal (WhatsApp / Simulador)
        │
        ▼
API (FastAPI)
  routes_webhook, routes_simulator, routes_admin, routes_health
        │
        ▼
Servicios
  conversation_service, precalificacion_service, ai_input_service,
  agent_service, rag_service, validation_service
        │
        ├─► Dominio (lógica pura)
        │     cedula_validator.py, credit_rules.py
        │
        └─► Repositorios (Supabase)
              user_repository, credit_repository, audit_repository,
              rag_repository, credit_profile_repository
```

### 5.3 Componentes y responsabilidades

| Componente | Tecnología | Rol |
|---|---|---|
| Backend API | FastAPI + Uvicorn | Webhook WhatsApp, simulador, health, admin |
| Base de datos | Supabase (PostgreSQL) | Persistencia, buró simulado, auditoría, RAG |
| Mensajería | Twilio WhatsApp | Canal conversacional |
| IA | OpenAI (`gpt-4o-mini`) | Normalización, RAG, agente con tools |
| CI | GitHub Actions | 87 tests en cada push/PR |
| CD | Render | Auto-deploy desde rama `develop` |
| Panel admin | Streamlit | Solicitudes, usuarios, auditoría IA |

### 5.4 Modelo de datos principal

Tablas relevantes (`supabase/schema.sql`):

| Tabla | Propósito |
|---|---|
| `users` | Usuario WhatsApp, cédula, consentimiento |
| `conversations` | Estado del flujo conversacional |
| `messages` | Historial inbound/outbound |
| `credit_requests` | Solicitudes con campos v2 (score, TEA, cuota, resultado) |
| `credit_profiles` | Buró simulado (21 perfiles ficticios) |
| `credit_history_events` | Eventos de historial por perfil |
| `handoff_cases` | Derivación a asesor humano |
| `tool_audit_logs` | Auditoría de invocaciones de tools |
| `rag_documents` / `rag_chunks` | Documentos y fragmentos para RAG |

---

## 6. Flujo conversacional

### 6.1 Estados del bot

El flujo se implementa como máquina de estados en `conversation_service.py`:

| Estado | Descripción |
|---|---|
| `START` / `MENU` | Bienvenida y menú principal (1=precalificar, 2=info IA, 3=asesor) |
| `ASK_NAME` | Solicita nombre |
| `ASK_CEDULA` | Solicita y valida cédula ecuatoriana |
| `CONSENT` | Solicita consentimiento para consultar buró |
| `ASK_AMOUNT` | Monto solicitado |
| `ASK_TERM` | Plazo en meses (3–36) |
| `ASK_INCOME` | Ingreso mensual neto |
| `CONFIRM_DATA` | Confirmación antes de evaluar |
| `EVALUATE_REQUEST` | Invoca precalificación |
| `SHOW_RESULT` | Muestra resultado al usuario |
| `INFO_AI` | Modo información con agente IA + RAG |
| `HANDOFF_REQUESTED` | Derivación a asesor |
| `FINISHED` | Conversación finalizada |

### 6.2 Menú principal

1. **Precalificar crédito** — flujo completo con cálculo determinista.
2. **Información con IA** — preguntas sobre políticas (RAG + agente).
3. **Hablar con un asesor** — deriva a humano.

### 6.3 Ejemplo de interacción (precalificación)

| Paso | Usuario | Bot interpreta / responde |
|---|---|---|
| Menú | `1` | Inicia precalificación |
| Nombre | `María López` | Valida y guarda |
| Cédula | `0912345675` | Valida módulo 10, busca perfil |
| Consentimiento | `sí, autorizo` | Normaliza a `1`, registra consentimiento |
| Monto | `cinco mil` | Normaliza a `5000` |
| Plazo | `un año` | Normaliza a `12` meses |
| Ingreso | `1200` | Valida y guarda |
| Confirmación | `sí` | Ejecuta `precalificar_por_cedula` |
| Resultado | — | Preaprobado / observado / no cumple + detalle |

---

## 7. Motor de cálculo crediticio (determinista)

> **Principio clave:** el LLM **nunca** calcula montos, tasas ni scores. Solo el dominio
> en `app/domain/credit_rules.py` realiza los cálculos.

### 7.1 Entradas

- Score y perfil del buró simulado (`credit_profiles`).
- Ingreso mensual neto del usuario.
- Plazo en meses (3–36).
- Monto solicitado (opcional).

### 7.2 Categorización de score (escala Ecuador 1–999)

| Categoría | Rango | TEA referencial | Multiplicador monto / ingreso |
|---|---|---|---|
| Excelente | 750–999 | 14.5% | 6.0× |
| Aceptable | 550–749 | 16.0% | 4.0× |
| Regular | 349–549 | 16.5% | 1.5× |
| Alto riesgo | 1–348 | — | No elegible |

### 7.3 Reglas de elegibilidad

No se precalifica si:

- Figura en **lista negra** simulada.
- Tiene **mora activa** > 30 días.
- Score en categoría **alto riesgo**.
- Sin historial (thin file) → se evalúa conservadoramente como **regular**.

### 7.4 Fórmulas

1. **Capacidad de pago** = 35% × ingreso neto − cuotas vigentes del buró.
2. **Cuota mensual** — amortización francesa:

   `cuota = monto × [ r(1+r)^n ] / [ (1+r)^n − 1 ]`  
   donde `r = TEA / 12` y `n = plazo en meses`.

3. **Monto máximo** = mínimo entre techo por categoría y monto sostenible por capacidad.
4. **Resultado:**
   - **Preaprobado:** cuota ≤ capacidad (categorías excelente/aceptable).
   - **Observado:** cuota ≤ 115% de capacidad, o categoría regular.
   - **No cumple:** resto de casos o no elegible.

### 7.5 Implementación y pruebas

| Archivo | Rol |
|---|---|
| `app/domain/credit_rules.py` | Motor puro de reglas |
| `app/services/precalificacion_service.py` | Orquestación + auditoría |
| `app/tests/test_credit_rules.py` | Tests unitarios del dominio |
| `app/tests/test_precalificacion_service.py` | Tests del servicio |

---

## 8. Tools del agente y auditoría

### 8.1 Concepto

Cada “tool” es una **función de negocio invocable** (por el flujo o por el agente IA).
Toda invocación se registra en `tool_audit_logs` con:

- `tool_name`, `input_payload`, `output_payload`
- `success`, `latency_ms`, `conversation_id`, `created_at`
- Cédula **enmascarada** (ej. `09******75`) — requisito RNF-04

### 8.2 Catálogo de tools

| Tool | Archivo | Cuándo se invoca |
|---|---|---|
| `precalificar_por_cedula` | `precalificacion_service.py` | Al confirmar datos en precalificación |
| `normalizar_entrada_usuario` | `ai_input_service.py` | Cada paso del flujo (monto, plazo, menú…) |
| `consultar_politica_credito` | `agent_service.py` / RAG | Preguntas sobre políticas |
| `validar_cedula` | `agent_service.py` | Validación de cédula vía agente |
| `explicar_reglas_credito` | `agent_service.py` | Explicación de reglas deterministas |
| `agente_openai_tools` | `agent_service.py` | Orquestación del agente (function calling) |

### 8.3 Agente OpenAI con function calling

En el modo **INFO_AI** (menú opción 2), el agente puede invocar:

1. `consultar_politica_credito(pregunta)` — recupera chunks RAG relevantes.
2. `validar_cedula(cedula)` — algoritmo módulo 10 ecuatoriano.
3. `explicar_reglas_credito(tema)` — devuelve categorías, tasas, capacidad, plazos.

El LLM **interpreta** la pregunta y **decide** qué tool usar; los **cálculos** siguen
siendo deterministas en el dominio.

### 8.4 Consulta de auditoría (SQL)

```sql
SELECT tool_name, success, latency_ms, input_payload, output_payload, created_at
FROM tool_audit_logs
ORDER BY created_at DESC
LIMIT 20;
```

También visible en el panel Streamlit → página **Auditoría IA**.

---

## 9. RAG — Retrieval-Augmented Generation

### 9.1 Objetivo

Responder preguntas sobre **políticas de crédito** usando contexto recuperado de un
documento curado, evitando que el modelo invente reglas.

### 9.2 Fuentes de conocimiento

1. **Documento local:** `creditbot/data/politica_credito.md`
2. **Supabase:** tablas `rag_documents` y `rag_chunks` (`seed_rag_documents.sql`)
3. **Indexación:** `scripts/index_rag.py` genera embeddings OpenAI (`text-embedding-3-small`, 1536 dimensiones)

### 9.3 Flujo RAG

```text
Pregunta del usuario
      │
      ▼
Embedding de la pregunta (OpenAI)
      │
      ▼
Búsqueda por similitud coseno sobre chunks
      (prioriza Supabase si hay embeddings; fallback documento local)
      │
      ▼
GPT recibe contexto + pregunta → respuesta en español
      │
      ▼
Registro en tool_audit_logs
```

### 9.4 Evidencia de indexación

Script ejecutado exitosamente:

```text
Indexado chunk ... (1536 dims)  × 5
Listo. 5 chunks indexados.
```

### 9.5 Archivos relevantes

| Archivo | Rol |
|---|---|
| `data/politica_credito.md` | Fuente de verdad de políticas |
| `supabase/seed_rag_documents.sql` | Seed de documento y chunks |
| `scripts/index_rag.py` | Generación de embeddings |
| `app/services/rag_service.py` | Recuperación por similitud |
| `app/repositories/rag_repository.py` | Lectura de chunks en Supabase |
| `app/services/agent_service.py` | Agente que consume RAG vía tools |

---

## 10. Integración de IA en el flujo conversacional

### 10.1 Normalización de lenguaje natural

Servicio: `app/services/ai_input_service.py`

| Entrada del usuario | Interpretación |
|---|---|
| `un año` | 12 meses |
| `cinco mil` | 5000 |
| `sí, autorizo` | 1 (consentimiento) |
| `precalificar` | opción 1 del menú |

Estrategia: reglas locales primero; OpenAI como respaldo si hay API key.

### 10.2 Separación de responsabilidades IA vs. negocio

| Capa | Responsabilidad |
|---|---|
| IA (OpenAI) | Interpretar texto, recuperar contexto, decidir tools |
| Dominio (`credit_rules`) | Calcular montos, cuotas, tasas, resultados |
| Auditoría | Registrar toda invocación de tool |

Esta separación garantiza **explicabilidad** y **reproducibilidad** exigidas en
contexto financiero académico.

---

## 11. CI/CD — Integración y despliegue continuo

### 11.1 CI — GitHub Actions

Archivo: `.github/workflows/ci.yml`

- **Trigger:** push y pull request a `main` y `develop`.
- **Pasos:** checkout → Python 3.12 → `pip install -r requirements.txt` → `pytest -v`.
- **Estado actual:** ✅ checks verdes en GitHub (evidencia: capturas de commits con ✓).

### 11.2 CD — Render

| Configuración | Valor |
|---|---|
| Repositorio | `MantaVibers/CrediBot-Uleam` |
| Rama | `develop` |
| Root Directory | `creditbot` |
| Auto-Deploy | On Commit |
| Health check | `GET /health` → `{"status":"ok"}` |
| URL | https://credibot-uleam.onrender.com |

### 11.3 Flujo completo DevOps

```text
git push origin develop
        │
        ▼
GitHub Actions (CI) ── pytest (87 tests)
        │
        ▼
Render (CD) ── redeploy automático
        │
        ▼
Producción: Supabase + Twilio + OpenAI
```

### 11.4 Contenerización

- `creditbot/Dockerfile` — imagen portable del backend.
- `creditbot/render.yaml` — blueprint con servicios `creditbot` y `creditbot-dashboard`.

---

## 12. Pruebas y calidad

### 12.1 Estrategia de pruebas

| Tipo | Herramienta | Alcance |
|---|---|---|
| Unitarias | pytest | Dominio, validadores, reglas de crédito |
| Servicios | pytest + mocks | Precalificación, IA, RAG, agente |
| Integración flujo | pytest + mocks | `conversation_service` end-to-end |
| Seed | pytest | Integridad de perfiles ficticios |

### 12.2 Métricas

- **Total tests:** 87
- **Estado:** todos en verde (local y CI)
- **Cobertura funcional:** dominio, flujo conversacional, webhook Twilio, auditoría, IA

### 12.3 Comando

```bash
cd creditbot
pytest -v
```

---

## 13. Despliegue y configuración

### 13.1 Variables de entorno (producción)

| Variable | Descripción |
|---|---|
| `SUPABASE_URL` | URL del proyecto Supabase |
| `SUPABASE_SERVICE_ROLE_KEY` | Clave server-side |
| `TWILIO_ACCOUNT_SID` | Account SID Twilio |
| `TWILIO_AUTH_TOKEN` | Auth Token Twilio |
| `TWILIO_WHATSAPP_FROM` | Número remitente WhatsApp |
| `TWILIO_VALIDATE_SIGNATURE` | `true` en producción |
| `APP_PUBLIC_URL` | URL pública del backend |
| `OPENAI_API_KEY` | Clave OpenAI (IA + RAG) |
| `OPENAI_MODEL` | `gpt-4o-mini` |
| `DEFAULT_COUNTRY_CODE` | `593` |

> El archivo `.env` **no se versiona** (contiene secretos).

### 13.2 Configuración Supabase (orden de ejecución)

1. `supabase/schema.sql`
2. `supabase/seed_credit_profiles.sql` (21 perfiles)
3. `supabase/seed_rag_documents.sql`
4. `python scripts/index_rag.py` (embeddings)

### 13.3 Webhook Twilio

```text
https://credibot-uleam.onrender.com/webhook/whatsapp
```

---

## 14. Panel administrativo (Streamlit)

Aplicación complementaria en `creditbot/dashboard/`:

| Página | Contenido |
|---|---|
| Solicitudes | Listado de precalificaciones v2 |
| Usuarios | Usuarios registrados |
| Casos derivados | Handoffs a asesor |
| **Auditoría IA** | Registros de `tool_audit_logs` |

Ejecución local:

```bash
cd creditbot
streamlit run dashboard/app.py
```

---

## 15. Resultados y evidencias

### 15.1 Checklist de cumplimiento (requisitos del docente)

| Requisito | Estado | Evidencia |
|---|---|---|
| Cálculos deterministas | ✅ Cumplido | `credit_rules.py`, tests, demo WhatsApp |
| Tools auditables | ✅ Cumplido | `tool_audit_logs`, 6 tools registradas |
| RAG documentado | ✅ Cumplido | `politica_credito.md`, seed, index, `ia_tools_rag.md` |
| GitHub | ✅ Cumplido | Repo público, historial de commits |
| CI/CD | ✅ Cumplido | Actions verde + Render auto-deploy |
| Funcionamiento en nube | ✅ Cumplido | URL producción + WhatsApp Sandbox |

### 15.2 Demo sugerida para evaluación (5–10 min)

1. Mostrar **GitHub Actions** en verde.
2. Abrir `https://credibot-uleam.onrender.com/health`.
3. **WhatsApp** — opción 1: precalificar con lenguaje natural.
4. **WhatsApp** — opción 2: preguntar sobre score o validar cédula.
5. **Panel Streamlit** — página Auditoría IA con registros recientes.
6. Explicar que los **cálculos no los hace el LLM**, sino el dominio.

### 15.3 Perfil de prueba recomendado

- **Cédula:** `0912345675`
- **Nombre buró:** María González López
- **Score:** 720 (categoría aceptable)

---

## 16. Conclusiones

1. Se logró implementar un agente conversacional funcional en WhatsApp con
   precalificación simulada y despliegue en la nube.
2. La separación entre **IA interpretativa** y **motor determinista** garantiza
   resultados explicables y auditables, alineados con buenas prácticas en sistemas
   financieros.
3. El sistema de **tools con auditoría** permite trazabilidad completa de cada
   decisión automatizada.
4. El **RAG** documentado sobre política de crédito evita alucinaciones del modelo
   en respuestas informativas.
5. La pipeline **CI/CD** (87 tests + auto-deploy) asegura calidad continua del software.

---

## 17. Trabajo futuro

1. Fusionar `develop → main` para rama de producción estable.
2. Desplegar panel Streamlit como servicio separado en Render (`creditbot-dashboard`).
3. Ampliar cobertura de tests E2E con OpenAI mockeado en staging.
4. Integrar pgvector nativo en Supabase para búsqueda vectorial server-side.
5. Internacionalización y soporte multi-idioma.

---

## 18. Referencias

1. Documentación FastAPI — https://fastapi.tiangolo.com/
2. Documentación Supabase — https://supabase.com/docs
3. Twilio WhatsApp API — https://www.twilio.com/docs/whatsapp
4. OpenAI API — https://platform.openai.com/docs
5. Render Docs — https://render.com/docs
6. GitHub Actions — https://docs.github.com/en/actions
7. Algoritmo validación cédula Ecuador (módulo 10) — normativa/registro civil EC
8. Documentación interna del proyecto:
   - `creditbot/docs/ia_tools_rag.md`
   - `creditbot/docs/bitacora_desarrollo.md`
   - `creditbot/docs/despliegue.md`
   - `creditbot/docs/flujo_conversacional.md`

---

## 19. Anexos (insertar capturas en el PDF)

### Anexo A — Capturas obligatorias

| # | Descripción | Archivo sugerido |
|---|---|---|
| A.1 | Portada del repositorio GitHub | Captura de pantalla |
| A.2 | GitHub Actions CI en verde | Captura de commits con ✓ |
| A.3 | Render — servicio activo y deploy exitoso | Captura dashboard Render |
| A.4 | Health check (`/health`) | Captura navegador o Postman |
| A.5 | Conversación WhatsApp — precalificación | Captura chat |
| A.6 | Conversación WhatsApp — modo IA (opción 2) | Captura chat |
| A.7 | Panel Streamlit — Auditoría IA | Captura con `tool_audit_logs` |
| A.8 | Supabase — tabla `tool_audit_logs` | Captura SQL Editor |
| A.9 | Supabase — `rag_chunks` con embeddings | Captura SQL Editor |
| A.10 | Diagrama de arquitectura | Generado desde sección 5 |

### Anexo B — Estructura del repositorio

```text
CrediBot-Uleam/
├── .github/workflows/ci.yml
├── creditbot/
│   ├── app/
│   │   ├── api/
│   │   ├── domain/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── tests/          (87 tests)
│   ├── dashboard/
│   ├── data/politica_credito.md
│   ├── docs/
│   ├── scripts/index_rag.py
│   ├── supabase/
│   ├── Dockerfile
│   └── render.yaml
└── informe_credibot_uleam.md   (este documento)
```

### Anexo C — Commits principales (referencia)

| Commit | Descripción |
|---|---|
| Schema v2 + seed perfiles | Base de datos y buró simulado |
| Dominio cédula + credit_rules | Motor determinista |
| Precalificación v2 + flujo | Integración conversacional |
| Auditoría tool_audit_logs | Trazabilidad |
| CI GitHub Actions + Docker | Integración continua |
| OpenAI en todo el flujo | Normalización IA |
| RAG Supabase + indexación | Embeddings y búsqueda |
| Agente function calling | Tools del agente |
| Panel Auditoría IA | Visualización Streamlit |

---

## 20. Prompt sugerido para ChatGPT (copiar y pegar)

```text
Genera un informe académico en PDF a partir del documento Markdown adjunto
(informe_credibot_uleam.md). Requisitos:

1. Portada formal ULEAM con los campos [COMPLETAR] que yo rellenaré.
2. Índice, numeración de páginas, márgenes 2.5 cm, Arial/Calibri 11 pt.
3. Convertir diagramas ASCII en figuras esquemáticas profesionales.
4. Mantener todas las tablas técnicas.
5. Secciones: Resumen, Introducción, Objetivos, Metodología, Arquitectura,
   Implementación (cálculos, tools, RAG, IA), CI/CD, Pruebas, Despliegue,
   Resultados, Conclusiones, Referencias, Anexos.
6. Tono académico en español, 15–25 páginas.
7. Dejar espacios marcados [INSERTAR CAPTURA] en los anexos.
8. Al final, incluir una tabla resumen de cumplimiento de requisitos del docente.
```

---

*Documento generado para el proyecto CrediBot-Uleam — julio 2026.*
