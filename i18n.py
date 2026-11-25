"""Sitio multilenguaje.

Las páginas en español (public/*.html, public/casos/*.html) son la fuente.
Este script las traduce con los diccionarios i18n/<idioma>.json
({"texto en español": "traducción"}) y escribe public/<idioma>/...

Uso:
  python3 i18n.py extraer   -> agrega a los .json las claves nuevas (vacías) y avisa
  python3 i18n.py generar   -> escribe public/en y public/pt (falla si falta alguna traducción)
"""
import html
import json
import re
import sys
from pathlib import Path

PUBLIC = Path("public")
DIR = Path("i18n")
IDIOMAS = {"es": "Español", "en": "English", "pt": "Português"}
TRADUCIDOS = ["en", "pt"]
PAGINAS = ["index.html", "trabajo.html", "casos-de-estudio.html", "estudio.html", "casos/arma-partido.html", "casos/pizcaya.html"]
ATRIBUTOS = ("alt", "data-alt", "placeholder", "aria-label", "title")
# textos dentro del <script> de cada página (no son nodos de texto)
JS = {
    "en": {"Abriendo tu correo...": "Opening your email...", "'Proyecto: '": "'Project: '"},
    "pt": {"Abriendo tu correo...": "Abrindo seu e-mail...", "'Proyecto: '": "'Projeto: '"},
}

TEXTO = re.compile(r"(<[^>]*>)([^<>]+)(?=<)")
BLOQUES = re.compile(r"(?s)(<script\b.*?</script>|<style\b.*?</style>)")


def norm(t):
    return " ".join(html.unescape(t).split())


def traducible(clave):
    return bool(re.search(r"[A-Za-zÁÉÍÓÚáéíóúÑñ]", clave))


def partes(s):
    """Divide en (es_codigo, trozo): no se traduce dentro de <script>/<style>."""
    out, i = [], 0
    for m in BLOQUES.finditer(s):
        out.append((False, s[i:m.start()]))
        out.append((True, m.group(0)))
        i = m.end()
    out.append((False, s[i:]))
    return out


def recorrer(s, fn):
    """Aplica fn(clave)->str|None a nodos de texto y atributos; devuelve el HTML nuevo."""
    def nodo(m):
        tag, crudo = m.group(1), m.group(2)
        if "material-symbols" in tag:
            return m.group(0)
        clave = norm(crudo)
        if not clave or not traducible(clave):
            return m.group(0)
        nuevo = fn(clave)
        if nuevo is None:
            return m.group(0)
        pre = crudo[:len(crudo) - len(crudo.lstrip())]
        pos = crudo[len(crudo.rstrip()):]
        return tag + pre + html.escape(nuevo, quote=False) + pos

    def atributo(m):
        nombre, valor = m.group(1), m.group(2)
        clave = norm(valor)
        if not clave or not traducible(clave):
            return m.group(0)
        nuevo = fn(clave)
        return m.group(0) if nuevo is None else f'{nombre}="{html.escape(nuevo)}"'

    def meta(m):
        clave = norm(m.group(2))
        nuevo = fn(clave)
        return m.group(0) if nuevo is None else m.group(1) + html.escape(nuevo) + m.group(3)

    res = []
    for codigo, trozo in partes(s):
        if codigo:
            res.append(trozo)
            continue
        trozo = TEXTO.sub(nodo, trozo)
        trozo = re.sub(r'\b(%s)="([^"]*)"' % "|".join(ATRIBUTOS), atributo, trozo)
        trozo = re.sub(r'(<meta name="description" content=")([^"]*)(")', meta, trozo)
        res.append(trozo)
    return "".join(res)


def claves_de_todo():
    vistas = []
    for p in PAGINAS:
        s = (PUBLIC / p).read_text(encoding="utf-8")
        recorrer(s, lambda c: vistas.append(c) or None)
    return list(dict.fromkeys(vistas))


def cargar(idioma):
    f = DIR / f"{idioma}.json"
    return json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}


def extraer():
    claves = claves_de_todo()
    DIR.mkdir(exist_ok=True)
    for idi in TRADUCIDOS:
        d = cargar(idi)
        nuevas = [c for c in claves if c not in d]
        for c in nuevas:
            d[c] = ""
        sobran = [c for c in d if c not in claves]
        (DIR / f"{idi}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"{idi}: {len(claves)} textos, {len(nuevas)} nuevos, {sum(1 for v in d.values() if not v)} sin traducir, {len(sobran)} que ya no se usan")


def selector(actual, pagina):
    """Links ES / EN / PT para el menú, apuntando a la misma página en cada idioma."""
    prof = pagina.count("/") + (0 if actual == "es" else 1)
    raiz = "../" * prof
    items = []
    for idi in IDIOMAS:
        href = raiz + ("" if idi == "es" else idi + "/") + pagina
        if idi == actual:
            items.append(f'<span class="text-primary-container" aria-current="true">{idi.upper()}</span>')
        else:
            items.append(f'<a class="text-on-surface-variant hover:text-primary transition-colors" href="{href}" '
                         f'hreflang="{idi}" lang="{idi}" title="{IDIOMAS[idi]}">{idi.upper()}</a>')
    sep = '<span class="text-on-surface-variant/40">/</span>'
    return ('<div class="flex items-center gap-space-xs font-label-md text-label-md uppercase tracking-wider" '
            'data-idioma>' + sep.join(items) + "</div>")


def alternos(pagina):
    prof = pagina.count("/")
    base = "https://malackath.com/"
    out = [f'<link rel="alternate" hreflang="{i}" href="{base}{"" if i == "es" else i + "/"}{pagina}"/>' for i in IDIOMAS]
    out.append(f'<link rel="alternate" hreflang="x-default" href="{base}{pagina}"/>')
    return "".join(out)


MARCA_SELECTOR = '<div class="flex items-center gap-space-md"><a class="'


def poner_selector(s, idi, pagina):
    if s.count(MARCA_SELECTOR) != 1:
        raise SystemExit(f"{pagina}: no encontré dónde va el selector de idioma")
    s = s.replace(MARCA_SELECTOR, MARCA_SELECTOR.replace('<a class="', selector(idi, pagina) + '<a class="'), 1)
    s = s.replace("</head>", alternos(pagina) + "</head>", 1)
    return s


def generar():
    for pagina in PAGINAS:
        ruta = PUBLIC / pagina
        es = ruta.read_text(encoding="utf-8")
        if 'data-idioma' not in es:
            ruta.write_text(poner_selector(es, "es", pagina), encoding="utf-8")
    faltan = {}
    for idi in TRADUCIDOS:
        d = cargar(idi)
        for pagina in PAGINAS:
            s = (PUBLIC / pagina).read_text(encoding="utf-8")
            s = re.sub(r'<div class="flex items-center gap-space-xs font-label-md[^"]*" data-idioma>.*?</div>', "", s, count=1, flags=re.S)
            s = re.sub(r'<link rel="alternate" hreflang[^>]*/>', "", s)

            def fn(c):
                v = d.get(c)
                if not v:
                    faltan.setdefault(idi, set()).add(c)
                    return None
                return v
            s = recorrer(s, fn)
            for a, b in JS[idi].items():
                s = s.replace(a, b)
            s = re.sub(r'(<html[^>]*\blang=")es"', rf'\g<1>{idi}"', s, count=1)
            # recursos compartidos: un nivel más arriba
            s = re.sub(r'((?:src|href)=")((?:\.\./)*)(img/|css/)', r'\1../\2\3', s)
            s = poner_selector(s, idi, pagina)
            out = PUBLIC / idi / pagina
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(s, encoding="utf-8")
        print(f"{idi}: {len(PAGINAS)} páginas")
    if faltan:
        for idi, cs in faltan.items():
            print(f"FALTAN {len(cs)} traducciones en {idi}:", *sorted(cs)[:15], sep="\n  ")
        sys.exit(1)


if __name__ == "__main__":
    {"extraer": extraer, "generar": generar}[sys.argv[1]]()
