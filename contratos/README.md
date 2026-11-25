# Contratos y documentos comerciales de Malackath

> **Plantillas. No son asesoramiento legal.** Antes de usarlas con un cliente, que las revise un abogado en Uruguay (y uno local si el cliente está en Brasil u otro país). Lo de IVA y facturación lo valida el contador.

Esta carpeta no se publica en el sitio (está fuera de `public/`).

## Cómo se usan juntos

```
Pedido del cliente (formulario web o charla)
   └─ 1. Propuesta comercial ........ qué, cuánto, cuándo (no obliga)
        └─ 2. Contrato marco (MSA) ... se firma una sola vez por cliente
             ├─ 3. SOW (alcance) ..... uno por proyecto
             │    ├─ Anexo A: Time & Materials (si se cobra por hora)
             │    └─ Órdenes de cambio (cada cambio de alcance)
             └─ 4. Mantenimiento mensual (uno por cliente o por producto)
   NDA ............................... antes de la propuesta, si el cliente lo pide
   Términos de pago .................. anexo común a todos
```

| # | Archivo | Para qué |
|---|---------|----------|
| 1 | `es/01-propuesta.md` | Presupuesto con alcance, precio y plazos. Vence a los {{validez_dias}} días. |
| 2 | `es/02-contrato-marco.md` | Reglas generales: propiedad intelectual, confidencialidad, responsabilidad, rescisión, jurisdicción. |
| 3 | `es/03-sow.md` | Alcance de un proyecto: entregables, hitos, aceptación, precio (fijo o T&M). |
| 4 | `es/04-anexo-time-and-materials.md` | Tarifas por hora, registro de horas, tope, facturación mensual. |
| 5 | `es/05-mantenimiento.md` | Cuota mensual con horas incluidas, tiempos de respuesta, qué entra y qué no. |
| 6 | `es/06-orden-de-cambio.md` | Cambio de alcance, precio o plazo, firmado por las dos partes. |
| 7 | `es/07-terminos-de-pago.md` | Moneda, IVA, vencimientos, mora, gastos de terceros. |
| 8 | `es/08-nda.md` | Acuerdo de confidencialidad mutuo. |

## Campos

Todo lo que va entre `{{dobles_llaves}}` se completa por cliente. Los datos de Malackath (razón social, RUT, domicilio, tarifas) **no están cargados todavía**: ver `datos-malackath.md`.

## Idiomas

`es/` es la fuente. `en/` y `pt/` son traducciones a revisar (en Brasil, el abogado local debería mirar la versión en portugués).
