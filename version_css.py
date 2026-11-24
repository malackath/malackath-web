"""Agrega ?v=<hash> al link de estilos.css en todas las páginas de public/.

Así el navegador nunca mezcla una página nueva con un CSS viejo guardado en caché
(pasó el 2026-11-24: el hero se veía amontonado en el navegador de Ber).
Corre al final de `npm run build`, después de compilar el CSS.
"""
import hashlib, pathlib, re

pub = pathlib.Path("public")
v = hashlib.sha256((pub / "css/estilos.css").read_bytes()).hexdigest()[:10]
n = 0
for f in pub.rglob("*.html"):
    s = f.read_text()
    t = re.sub(r'(href="(?:\.\./)*css/estilos\.css)(?:\?v=[0-9a-f]+)?"', rf'\1?v={v}"', s)
    if t != s:
        f.write_text(t); n += 1
print(f"estilos.css?v={v} en {n} páginas")
