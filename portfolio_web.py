"""Contenido del portfolio (portfolio.malackath.com) llevado al sitio de Malackath.

Fuente única de datos: portfolio/proyectos.py (nombres, tipos y descripciones ya publicados)
y las capturas reales de portfolio/public/img/p/. Pedido de Ber, 2026-11-25.

Qué hace (todo con componentes del propio Stitch, sin rediseñar):
- Identidad de marca (home): los 12 logos provisorios pasan a ser los logos reales.
- Trabajo: a las 6 tarjetas de Stitch se suman los otros 16 proyectos, con el mismo
  componente de tarjeta y la misma secuencia de anchos (8+4, 4+8, 6+6). Índice igual.
- Armá Partido, Palquear y Mesaluma: la foto genérica queda y se le suma encima un celular
  con una captura real de la app (pendiente anotado por Ber: «no se reemplaza, se agrega»).
- RaveKit: la imagen de Stitch (rota) pasa a ser una captura real de getravekit.com.
"""
import glob
import html
import os
import shutil
import sys
from pathlib import Path

AQUI = Path(__file__).parent
IMG_SRC = AQUI / "portfolio" / "public" / "img" / "p"
DEST = "img/portfolio/"            # dentro de public/
PORTFOLIO = "https://portfolio.malackath.com/"

sys.path.insert(0, str(AQUI / "portfolio"))
from proyectos import PUBLICOS  # noqa: E402

P = {p["c"]: p for p in PUBLICOS}


def _primera(patron):
    f = sorted(glob.glob(str(IMG_SRC / patron)))
    return os.path.basename(f[0]) if f else None


def imagen(c, cual):
    """cual: 'd' (primera de compu), 'm' (primera de celular) o 'logo'."""
    if cual == "logo":
        if c == "nunca-te-falla":
            return "nunca-te-falla-logo.svg"
        if c == "marealta-consultora":
            return "marealta-consultora-logo.png"
        if c == "ruvia":
            return "ruvia-logo.png"     # logo nuevo de RuVIAJE (logo_archivo en proyectos.py)
        if c == "citadenta":
            return "citadenta-logo.png"   # logo_archivo en proyectos.py (negativo, para fondo oscuro)
        return _primera(f"{c}-logo-[0-9a-f]*.webp")
    if c == "sitios-gastro":
        return _primera(f"sitios-gastro-fuego-silvestre-{cual}-01-*.webp")
    return _primera(f"{c}-{cual}-01-*.webp")


_USADAS = set()


def ruta(nombre, pre=""):
    _USADAS.add(nombre)
    return f"{pre}{DEST}{nombre}"


def copiar(out):
    d = Path(out) / DEST
    d.mkdir(parents=True, exist_ok=True)
    for n in sorted(_USADAS):
        src = AQUI / "design" / "tarjetas" / n
        shutil.copy(src if src.exists() else IMG_SRC / n, d / n)
    print(f"portfolio: {len(_USADAS)} imágenes copiadas a {DEST}")


# ------------------------------------------------------------ IDENTIDAD DE MARCA
# Los proyectos con logo propio (La Gloria, UsaStorefront y Web Arnelli no tienen logo: quedan fuera).
CON_LOGO = ["arma-partido", "pizcaya", "palquear", "cartelera", "mesaluma", "ravekit", "barajala",
            "coinciva", "ruvia", "nunca-te-falla",
            "marea-alta", "marealta-consultora", "banana-team", "ecos", "velvet", "patovava",
            "jip", "zoomi", "coat-n-nest", "sitios-gastro", "citadenta"]   # Citadenta al final: no corre los verdes por posición


# Marea Alta tenía dos tarjetas seguidas (la parte digital y la consultora): en el home queda una sola (Ber, 2026-11-25)
FUERA_HOME = {"marealta-consultora"}


# proyectos con caso de estudio en el sitio
CASOS = {"arma-partido": "arma-partido", "pizcaya": "pizcaya", "palquear": "palquear", "cartelera": "cartelera",
         "mesaluma": "mesaluma", "ravekit": "ravekit", "citadenta": "citadenta"}


def _fondo_blanco(nombre):
    """Logo que trae su propio fondo blanco (ej. Botánica Bistro en Sitios Gastro): el recuadro entero va en blanco,
    como Mesaluma y Zoomi, para que no quede un rectángulo blanco flotando sobre el oscuro (Ber, 2026-11-25)."""
    try:
        from PIL import Image
        im = Image.open(IMG_SRC / nombre).convert("RGBA")
    except Exception:
        return False
    esquinas = [im.getpixel(p) for p in [(1, 1), (im.width - 2, 1), (1, im.height - 2), (im.width - 2, im.height - 2)]]
    return all(a > 250 and min(r, g, b) > 245 for r, g, b, a in esquinas)


def marcas(todos=False):
    """Logos para el carrusel del home (2 filas) o, con todos=True, la lista completa para marcas.html.
    Cada logo del home lleva a su tarjeta en marcas.html (pedido de Ber, 2026-11-25: no salir al portfolio)."""
    filas = []
    for c in CON_LOGO:
        if c in FUERA_HOME:   # también en la página de logos: un solo Marea Alta
            continue
        p = P[c]
        fondo = "blanco" if _fondo_blanco(imagen(c, "logo")) else p["fondo"]
        filas.append({"clave": c, "nombre": p["n"], "imagen": ruta(imagen(c, "logo")), "url": "marcas.html#" + c,
                      "caso": CASOS.get(c), "tipo": p["t"], "descripcion": p["d"], "fondo": fondo})
    if todos:
        return filas
    fila_1, fila_2 = filas[:10], filas[10:]
    # Citadenta en el medio de la segunda fila del home, no al final (Ber, 2026-11-26).
    # El verde del home va por marca (MARCAS_LIMA), así que moverla no corre los verdes.
    cit = [f for f in fila_2 if f["clave"] == "citadenta"]
    if cit:
        fila_2.remove(cit[0])
        fila_2.insert(len(fila_2) // 2, cit[0])
    return fila_1, fila_2


# ------------------------------------------------------------ TRABAJO
# Los 16 proyectos del portfolio que no tenían tarjeta (las 6 de Stitch quedan como están).
EXTRA = ["nunca-te-falla", "mesaluma", "ruvia", "coinciva", "barajala", "marealta-consultora",
         "marea-alta", "velvet", "ecos", "patovava", "zoomi", "jip",
         "sitios-gastro", "banana-team", "usa-storefront", "web-arnelli", "coat-n-nest", "citadenta"]
# Mesaluma ya comparte tarjeta con La Gloria en Stitch: no se repite.
EXTRA.remove("mesaluma")

SITIO = {"marealta-consultora": "marealtagastro.com", "ecos": "ecos.arnelli.com"}
ANCHOS = [8, 4, 4, 8, 6, 6]   # la secuencia de las 6 tarjetas de Stitch


def categoria(p):
    if p.get("solo_logo"):
        return "branding"
    return "mobile" if p["t"] == "App" else "web"


CATEGORIA_TXT = {"mobile": "App", "web": "Web", "branding": "Marca"}


# Tarjetas con foto propia en lugar de una captura (Ber, 2026-11-25: Citadenta con «una persona, un médico,
# una sonrisa y el loguito»: foto del equipo del folleto + logo, armada desde insumos/citadenta).
FOTO_TARJETA = {"citadenta": ("img/proyectos/citadenta-equipo.webp", "Equipo de una clínica dental sonriendo, con el logo de Citadenta")}


def tarjeta_trabajo(c, i, total, ancho):
    p = P[c]
    e = html.escape
    cat = categoria(p)
    if p.get("solo_logo"):
        img = (f'<img alt="Logo de {e(p["n"])}" loading="lazy" class="md:absolute md:inset-0 w-full h-full object-contain p-12 md:p-16 '
               f'transition-transform duration-700 group-hover:scale-105" src="{ruta(imagen(c, "logo"))}"/>')
    elif c in FOTO_TARJETA:
        img = (f'<img alt="{e(FOTO_TARJETA[c][1])}" loading="lazy" class="md:absolute md:inset-0 w-full h-full object-cover '
               f'transition-transform duration-700 group-hover:scale-105" src="{FOTO_TARJETA[c][0]}"/>')
    elif imagen(c, "d") is None or c == "ruvia":   # RuVIAJE: la tarjeta sigue mostrando el celular (la web nueva va en el portfolio)
        img = (f'<img alt="{e(p["n"])}: pantalla de la app" loading="lazy" class="md:absolute md:inset-0 w-full h-full object-contain py-space-md '
               f'transition-transform duration-700 group-hover:scale-105" src="{ruta(imagen(c, "m"))}"/>')
    else:
        img = (f'<img alt="{e(p["n"])}: pantalla principal" loading="lazy" style="object-position:left top" class="md:absolute md:inset-0 w-full h-full object-cover '
               f'transition-transform duration-700 group-hover:scale-105" src="{ruta(imagen(c, "d"))}"/>')
    sitio = ""
    if c in SITIO:
        sitio = f"""
<div class="absolute bottom-space-md left-space-md right-space-md opacity-0 group-hover:opacity-100 transition-opacity duration-300 bg-surface-container/90 backdrop-blur-xl p-space-md rounded-lg shadow-lg flex items-center justify-between">
<span class="font-label-sm text-label-sm uppercase text-on-surface-variant">Sitio</span>
<span class="font-label-md text-label-md font-bold text-primary-container">{SITIO[c]}</span>
</div>"""
    # con caso de estudio propio (Citadenta): la tarjeta lleva al caso, como las de Stitch
    href = f"casos/{CASOS[c]}.html" if c in CASOS else PORTFOLIO + "#" + c
    ver = ("Ver caso de estudio", f"{p['n']}: caso de estudio") if c in CASOS else ("Ver en el portfolio", f"{p['n']} en el portfolio")
    titulo = "font-headline-md text-headline-md md:font-headline-lg md:text-headline-lg" if ancho >= 6 else "font-headline-md text-headline-md"
    return f"""<!-- Proyecto {i:02d}: {e(p["n"])} (del portfolio) -->
<article class="project-card md:row-span-2 md:grid md:grid-rows-subgrid md:gap-0 md:col-span-{ancho} flex flex-col group relative rounded-xl bg-surface-container-low overflow-hidden shadow-xl transition-all duration-500 hover:-translate-y-1" data-category="{cat}">
<div class="relative w-full aspect-[4/5] md:aspect-auto md:h-full md:min-h-[320px] overflow-hidden bg-surface-container-highest">
{img}
<div class="absolute inset-0 bg-gradient-to-t from-surface-container-lowest via-surface-container-lowest/30 to-transparent"></div>
<div class="absolute top-space-md left-space-md flex flex-wrap items-center gap-space-xs">
<span class="px-space-sm py-space-xs rounded-full bg-surface-container-lowest/80 backdrop-blur-md font-label-sm text-label-sm uppercase text-primary tracking-wider">
              {e(p["t"])}
            </span>
</div>{sitio}
</div>
<div class="p-space-lg md:py-space-xl flex flex-col justify-between flex-1 gap-space-md">
<div class="flex flex-col gap-space-xs">
<div class="flex items-center justify-between">
<span class="font-label-sm text-label-sm uppercase text-on-surface-variant tracking-wider">{e(CATEGORIA_TXT[cat])}</span>
<span class="font-label-sm text-label-sm text-on-surface-variant font-mono">{i:02d} // {total:02d}</span>
</div>
<h2 class="{titulo} uppercase text-primary group-hover:text-primary-container transition-colors tracking-tight">
              <a href="{href}">{e(p["n"].upper())}</a>
            </h2>
<p class="font-body-sm text-body-sm text-on-surface-variant line-clamp-2">
              {e(p["d"])}
            </p>
</div>
<div class="flex items-center justify-between pt-space-xs">
<span class="font-label-sm text-label-sm uppercase text-on-surface-variant">{ver[0]}</span>
<a href="{href}" aria-label="{e(ver[1])}" class="w-10 h-10 rounded-full bg-surface-container-high group-hover:bg-primary-container text-primary group-hover:text-on-primary-fixed flex items-center justify-center transition-all duration-300">
<span class="material-symbols-outlined text-[20px] transition-transform duration-300 group-hover:translate-x-0.5 group-hover:-translate-y-0.5">north_east</span>
</a>
</div>
</div>
</article>
"""


def fila_indice(c, i):
    p = P[c]
    e = html.escape
    cat = categoria(p)
    return f"""<!-- Row {i:02d} -->
<a class="list-item-row group grid grid-cols-12 items-center px-space-lg py-space-lg hover:bg-surface-container-high transition-colors" data-category="{cat}" href="{f'casos/{CASOS[c]}.html' if c in CASOS else PORTFOLIO + '#' + c}">
<div class="col-span-1 font-label-md text-label-md text-on-surface-variant font-mono">{i:02d}</div>
<div class="col-span-4 flex flex-col">
<span class="font-headline-sm text-headline-sm uppercase text-primary group-hover:text-primary-container transition-colors">{e(p["n"].upper())}</span>
<span class="font-body-sm text-body-sm text-on-surface-variant">{e(p["d"])}</span>
</div>
<div class="col-span-3 font-label-sm text-label-sm uppercase text-on-surface-variant">{e(p["t"])}</div>
<div class="col-span-2"></div>
<div class="col-span-1"></div>
<div class="col-span-1 flex justify-end">
<div class="w-8 h-8 rounded-full bg-surface-container flex items-center justify-center group-hover:bg-primary-container group-hover:text-on-primary-fixed text-primary transition-colors">
<span class="material-symbols-outlined text-[18px]">arrow_forward</span>
</div>
</div>
</a>
"""


def tarjetas_extra(desde, total):
    return "".join(tarjeta_trabajo(c, desde + k, total, ANCHOS[k % len(ANCHOS)]) for k, c in enumerate(EXTRA))


def filas_extra(desde):
    return "".join(fila_indice(c, desde + k) for k, c in enumerate(EXTRA))


# ------------------------------------------------------------ CELULAR SOBRE LA FOTO
CSS_CELULAR = """
.celu-real { position:absolute; z-index:2; right:4%; bottom:-14%; width:clamp(84px, 24%, 150px); aspect-ratio:9/19.5;
  border-radius:20px; padding:5px; background:#1c1b1d; box-shadow:0 18px 40px rgba(0,0,0,.55), 0 0 0 1px rgba(255,255,255,.08);
  transform:rotate(-4deg); transition:transform .5s; pointer-events:none; }
.celu-real img { width:100%; height:100%; object-fit:cover; object-position:top; border-radius:15px; display:block; }
.group:hover .celu-real { transform:rotate(-2deg) translateY(-6px); }
@media (prefers-reduced-motion: reduce) { .celu-real, .group:hover .celu-real { transition:none; transform:rotate(-4deg); } }
"""


def celular(c, pre=""):
    p = P[c]
    return (f'<div class="celu-real" aria-hidden="true"><img alt="" loading="lazy" '
            f'src="{ruta(imagen(c, "m"), pre)}"/></div><!-- celular real: {html.escape(p["n"])} -->')
