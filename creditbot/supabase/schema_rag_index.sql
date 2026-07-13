-- Índice ivfflat para búsqueda semántica en RAG (opcional, ejecutar cuando RAG esté activo).
--
-- Requisitos:
-- 1. Haber ejecutado schema.sql (tablas rag_documents y rag_chunks).
-- 2. Tener filas en rag_chunks con embeddings (ivfflat falla o es inútil en tabla vacía).
-- 3. Si falla por memoria en SQL Editor, ejecutar desde psql o Supabase CLI con:
--    SET maintenance_work_mem = '128MB';
--
-- En plan gratuito de Supabase, si sigue fallando, omitir este índice hasta usar RAG en producción.

create index if not exists rag_chunks_embedding_idx
    on rag_chunks using ivfflat (embedding vector_cosine_ops) with (lists = 100);
