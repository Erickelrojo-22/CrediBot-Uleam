# RAG semántico de políticas

CrediBot usa Supabase pgvector para recuperar secciones relevantes de las políticas. Si aún no hay embeddings indexados o el servicio no está disponible, conserva la búsqueda local como respaldo.

## Activación

1. Ejecuta el bloque RAG actualizado de `supabase/schema.sql` en el SQL Editor de Supabase.
2. Configura `OPENAI_API_KEY` y, opcionalmente, `OPENAI_EMBEDDING_MODEL=text-embedding-3-small`.
3. Desde la carpeta `creditbot`, ejecuta:

```powershell
python -m app.rag.ingest
```

El comando lee los documentos de `docs/policies`, genera embeddings y los guarda en `rag_chunks`.

## Mantenimiento

Después de cambiar una política Markdown, ejecuta nuevamente la ingesta. Las consultas del bot muestran la fuente de cada sección recuperada.
