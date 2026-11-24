"""Logos de la sección «Identidad de marca» del home. Único lugar para editarlos.

Cada logo va en una tarjeta como las de Proyectos destacados (pedido de Ber, 2026-11-24):
- nombre: texto alternativo del logo (no se muestra; el nombre ya está en el logo)
- imagen: ruta dentro de public/, ej. "img/marcas/mesaluma.svg" (None = recuadro provisorio)
- tipo: "App", "Empresa", etc. (va arriba de la descripción, en lima)
- descripcion: una línea, para quién se hizo el logo
- url: opcional, link al caso o al sitio
Si cambia un texto en español: python3 i18n.py extraer y completar i18n/en.json y pt.json.
PROVISORIO: Ber va a pasar los logos reales.
"""

_DESC = "Descripción breve: para quién se hizo este logo."

FILA_1 = [{"nombre": f"Logo {i:02d}", "imagen": None, "url": None,
           "tipo": "App" if i % 2 else "Empresa", "descripcion": _DESC} for i in range(1, 7)]
FILA_2 = [{"nombre": f"Logo {i:02d}", "imagen": None, "url": None,
           "tipo": "App" if i % 2 else "Empresa", "descripcion": _DESC} for i in range(7, 13)]
