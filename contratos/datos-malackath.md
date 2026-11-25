# Datos que se completan en cada documento

Nada de esto queda fijo en las plantillas: todo es un campo que Ber completa (o elige de un perfil guardado) en el generador. No inventar datos.

## Emisor (quien factura)
Puede variar según el país y la empresa que firme. El generador guarda **perfiles de emisor** que se eligen y se pueden editar en cada documento.

| Campo | Ejemplos | Nota |
|---|---|---|
| `{{prestador_razon_social}}` | | por perfil |
| `{{prestador_nombre_fantasia}}` | Malackath | |
| `{{prestador_id_fiscal_tipo}}` | RUT (Uruguay), CNPJ o CPF (Brasil), EIN (EE. UU.) | |
| `{{prestador_id_fiscal}}` | | |
| `{{prestador_domicilio}}` | | |
| `{{prestador_representante}}` | | |
| `{{prestador_email}}`, `{{prestador_whatsapp}}` | hola@malackath.com, +598 94 202 607 | los de la web |

## Cliente
Mismos campos con `cliente_` (tipo de identificación fiscal según su país).

## Impuestos, ley y jurisdicción
| Campo | Por defecto (emisor en Uruguay) | Editable |
|---|---|---|
| `{{impuesto_nombre}}` / `{{impuesto_pct}}` | IVA 22% a clientes de Uruguay; 0% exportación de servicios a clientes del exterior | sí (ej.: ISS en Brasil); validar con contador |
| `{{ley_aplicable}}` / `{{jurisdiccion}}` | Uruguay / Montevideo | sí |
| `{{ley_datos_personales}}` | Ley N.º 18.331 | sí (LGPD en Brasil) |

## Moneda y tarifas
- Moneda por documento: US$ por defecto, $U o R$ (decisión de Ber 2026-11-25).
- Roles y tarifas por hora: el generador guarda valores sugeridos y se cambian en cada propuesta.
- Mantenimiento: cuota y horas incluidas por contrato (horas no acumulables, decisión de Ber 2026-11-25).
