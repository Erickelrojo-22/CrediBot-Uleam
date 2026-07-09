# Flujo conversacional de CrediBot

## Estados

| Estado | Descripción |
|---|---|
| `START` | Inicio de conversación |
| `MENU` | Menú principal |
| `ASK_NAME` | Solicita nombre |
| `ASK_AMOUNT` | Solicita monto |
| `ASK_TERM` | Solicita plazo |
| `ASK_INCOME` | Solicita ingreso |
| `CONFIRM_DATA` | Confirma resumen |
| `SHOW_RESULT` | Muestra resultado |
| `HANDOFF_REQUESTED` | Derivado a asesor |
| `FINISHED` | Conversación cerrada |

## Flujo esperado

```text
Usuario: Hola
Bot: Hola, soy CrediBot. ¿Qué deseas hacer?
     1. Precalificar crédito
     2. Información general
     3. Hablar con asesor

Usuario: 1
Bot: Perfecto. Indícame tu nombre completo.

Usuario: Carlos Ortiz
Bot: ¿Qué monto deseas solicitar?

Usuario: 500
Bot: ¿En cuántos meses deseas pagar el crédito?

Usuario: 12
Bot: ¿Cuál es tu ingreso mensual aproximado?

Usuario: 700
Bot: Resumen:
     Nombre: Carlos Ortiz
     Monto: $500.00
     Plazo: 12 meses
     Ingreso: $700.00
     ¿Confirmas la información?
     1. Sí
     2. No

Usuario: 1
Bot: Resultado: Preaprobado.
     Cuota estimada: $41.67
     Un asesor puede continuar con la validación final.
```

## Regla de negocio

```text
cuota_estimada = monto_solicitado / plazo
capacidad_pago = ingreso_mensual * 0.30
```

| Condición | Resultado |
|---|---|
| `cuota_estimada <= capacidad_pago` | `preaprobado` |
| `cuota_estimada <= capacidad_pago * 1.20` | `observado` |
| `cuota_estimada > capacidad_pago * 1.20` | `no_cumple` |

## Derivación a asesor

Se crea un caso en `handoff_cases` cuando:

- El usuario elige la opción 3 del menú
- Escribe palabras como `asesor`, `humano`, `persona` o `agente`
- El resultado queda como `observado`
- Falla 3 veces con datos inválidos

## Cómo probar el flujo

### Opción 1: simulador local

Usa `POST /simulate/message` cambiando el campo `message` en cada paso.

### Opción 2: Twilio WhatsApp Sandbox

1. Configura el webhook en Twilio Console.
2. Une tu número al Sandbox.
3. Escribe desde WhatsApp al número de prueba de Twilio.

Guía: [`twilio_setup.md`](twilio_setup.md)
