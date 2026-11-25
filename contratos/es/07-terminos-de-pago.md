# Términos de pago

> Plantilla a revisar por un abogado y por el contador (IVA y facturación). Anexo común del Contrato marco, SOWs, Mantenimiento y Propuestas.

## 1. Moneda

Los precios se expresan en **{{moneda_nombre}} ({{moneda}})**, según la propuesta o el SOW (por defecto dólares estadounidenses; también pesos uruguayos o reales). Si se factura en otra moneda, se usa el tipo de cambio {{fuente_tipo_cambio}} del día anterior a la factura.

## 2. Impuestos

- Los precios **no incluyen {{impuesto_nombre}}**. Se suma {{impuesto_nombre}} {{impuesto_pct}} en la factura cuando corresponda.
- {{nota_impuestos}}
  *(Ejemplos que completa el generador según emisor y cliente: emisor en Uruguay con cliente uruguayo, IVA 22%; emisor en Uruguay con cliente del exterior, exportación de servicios sin IVA; emisor en Brasil, ISS u otro según municipio. Validar con el contador.)*
- Las retenciones o impuestos del país del Cliente corren por su cuenta. El Cliente paga el monto completo de la factura, sin descontar comisiones bancarias ni de transferencia.

## 3. Esquema de pago

| Tipo de trabajo | Cómo se paga |
|---|---|
| Proyecto a precio cerrado | {{anticipo_pct}}% al firmar, resto por hitos según el SOW. Los trabajos de menos de {{moneda}} {{monto_pago_unico}} se pagan {{pct_unico}}% al firmar. |
| Time & Materials | Factura mensual a mes vencido con detalle de horas. |
| Mantenimiento | Cuota por mes adelantado, del 1 al {{dia_vencimiento_cuota}} de cada mes. |
| Gastos de terceros | Por adelantado o con la factura siguiente, con comprobante. |

## 4. Vencimiento

Las facturas vencen a los **{{dias_vencimiento}} días** de emitidas. Medios de pago: {{medios_pago}} *(ej.: transferencia bancaria local, transferencia internacional, Mercado Pago, Stripe)*. Datos bancarios: en cada factura.

## 5. Atrasos

- Pasados {{dias_gracia}} días del vencimiento, se aplica un interés por mora de {{interes_mora}} mensual. *[El abogado debe confirmar el tope legal.]*
- Con más de {{dias_suspension}} días de atraso, Malackath puede pausar el trabajo y el mantenimiento, avisando antes. Los plazos se corren por el tiempo de la pausa.
- Los derechos sobre los entregables pasan al Cliente recién con el pago total (ver Contrato marco, cláusula 6).

## 6. Cancelación por el Cliente

Si el Cliente cancela un proyecto, paga el trabajo hecho hasta ese día (por horas registradas o por avance del hito) y los gastos comprometidos. El anticipo no se devuelve en la parte que cubra ese trabajo.
