#!/usr/bin/env python3
"""Empaqueta las plantillas de contratos/<idioma>/*.md en plantillas.js para el generador.

Correr después de cambiar cualquier plantilla:
    python3 herramientas/presupuestos/armar.py
"""
import json
import pathlib

RAIZ = pathlib.Path(__file__).resolve().parents[2]
CONTRATOS = RAIZ / "contratos"
SALIDA = pathlib.Path(__file__).resolve().parent / "plantillas.js"

# clave del documento -> número de archivo
DOCS = {
    "propuesta": "01",
    "marco": "02",
    "sow": "03",
    "tm": "04",
    "mantenimiento": "05",
    "cambio": "06",
    "pagos": "07",
    "nda": "08",
}


def main():
    datos = {}
    for idioma_dir in sorted(p for p in CONTRATOS.iterdir() if p.is_dir()):
        idioma = idioma_dir.name
        for clave, num in DOCS.items():
            archivos = sorted(idioma_dir.glob(f"{num}-*.md"))
            if archivos:
                datos.setdefault(idioma, {})[clave] = archivos[0].read_text(encoding="utf-8")
    SALIDA.write_text(
        "// Generado por armar.py desde contratos/. No editar a mano.\n"
        "window.PLANTILLAS = " + json.dumps(datos, ensure_ascii=False, indent=1) + ";\n",
        encoding="utf-8",
    )
    for idioma, docs in datos.items():
        print(f"{idioma}: {len(docs)} plantillas")


if __name__ == "__main__":
    main()
