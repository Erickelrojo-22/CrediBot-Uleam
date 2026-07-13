# Política de precalificación CrediBot (fines académicos)

CrediBot es un asistente de **precalificación**, no una aprobación final de crédito.
Los montos, cuotas y tasas son referenciales y un asesor humano valida el caso.

## Score crediticio (escala Ecuador 1–999)

- **Excelente (750–999):** mejor perfil; TEA referencial ~14.5%; monto hasta ~6× ingreso mensual.
- **Aceptable (550–749):** perfil viable con condiciones moderadas; TEA ~16%; monto hasta ~4× ingreso.
- **Regular (349–549):** mayor riesgo; TEA ~16.5%; monto conservador hasta ~1.5× ingreso.
- **Alto riesgo (1–348):** no cumple condiciones básicas de precalificación automática.

## Elegibilidad

No se precalifica automáticamente si:

- Figura en **lista negra** simulada.
- Tiene **mora activa** mayor a 30 días.
- El score cae en categoría **alto riesgo**.

Sin historial crediticio suficiente (thin file) se evalúa de forma conservadora como regular.

## Capacidad de pago

Se considera que hasta el **35% del ingreso neto mensual** puede destinarse al pago del crédito,
descontando cuotas vigentes reportadas en el buró simulado.

## Plazos

Los plazos válidos para precalificar van de **3 a 36 meses**.

## Consentimiento

Antes de consultar el historial crediticio simulado, el usuario debe autorizar expresamente
la consulta (datos ficticios del curso).

## Resultados posibles

- **Preaprobado:** cumple reglas y la cuota estimada cabe en la capacidad de pago.
- **Observado:** perfil cercano al límite; requiere revisión de un asesor.
- **No cumple:** no supera elegibilidad o la cuota excede la capacidad.

## Datos de prueba

El buró simulado incluye 21 perfiles ficticios con cédulas válidas (algoritmo módulo 10).
Ejemplo: cédula `0912345675` — María González López, score 720, categoría aceptable.
