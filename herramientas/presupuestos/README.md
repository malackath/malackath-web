# Presupuestos y contratos (herramienta interna)

No se publica: está fuera de `public/`. Se abre con doble clic en `index.html` (Chrome o Safari).

- **Expedientes:** uno por cliente o proyecto. Se guardan en el navegador; el botón **Respaldo** baja todo en un `.json` y **Restaurar** lo vuelve a cargar (suma, no borra).
- **Pestañas:** propuesta, contrato marco, SOW, anexo T&M, mantenimiento, orden de cambio, términos de pago y NDA. Todos usan los mismos datos del expediente.
- **Campos:** todo se completa en cada documento (emisor, cliente, ID fiscal, domicilio, impuesto, ley, tarifas). Lo vacío se ve en amarillo y sale como línea en blanco en el PDF.
- **Ajustes:** perfiles de emisor (ej. Uruguay y Brasil), tarifas sugeridas, catálogo de servicios y numeración.
- **Pegar pedido:** pegá el mensaje que llega desde `malackath.com/presupuesto.html` (trae una línea `MLK1:`) y se crea el expediente.
- **Exportar PDF:** abre imprimir; elegí "Guardar como PDF". Las notas para el abogado salen solo si marcás la casilla.

Si cambia una plantilla en `contratos/`, correr:

```
cd malackath-web && python3 herramientas/presupuestos/armar.py
```
