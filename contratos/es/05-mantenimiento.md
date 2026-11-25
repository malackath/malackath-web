# Contrato de mantenimiento mensual

> Plantilla a revisar por un abogado. Forma parte del Contrato marco N.º {{contrato_numero}}.
> **Modelo de cobro:** cuota fija con horas incluidas por mes, no acumulables; horas extra a tarifa (decidido por Ber, 2026-11-25).

**Cliente:** {{cliente_razon_social}} · **Producto cubierto:** {{producto}} *(sitio, app, tienda; con URL)* · **Plan:** {{plan_nombre}} · **Inicio:** {{fecha_inicio}}

## 1. Qué cubre

**Incluido en la cuota:**
- Monitoreo de que el sitio o la app estén en línea y alertas de caída.
- Actualizaciones de seguridad y de dependencias del software.
- Respaldo {{frecuencia_respaldo}} y prueba de restauración {{frecuencia_prueba_respaldo}}.
- Renovación y control de dominio, certificados y servicios contratados a nombre del Cliente (los costos de esos servicios los paga el Cliente).
- **{{horas_incluidas}} horas por mes** para cambios chicos: textos, fotos, precios, ajustes de diseño, correcciones, pequeñas mejoras.
- Informe mensual con lo hecho y las horas usadas.

**No incluido** (se cotiza aparte o por horas):
- Funciones o pantallas nuevas, rediseños, integraciones nuevas.
- Problemas causados por cambios hechos por terceros o por el Cliente.
- Costos de hosting, dominio, licencias, tiendas de apps, anuncios.
- Recuperación ante ataques o pérdida de datos originados fuera del control de Malackath, salvo restaurar el último respaldo.

## 2. Horas

- Las horas incluidas **no se acumulan** de un mes a otro.
- Las horas extra se cobran a la tarifa del Anexo A{{descuento_horas_extra_texto}}, previo aviso al Cliente cuando el pedido las vaya a superar.

## 3. Tiempos de respuesta

Horario de atención: {{horario_atencion}} ({{zona_horaria}}), días hábiles de {{pais_dias_habiles}}.

| Prioridad | Ejemplo | Primera respuesta | Objetivo de solución |
|---|---|---|---|
| Crítica | sitio o app caídos, pagos que no funcionan | {{respuesta_critica}} | {{solucion_critica}} |
| Alta | una función importante falla | {{respuesta_alta}} | {{solucion_alta}} |
| Normal | cambios de contenido, ajustes | {{respuesta_normal}} | dentro del mes |

Los tiempos son objetivos de servicio, no garantías de resultado. Dependen también de los proveedores de infraestructura (Firebase, Cloudflare, Shopify, tiendas de apps).

**Canal de pedidos:** {{canal_pedidos}} *(ej.: email a {{prestador_email}}; las críticas también por WhatsApp)*.

## 4. Precio

**Cuota mensual:** {{moneda}} {{cuota_mensual}} {{iva_texto}}, facturada por mes adelantado. Pago según Términos de Pago.

Malackath puede ajustar la cuota una vez por año avisando con 30 días. El Cliente puede rescindir sin costo si no acepta el ajuste.

## 5. Plazo

Plazo mínimo de {{meses_minimos}} meses; después se renueva sola mes a mes. Cualquier parte puede terminarlo con {{dias_preaviso_mantenimiento}} días de aviso escrito. Al terminar, Malackath entrega accesos, código y último respaldo dentro de {{dias_entrega_final}} días hábiles.

## 6. Accesos

El Cliente es dueño de sus cuentas (dominio, hosting, tiendas de apps, Shopify) y le da a Malackath acceso como colaborador. Malackath no guarda contraseñas del Cliente fuera de un gestor seguro y las devuelve o las borra al terminar.

## Firmas

| Por Malackath | Por el Cliente |
|---|---|
| {{prestador_representante}} | {{cliente_representante}} |
| Firma / fecha: | Firma / fecha: |
