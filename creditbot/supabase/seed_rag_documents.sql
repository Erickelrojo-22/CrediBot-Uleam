-- Seed de documentos RAG para CrediBot (política de crédito académica)
-- Ejecutar DESPUÉS de schema.sql
-- Idempotente: ON CONFLICT DO NOTHING donde aplica

insert into rag_documents (id, title, source_path)
values (
    'a1111111-1111-1111-1111-111111111111',
    'Política de precalificación CrediBot',
    'creditbot/data/politica_credito.md'
)
on conflict (id) do nothing;

-- Chunks de texto (embeddings NULL hasta ejecutar scripts/index_rag.py)
insert into rag_chunks (document_id, content, metadata)
select 'a1111111-1111-1111-1111-111111111111', chunk.content, chunk.metadata
from (values
    (
        'CrediBot es precalificación, no aprobación final. Montos, cuotas y tasas son referenciales.',
        '{"section":"intro"}'::jsonb
    ),
    (
        'Score excelente 750-999: TEA ~14.5%, monto hasta ~6x ingreso. Aceptable 550-749: TEA ~16%, hasta ~4x. Regular 349-549: TEA ~16.5%, hasta ~1.5x. Alto riesgo 1-348: no cumple automático.',
        '{"section":"score"}'::jsonb
    ),
    (
        'No se precalifica con lista negra, mora mayor a 30 días o categoría alto riesgo. Sin historial (thin file) se evalúa conservador como regular.',
        '{"section":"elegibilidad"}'::jsonb
    ),
    (
        'Capacidad de pago: hasta 35% del ingreso neto mensual menos cuotas vigentes del buró simulado. Plazos válidos: 3 a 36 meses.',
        '{"section":"capacidad"}'::jsonb
    ),
    (
        'Resultados: preaprobado si la cuota cabe en capacidad; observado si está hasta 115% de la capacidad; no cumple en otros casos. Requiere consentimiento antes de consultar buró simulado.',
        '{"section":"resultados"}'::jsonb
    )
) as chunk(content, metadata)
where not exists (
    select 1 from rag_chunks rc
    where rc.document_id = 'a1111111-1111-1111-1111-111111111111'
      and rc.content = chunk.content
);
