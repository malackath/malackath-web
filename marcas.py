"""Logos de la sección «Identidad de marca» del home. Único lugar para editarlos.

Cada logo: nombre (texto alternativo), imagen (ruta dentro de public/, ej. "img/marcas/mesaluma.svg";
None = recuadro provisorio) y url (opcional, link al caso o al sitio).
Para que se vean parejos conviene SVG o PNG con fondo transparente y en blanco o color claro.
PROVISORIO: Ber va a pasar los logos reales (pedido del 2026-11-24).
"""

FILA_1 = [{"nombre": f"Logo {i:02d}", "imagen": None, "url": None} for i in range(1, 7)]
FILA_2 = [{"nombre": f"Logo {i:02d}", "imagen": None, "url": None} for i in range(7, 13)]
