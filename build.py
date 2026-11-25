"""Arma el sitio de Malackath a partir del HTML exportado de Stitch.

Regla: el diseño de Stitch se respeta tal cual. Solo se cambia:
- logo Kinetic -> logo Malackath
- imágenes generadas -> fotos y capturas reales de los proyectos
- números/métricas no confirmados -> se sacan
- datos falsos de agencia (Kinetic, París/NY/Tokio) -> datos reales
- links internos para que las páginas se conecten

Uso: python3 build.py stitch public   (después: npm run css)
"""
import glob
import html
import re
import shutil
import casos_textos
import portfolio_web
import sys
from pathlib import Path

SRC = Path(sys.argv[1])
OUT = Path(sys.argv[2])

MAIL = "hola@malackath.com"          # elegido por Ber; la casilla falta crearla
WHATSAPP = "https://wa.me/59894202607"  # WhatsApp de Ber
# Vista previa: no indexar en buscadores. Pasar a False el día del lanzamiento.
BORRADOR = False  # lanzamiento en malackath.com con OK de Ber (2026-11-25)


def leer(nombre):
    return (SRC / nombre / "code.html").read_text(encoding="utf-8")


def rep(s, viejo, nuevo, n=1):
    c = s.count(viejo)
    if c < 1 or (n and c != n):
        raise SystemExit(f"No encontré (o encontré {c} veces) el texto: {viejo[:90]!r}")
    return s.replace(viejo, nuevo)


def cortar(s, desde, hasta):
    """Saca desde el marcador `desde` hasta justo antes de `hasta`."""
    i = s.find(desde)
    j = s.find(hasta, i + 1)
    if i < 0 or j < 0:
        raise SystemExit(f"Marcadores no encontrados: {desde!r} / {hasta!r}")
    return s[:i] + s[j:]


def link(s, texto, href):
    """Pone href al <a> que contiene `texto` (la primera vez que aparece)."""
    k = s.find(texto)
    if k < 0:
        raise SystemExit(f"Link no encontrado: {texto!r}")
    a = s.rfind("<a ", 0, k)
    fin = s.find(">", a)
    tag = s[a:fin]
    tag2 = re.sub(r'href="[^"]*"', f'href="{href}"', tag)
    if 'href="' not in tag:
        tag2 = tag + f' href="{href}"'
    if href.startswith("http"):
        tag2 += ' target="_blank" rel="noopener"'
    return s[:a] + tag2 + s[fin:]



def textos(s, mapa, estricto=True):
    """Reemplaza nodos de texto completos (espacios normalizados) según `mapa`."""
    import html as _h
    usados = set()
    def _f(m):
        crudo = m.group(1)
        clave = " ".join(_h.unescape(crudo).split())
        if clave in mapa:
            usados.add(clave)
            pre = crudo[:len(crudo) - len(crudo.lstrip())]
            pos = crudo[len(crudo.rstrip()):]
            return ">" + pre + _h.escape(mapa[clave], quote=False) + pos + "<"
        return m.group(0)
    s = re.sub(r">([^<>]+)<", _f, s)
    faltan = [k for k in mapa if k not in usados]
    if estricto and faltan:
        raise SystemExit("Textos no encontrados: " + " | ".join(f[:60] for f in faltan))
    return s


def imagenes(s, mapa, pre):
    """Reemplaza las imágenes de Stitch por orden. mapa: lista (archivo|None, alt, estilo extra)."""
    tags = list(re.finditer(r"<img[^>]*>", s))
    if len(tags) != len(mapa):
        raise SystemExit(f"Hay {len(tags)} imágenes y el mapa tiene {len(mapa)}")
    out, last = [], 0
    for m, (archivo, alt, extra) in zip(tags, mapa):
        tag = m.group(0)
        if archivo is not None:
            tag = re.sub(r'src="[^"]*"', f'src="{pre}{archivo}"', tag)
            tag = re.sub(r'\s(data-)?alt="[^"]*"', "", tag)
            tag = tag.replace("<img", f'<img alt="{alt}" loading="lazy"', 1)
            if extra:
                tag = tag.replace('class="', f'style="{extra}" class="', 1)
        out.append(s[last:m.start()] + tag)
        last = m.end()
    out.append(s[last:])
    return "".join(out)


def fondos(s, mapa):
    """Reemplaza por orden las imágenes de Stitch usadas como background-image. None = queda."""
    urls = list(re.finditer(r"url\('(https://lh3[^']+)'\)", s))
    if len(urls) != len(mapa):
        raise SystemExit(f"Hay {len(urls)} fondos y el mapa tiene {len(mapa)}")
    out, last = [], 0
    for m, archivo in zip(urls, mapa):
        out.append(s[last:m.start()] + (f"url('{archivo}')" if archivo else m.group(0)))
        last = m.end()
    out.append(s[last:])
    return "".join(out)


# RaveKit no tiene foto real en la compu de Ber: se usa la imagen que generó Stitch (PENDIENTE reemplazar)
RAVEKIT_STITCH = re.findall(r'src="(https://lh3[^"]+)"', (SRC / "kinetic_home_proyectos_reales" / "code.html").read_text(encoding="utf-8"))[7]

SAMPLE = ('<span class="self-start px-space-sm py-space-xs rounded-full bg-surface-container-highest '
          'font-label-sm text-label-sm uppercase text-on-surface-variant tracking-wider">Sample</span>')


def comun(s, pre, titulo, descripcion, activo=None):
    # idioma y <head>
    s = rep(s, '<html class="dark" lang="en">', '<html class="dark" lang="es">')
    cabeza = (f'<title>{titulo}</title><meta name="description" content="{descripcion}"/>'
              f'<link rel="icon" href="{pre}img/marca/favicon.svg" type="image/svg+xml"/>'
              f'<link rel="alternate icon" href="{pre}img/marca/favicon.ico"/>'
              f'<link rel="apple-touch-icon" href="{pre}img/marca/icono-app-blanco-180.png"/>')
    # algunas pantallas de Stitch traen el meta sin la barra final (<meta ...>): Estudio y Presupuesto quedaban sin título
    s, n = re.subn(r'<meta content="web_standard" name="shell-type"\s*/?>', lambda m: cabeza, s, count=1)
    if n != 1:
        raise SystemExit("No encontré el meta shell-type para poner el título")
    # Tailwind: en vez del CDN de Stitch, el CSS compilado con la misma config (ver tailwind.config.js)
    s, n = re.subn(r'<script src="https://cdn\.tailwindcss\.com[^"]*"></script><script id="tailwind-config">.*?</script>',
                   f'<link rel="stylesheet" href="{pre}css/estilos.css"/>', s, flags=re.S)
    if n != 1:
        raise SystemExit("No encontré el Tailwind de Stitch")
    # mobile: Stitch usa tamaños de escritorio sin su variante mobile en algunos títulos y en
    # celular se salen de la pantalla. Se usan los tamaños mobile que define el propio sistema de Stitch.
    def _mobile(m):
        c = m.group(1)
        for t in ("display-xl", "display-lg", "headline-lg"):
            if re.search(rf"(?<![\w:-])text-{t}(?![\w-])", c) and f"text-{t}-mobile" not in c:
                c = re.sub(rf"(?<![\w:-])text-{t}(?![\w-])", f"text-{t}-mobile md:text-{t}", c)
        return f'class="{c}"'
    s = re.sub(r'class="([^"]*)"', _mobile, s)
    # los brillos de fondo de Stitch se salen del ancho en celular: se recortan
    s = rep(s, "body { overscroll-behavior: none; }", "body { overscroll-behavior: none; } body > main, body > footer { overflow-x: clip; } @media (max-width: 767px) { .text-display-xl-mobile { font-size: clamp(1.6rem, 7.9vw, 2.75rem) !important; line-height: 1.1 !important; } .text-display-lg-mobile { font-size: clamp(1.6rem, 7.6vw, 2.25rem) !important; } }")
    # logo
    s, n = re.subn(r'<img alt="Kinetic Agency Logo"[^>]*>\s*<span class="[^"]*">KINETIC</span>',
                   f'<img alt="Malackath" class="h-8 w-auto object-contain" src="{pre}img/marca/malackath-horizontal-color-negativo.svg"/>', s)
    if n != 1:
        raise SystemExit("No encontré el logo de Kinetic")
    # links del menú y botones con data-path
    destinos = {"home": "index.html", "portfolio": "trabajo.html", "services": "servicios.html",
                "studio": "estudio.html", "case-studies": "casos-de-estudio.html", "contact": "estudio.html#contacto"}
    for clave, dest in destinos.items():
        s = re.sub(rf'data-path="{clave}" href="[^"]*"', f'data-path="{clave}" href="{pre}{dest}"', s)
        s = re.sub(rf'href="[^"]*" data-path="{clave}"', f'href="{pre}{dest}" data-path="{clave}"', s)
    # botón de persona del header (sin cuenta de usuario): lleva a contacto
    s = s.replace('<div class="w-8 h-8 rounded-full bg-primary flex items-center justify-center"><span class="material-symbols-outlined text-on-primary text-[18px]">person</span></div>',
                  f'<a aria-label="Contacto" href="{pre}estudio.html#contacto" class="w-8 h-8 rounded-full bg-primary flex items-center justify-center"><span class="material-symbols-outlined text-on-primary text-[18px]">person</span></a>')
    # footer: datos reales
    s = s.replace("PARIS [CET]", "MONTEVIDEO [UYT]").replace("NEW YORK [EST]", "BRASIL [BRT]")
    s = re.sub(r'<span class="text-on-surface-variant">/</span><span class="flex items-center gap-space-xs"><span class="h-1.5 w-1.5 rounded-full bg-primary-container"></span>TOKYO \[JST\]</span>', "", s)
    s = s.replace("© 2024 KINETIC STUDIO INC. ALL RIGHTS RESERVED.", "© 2026 MALACKATH. TODOS LOS DERECHOS RESERVADOS.")
    s = s.replace("© 2024 KINETIC STUDIO INC. ALL RIGHTS RESERVED", "© 2026 MALACKATH. TODOS LOS DERECHOS RESERVADOS")
    return s


# ------------------------------------------- FONDOS DE FOTO EN EL HERO DE LOS CASOS
# Pedido de Ber (2026-11-25): 2 fotos genéricas por caso, generadas en Flow (design/fondos-casos/,
# prompts en /mnt/project-files/malackath/casos-fondos/prompts-flow.md), que se alternan cada 5 s
# detrás del título, con velo oscuro para que el texto se lea.
def fotos_caso(nombre, tipo):
    """Fotos de fondo de un caso por convención de nombre (vale para todos los casos, actuales y futuros):
    design/fondos-casos/<clave>-1-*.webp y <clave>-2-*.webp → hero (se alternan); <clave>-pilares.webp → sección de pilares.
    <clave> = nombre de la página sin guiones (casos/arma-partido.html → armapartido)."""
    if nombre == "index.html":
        clave = "home"   # prueba en la home (pedido de Ber, 2026-11-25)
    elif nombre.startswith("casos/"):
        clave = nombre[len("casos/"):-len(".html")].replace("-", "")
    else:
        return []
    if tipo == "hero":
        return [Path(f).stem for f in sorted(glob.glob(str(FONDOS_SRC / f"{clave}-[0-9]-*.webp")))]
    return [clave + "-pilares"] if (FONDOS_SRC / f"{clave}-pilares.webp").exists() else []
FONDOS_SRC = Path(__file__).parent / "design" / "fondos-casos"
CSS_FONDO = """<style>
.caso-fondo{position:absolute;top:0;left:0;right:0;bottom:-120px;z-index:-1;pointer-events:none;overflow:hidden}
main section{position:relative}
.caso-fondo img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:center;opacity:0;transition:opacity 1.4s ease}
.caso-fondo img.activa{opacity:1}
.caso-fondo::after{content:"";position:absolute;inset:0;background:linear-gradient(90deg,rgba(19,19,21,.8) 0%,rgba(19,19,21,.55) 38%,rgba(19,19,21,.25) 70%,rgba(19,19,21,.15) 100%),linear-gradient(0deg,#131315 0%,rgba(19,19,21,.55) 22%,rgba(19,19,21,0) 50%)}
@media (max-width:767px){.caso-fondo::after{background:linear-gradient(0deg,#131315 0%,rgba(19,19,21,.7) 35%,rgba(19,19,21,.45) 100%)}}
</style>"""
JS_FONDO = """<script>(function(){var f=document.querySelector('.caso-fondo');if(!f)return;var im=f.querySelectorAll('img');
if(im.length<2||matchMedia('(prefers-reduced-motion: reduce)').matches)return;var k=0;
setInterval(function(){im[k].classList.remove('activa');k=(k+1)%im.length;im[k].classList.add('activa');},5000);})();</script>"""


# Sección de pilares (pedido de Ber): foto a todo el ancho detrás de las tarjetas, con velo oscuro.
MARCAS_PILARES = ("<!-- SECTION: SOLUTION & ARCHITECTURE -->", "<!-- SECTION 5: Product Architecture & Technical Pillars -->",
                  "<!-- 5. PRINCIPIOS & METODOLOGÍA -->")
CSS_PILARES = """<style>
.seccion-fondo{position:absolute;inset:0;z-index:-1;pointer-events:none;overflow:hidden}
.seccion-fondo img{width:100%;height:100%;object-fit:cover;object-position:center}
.seccion-fondo::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,#131315 0%,rgba(19,19,21,.55) 18%,rgba(19,19,21,.45) 50%,rgba(19,19,21,.55) 82%,#131315 100%)}
</style>"""


def fondo_pilares(nombre, s):
    fotos = fotos_caso(nombre, "pilares")
    marca = next((m for m in MARCAS_PILARES if m in s), None)
    if not fotos or not marca:
        return s
    i = s.find("<section", s.find(marca))
    j = s.find(">", i)
    tag = re.sub(r"\sbg-surface[\w-]*", "", s[i:j]).replace('class="', 'class="relative isolate ', 1)
    copiar_fondo(fotos[0])
    pre = "../" * nombre.count("/")
    img = f'<img alt="" loading="lazy" src="{pre}img/casos-fondos/{fotos[0]}.webp"/>'
    s = s[:i] + tag + f'>\n<div class="seccion-fondo" aria-hidden="true">{img}</div>' + s[j + 1:]
    return s.replace("</head>", CSS_PILARES + "</head>", 1)


def copiar_fondo(f):
    d = OUT / "img" / "casos-fondos"
    d.mkdir(parents=True, exist_ok=True)
    shutil.copy(FONDOS_SRC / f"{f}.webp", d / f"{f}.webp")


def fondo_caso(nombre, s):
    s = fondo_pilares(nombre, s)
    fotos = fotos_caso(nombre, "hero")
    if not fotos:
        return s
    i = s.find("<section", s.find("<main"))
    j = s.find(">", i)
    tag = s[i:j]
    tag = tag.replace('class="', 'class="relative isolate ', 1)
    pre = "../" * nombre.count("/")
    imgs = "".join(f'<img alt="" {"" if k else "fetchpriority=\"high\" "}class="{"activa" if k == 0 else ""}" src="{pre}img/casos-fondos/{f}.webp"/>'
                   for k, f in enumerate(fotos))
    for f in fotos:
        copiar_fondo(f)
    # en la home el hero recorta lo que sobresale (overflow-hidden): el fundido termina dentro de la sección
    extra = ' style="bottom:0"' if "overflow-hidden" in tag else ""
    s = s[:i] + tag + f'>\n<div class="caso-fondo" aria-hidden="true"{extra}>{imgs}</div>' + s[j + 1:]
    s = s.replace("</head>", CSS_FONDO + "</head>", 1).replace("</body>", JS_FONDO + "</body>", 1)
    return s


# Tarjetas de Trabajo en verde lima: SOLO las 8 que Ber marcó (2026-11-25, «solo donde indiqué»).
# Número de tarjeta en trabajo.html. Las demás y Casos de estudio quedan como Stitch.
# Degradé sobre el lima, opción C «Más vivo, hacia el verde» (Ber, 2026-11-25): luz amarilla arriba a la izquierda, verde intenso abajo a la derecha.
CSS_CAJA_LIMA = (".caja-lima{background:radial-gradient(60% 100% at 0% 0%,rgba(255,255,170,.9) 0%,rgba(255,255,170,0) 60%),"
                 "radial-gradient(90% 130% at 100% 100%,#4FC21A 0%,rgba(79,194,26,0) 60%),"
                 "linear-gradient(135deg,#E8FF4A 0%,#CAF300 50%,#93DA00 100%);box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}"
                 ".group:hover .caja-lima{filter:brightness(1.04)}"
                 # celular: la letra del hero es ancha; «USASTOREFRONT» no entraba en Trabajo
                 "@media (max-width:767px){.project-card .caja-lima :is(h2,h3){font-size:min(1.75rem,calc((100vw - 90px) / 15))!important;line-height:1.1!important}}")
TARJETAS_LIMA = {"01", "04", "07", "10", "13", "18", "20", "21"}
FLECHA_GRIS = "rounded-full bg-surface-container-high group-hover:bg-primary-container text-primary group-hover:text-on-primary-fixed"
FLECHA_LIMA = "rounded-full bg-primary-container text-on-primary-fixed group-hover:bg-primary-fixed-dim group-hover:scale-110"



def _caja_lima(m):
    """Caja de texto de la tarjeta en verde lima con letra oscura (decisión de Ber, 2026-11-25)."""
    a = m.group(0)
    n = re.search(r"(\d\d) // \d\d", a)
    if not n or n.group(1) not in TARJETAS_LIMA:
        return a
    i = a.rfind('<div class="p-space-lg')
    if i < 0:
        return a
    caja = a[i:]
    caja = caja.replace('<div class="p-space-lg', '<div class="caja-lima bg-primary-container p-space-lg', 1)
    caja = caja.replace(FLECHA_LIMA, "@@FLECHA_CAJA@@").replace(FLECHA_GRIS, "@@FLECHA_CAJA@@")
    caja = caja.replace("group-hover:text-primary-container", "")
    caja = re.sub(r"(?<![\w:-])text-on-surface-variant(?![\w-])", "text-on-primary-fixed/70", caja)
    caja = re.sub(r"(?<![\w:/-])text-primary-container(?![\w-])", "text-on-primary-fixed", caja)
    caja = re.sub(r"(?<![\w:-])text-primary(?![\w-])", "text-on-primary-fixed", caja)
    caja = re.sub(r"(?<![\w:-])bg-surface-container-high(?![\w-])", "bg-on-primary-fixed/10", caja)
    caja = caja.replace("@@FLECHA_CAJA@@", "rounded-full bg-on-primary-fixed text-primary-container group-hover:scale-110")
    # Título con la letra del titular del hero, igual que las tarjetas verdes de la home (Ber, 2026-11-25:
    # «todos los títulos de las tarjetas que tenían verde» van con esa tipografía).
    caja = re.sub(r'<(h[23]) class="font-headline-(?:lg|md) ([^"]*)"',
                  lambda t: f'<{t.group(1)} class="font-display-xl font-extrabold md:font-extrabold uppercase tracking-tighter md:tracking-[-0.04em] '
                  + re.sub(r"md:font-headline-(?:lg|md) ?", "", t.group(2)) + '"', caja, count=1)
    return a[:i] + caja

# Sombra de las imágenes sobre el lima y título con la letra del titular del hero (Ber, 2026-11-25)
SOMBRA_SOBRE_LIMA = 'style="box-shadow:0 8px 16px -8px rgba(23,30,0,.55),0 2px 4px rgba(23,30,0,.25)" '
# Home, Proyectos destacados: tarjetas en verde lima con el mismo degradé que Trabajo (marcas de Ber, 2026-11-25)
HOME_LIMA = {"Armá Partido", "RaveKit"}


def _home_lima(m):
    a = m.group(0)
    t = re.search(r"<h3[^>]*>(?:<a[^>]*>)?([^<]+)", a)
    if not t or t.group(1).strip() not in HOME_LIMA:
        return a
    a = a.replace("bg-surface-container p-space-lg", "caja-lima p-space-lg", 1)
    a = a.replace("hover:bg-surface-container-high", "", 1)
    a = a.replace('<div class="relative w-full h-', '<div ' + SOMBRA_SOBRE_LIMA + 'class="relative w-full h-', 1)
    a = re.sub(r'<h3 class="font-headline-(?:lg|md) ', '<h3 class="font-display-xl font-extrabold md:font-extrabold uppercase tracking-tighter md:tracking-[-0.04em] ', a, count=1)
    i = a.find('<div class="flex flex-col gap-space-sm">')
    if i < 0:
        return a
    txt = a[i:]
    txt = txt.replace("group-hover:text-primary-container", "")
    txt = re.sub(r"(?<![\w:-])text-on-surface-variant(?![\w-])", "text-on-primary-fixed/70", txt)
    txt = re.sub(r"(?<![\w:/-])text-(?:primary-container|secondary|tertiary|tertiary-fixed)(?![\w-])", "text-on-primary-fixed/70", txt)
    txt = re.sub(r"(?<![\w:-])text-primary(?![\w-])", "text-on-primary-fixed", txt)
    txt = re.sub(r"(?<![\w:-])bg-surface-container-highest(?![\w-])", "bg-on-primary-fixed/10", txt)
    return a[:i] + txt


# Identidad de marca (home): cada tanto una tarjeta en verde lima, cada una con su degradé (Ber, 2026-11-25).
# Elegidas a mano para que el ritmo parezca aleatorio sin amontonarse (fila 1 y fila 2 del carrusel).
MARCAS_LIMA = {"pizcaya": 0, "mesaluma": 1, "ruvia": 2, "banana-team": 3, "patovava": 1, "coat-n-nest": 0}
DEGRADES_LIMA = [
    "radial-gradient(60% 100% at 0% 0%,rgba(255,255,170,.9) 0%,rgba(255,255,170,0) 60%),radial-gradient(90% 130% at 100% 100%,#4FC21A 0%,rgba(79,194,26,0) 60%),linear-gradient(135deg,#E8FF4A 0%,#CAF300 50%,#93DA00 100%)",
    "radial-gradient(70% 90% at 100% 0%,rgba(255,255,170,.9) 0%,rgba(255,255,170,0) 60%),radial-gradient(90% 120% at 0% 100%,#4FC21A 0%,rgba(79,194,26,0) 62%),linear-gradient(225deg,#E8FF4A 0%,#CAF300 50%,#93DA00 100%)",
    "radial-gradient(80% 60% at 50% 0%,rgba(255,255,170,.85) 0%,rgba(255,255,170,0) 65%),radial-gradient(120% 70% at 50% 100%,#4FC21A 0%,rgba(79,194,26,0) 60%),linear-gradient(180deg,#E8FF4A 0%,#CAF300 55%,#93DA00 100%)",
    "radial-gradient(60% 80% at 100% 100%,rgba(255,255,170,.85) 0%,rgba(255,255,170,0) 60%),radial-gradient(90% 120% at 0% 0%,#4FC21A 0%,rgba(79,194,26,0) 55%),linear-gradient(315deg,#E8FF4A 0%,#CAF300 50%,#93DA00 100%)",
]


# Página de logos (grilla): el verde va por posición, no por marca, para que no se toquen
# ni de lado ni en diagonal con 4 columnas (pantalla grande) ni de lado con 3 (Ber, 2026-11-25).
POSICIONES_LIMA_GRILLA = (0, 2, 9, 11, 16, 18)


def _marca_lima(m):
    a = m.group(0)
    k = re.search(r'data-marca="([\w-]+)"', a)
    if not k or k.group(1) not in MARCAS_LIMA:
        return a
    return _pintar_lima(a, DEGRADES_LIMA[MARCAS_LIMA[k.group(1)]])


def _grilla_lima(s):
    n = iter(range(10**6))
    def f(m):
        i = next(n)
        if i not in POSICIONES_LIMA_GRILLA:
            return m.group(0)
        return _pintar_lima(m.group(0), DEGRADES_LIMA[POSICIONES_LIMA_GRILLA.index(i) % len(DEGRADES_LIMA)])
    return re.sub(r'<(a|article) class="group w-full scroll-mt-28.*?</\1>', f, s, flags=re.S)


def _pintar_lima(a, fondo):
    a = a.replace("rounded-xl bg-surface-container p-space-md", "rounded-xl p-space-md", 1)
    a = a.replace("hover:bg-surface-container-high", "hover:brightness-105", 1)
    a = re.sub(r"^<(a|article) class=", lambda t: f'<{t.group(1)} style="background:{fondo};box-shadow:inset 0 1px 0 rgba(255,255,255,.6)" class=', a, count=1)
    a = re.sub(r"(?<![\w:-])text-primary-container(?![\w-])", "text-on-primary-fixed", a)
    a = re.sub(r"(?<![\w:-])text-on-surface-variant(?![\w-])", "text-on-primary-fixed/75", a)
    a = a.replace('<div class="w-full h-40', '<div ' + SOMBRA_SOBRE_LIMA + 'class="w-full h-40', 1)
    return a


# Cierres de las páginas internas con la letra ancha y gruesa del cierre del home (Ber, 2026-11-25:
# «quiero esa tipografía», sobre «Construyamos tu próximo producto»). Mismo tamaño que antes.
CSS_TITULO_CIERRE = """<style>@layer base {
.titulo-cierre { font-weight: 800 !important; letter-spacing: -0.04em !important; line-height: 1.08 !important; }
/* celular: la letra ancha no entraba; la caja usa el aire chico del sistema y la letra baja lo justo para «PRODUCCIÓN?» */
@media (max-width: 767px) {
  .titulo-cierre { font-size: min(1.75rem, calc((100vw - 88px) / 12.6)) !important; }
  div:has(> div > .titulo-cierre).rounded-xl, div:has(> div > div > .titulo-cierre).rounded-xl { padding: 1.5rem !important; }
}
}</style>"""


def titulo_cierre(s):
    n0 = s.count("titulo-cierre")
    s = re.sub(r'<h3 class="(font-headline-lg-mobile md:font-headline-lg text-headline-lg-mobile md:text-headline-lg text-primary uppercase)">(\s*¿)',
               r'<h3 class="titulo-cierre \1">\2', s)
    s = re.sub(r'<h2 class="(font-headline-lg text-headline-lg-mobile md:text-headline-lg uppercase text-primary tracking-tight)">(\s*(?:¿TENÉS UN PROYECTO|Iniciemos un proyecto))',
               r'<h2 class="titulo-cierre \1">\2', s)
    if s.count("titulo-cierre") > n0:
        s = s.replace("</head>", CSS_TITULO_CIERRE + "</head>", 1)
    return s


# Tarjetas de vidrio blanco transparente con borde biselado, sin tornasolado (Ber, 2026-11-25).
# Fondo de página: el liso de siempre. Las tarjetas verdes (lima) no se tocan.
CSS_VIDRIO = """<style>
.rounded-xl.bg-surface-container,.rounded-xl.bg-surface-container-low,.rounded-lg.bg-surface-container,.bg-surface-container.p-space-md{
 background:rgba(255,255,255,.035)!important;
 border:1px solid rgba(255,255,255,.12)!important;
 -webkit-backdrop-filter:blur(18px);backdrop-filter:blur(18px);
 box-shadow:inset 1px 1px 0 rgba(255,255,255,.16),inset -1px -1px 0 rgba(0,0,0,.35)}
.rounded-xl.bg-surface-container:hover,.rounded-xl.bg-surface-container-low:hover{
 background:rgba(255,255,255,.06)!important;border-color:rgba(255,255,255,.18)!important}
</style>"""


def guardar(nombre, s):
    s = fondo_caso(nombre, s)
    if nombre != "index.html":
        s = titulo_cierre(s)
    if nombre == "index.html":
        s = re.sub(r"<article class=\"(?:relative )?lg:col-span.*?</article>", _home_lima, s, flags=re.S)
        s = re.sub(r'<a class="group shrink-0 w-72.*?</a>', _marca_lima, s, flags=re.S)
        s = s.replace("</head>", "<style>" + CSS_CAJA_LIMA + "</style></head>", 1)
    if nombre == "marcas.html":
        s = _grilla_lima(s)
        s = s.replace("</head>", "<style>" + CSS_CAJA_LIMA + "</style></head>", 1)
    if nombre == "trabajo.html":
        s = re.sub(r'<article class="project-card.*?</article>', _caja_lima, s, flags=re.S)
        s = s.replace("</head>", "<style>" + CSS_CAJA_LIMA + "</style></head>", 1)
    s = s.replace("</head>", CSS_VIDRIO + "</head>", 1)
    # anclas: el header fijo mide 80px; el destino queda debajo con aire (pedido de Ber 2026-11-24)
    s = s.replace("</head>", '<style>html{scroll-padding-top:112px}</style></head>', 1)
    if BORRADOR:
        s = s.replace("</head>", '<meta name="robots" content="noindex, nofollow"/></head>', 1)
    # celular: el botón del menú no entra junto al selector de idioma; queda el ícono de contacto
    i, j = s.find("<header"), s.find("</header>")
    if i >= 0:
        cab = s[i:j]
        cab = re.sub(r'(<a class=")inline-flex( items-center justify-center[^"]*" data-path="contact")', r'\1hidden md:inline-flex\2', cab, count=1)
        cab = cab.replace('class="w-8 h-8 rounded-full bg-primary flex', 'class="hidden md:flex w-8 h-8 shrink-0 rounded-full bg-primary')
        cab = menu_celular(cab)
        s = s[:i] + cab + s[j:]
        s = s.replace("</body>", JS_MENU + "</body>", 1)
    s = pie(nombre, s)
    s = textos(s, casos_textos.COMUN, estricto=False)
    s = re.sub(r'data-alt="SaaS product design and brand identity for RaveKit[^"]*"',
               'data-alt="RaveKit: pedidos de reseñas por WhatsApp y QR"', s)
    p = OUT / nombre
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")
    quedan = s.count("lh3.googleusercontent.com")
    print(f"{nombre}: ok ({quedan} imágenes de Stitch sin reemplazar)")



# ------------------------------------------- MENÚ DEL CELULAR (pedido de Ber, 2026-11-25)
# Stitch no traía menú para celular: un botón redondo como el de contacto abre los mismos links del menú
# en una lista debajo de la barra, con el botón lima de «Iniciar proyecto».
def menu_celular(cab):
    nav = re.search(r"<nav [^>]*>(.*?)</nav>", cab, flags=re.S)
    if not nav:
        return cab
    links = re.findall(r'<a (?:aria-current="page" )?class="[^"]*" (data-path="[^"]*" href="[^"]*")>([^<]*)</a>', nav.group(1))
    assert len(links) == 4, links
    activo = re.search(r'<a aria-current="page" class="[^"]*" data-path="([^"]*)"', nav.group(1))
    items = "".join(
        f'<a {attrs} class="font-label-lg text-label-lg uppercase tracking-wider py-space-md border-b border-white/5 '
        + ("text-primary-container" if activo and f'data-path="{activo.group(1)}"' in attrs else "text-primary")
        + f'">{txt}</a>' for attrs, txt in links)
    contacto = re.search(r'<a class="hidden md:inline-flex[^"]*" (data-path="contact" href="[^"]*")>([^<]*)</a>', cab)
    boton = (f'<a {contacto.group(1)} class="mt-space-md inline-flex items-center justify-center px-space-lg py-space-md rounded-full '
             f'bg-primary-container text-on-primary-fixed font-label-md text-label-md uppercase">{contacto.group(2)}</a>') if contacto else ""
    panel = f'<nav id="menu-celu" class="md:hidden px-margin-mobile pb-space-lg flex-col" style="display:none">{items}{boton}</nav>'
    btn = ('<button type="button" aria-label="Menú" aria-expanded="false" aria-controls="menu-celu" data-menu '
           'class="md:hidden w-10 h-10 shrink-0 rounded-full bg-primary flex items-center justify-center">'
           '<span class="material-symbols-outlined text-on-primary text-[22px]">menu</span></button>')
    k = cab.rfind("</div></div>")
    return cab[:k] + btn + cab[k:] + panel


JS_MENU = """<script>
(function () {
  var b = document.querySelector('[data-menu]'), m = document.getElementById('menu-celu');
  if (!b || !m) return;
  function poner(abierto) {
    m.style.display = abierto ? 'flex' : 'none';
    b.setAttribute('aria-expanded', abierto);
    b.firstElementChild.textContent = abierto ? 'close' : 'menu';
  }
  b.addEventListener('click', function () { poner(m.style.display === 'none'); });
  m.addEventListener('click', function (e) { if (e.target.closest('a')) poner(false); });
  addEventListener('resize', function () { if (innerWidth >= 768) poner(false); });
})();
</script>"""


def pie(nombre, s):
    """Pie: afuera los links de Stitch que no llevan a ningún lado (redes y legales sin página);
    en el home se saca «Construyamos el futuro juntos» porque repite el cierre de arriba,
    y en las demás páginas ese título baja de tamaño en celular para que entre (pedido de Ber, 2026-11-25)."""
    i, j = s.find("<footer"), s.find("</footer>")
    if i < 0:
        return s
    f = s[i:j]
    f, n = re.subn(r'<div class="flex flex-wrap items-center gap-space-lg[^"]*">(?:<a [^>]*href="#">[^<]*</a>)+</div>', "", f)
    assert n == 1, f"{nombre}: redes del pie ({n})"
    f, n = re.subn(r'<div class="flex items-center gap-space-md font-label-sm[^"]*">(?:<a [^>]*href="#">[^<]*</a>(?:<span>/</span>)?)+</div>', "", f)
    assert n == 1, f"{nombre}: legales del pie ({n})"
    # logo de Malackath en el pie, arriba de los husos horarios (pedido de Ber, 2026-11-25)
    pre = "../" * nombre.count("/")
    f, n = re.subn(r'(<div class="flex flex-col lg:flex-row lg:items-center justify-between gap-space-xl pt-space-xl">)(<div class="flex flex-col gap-space-xs">)',
                   r'\1<div class="flex flex-col gap-space-lg"><a href="' + pre + 'index.html" aria-label="Malackath"><img alt="Malackath" class="h-10 md:h-12 w-auto" src="' + pre + r'img/marca/malackath-horizontal-color-negativo.svg"/></a>\2', f)
    assert n == 1, f"{nombre}: logo del pie ({n})"
    f = f.replace('BRASIL [BRT]</span></div></div>', 'BRASIL [BRT]</span></div></div></div>', 1) if "BRASIL [BRT]" in f else f
    # «Empecemos / Construyamos el futuro juntos» repetía el cierre de cada página: se saca en todas (Ber, 2026-11-25)
    f, n = re.subn(r'<div class="flex flex-col gap-space-md"><span [^>]*>[^<]*</span><h2 [^>]*>[^<]*</h2></div>', "", f)
    assert n == 1, f"{nombre}: título del pie ({n})"
    return s[:i] + f + s[j:]


# ------------------------------------------------- HERO: ventanas flotantes
def escenario_hero(pre=""):
    """Saca de la pantalla animada de Stitch el escenario 3D del hero (HTML, CSS y parallax)
    y le pone el contenido de cada ventana desde hero.py."""
    import hero, html as _h
    a = leer("kinetic_home_kinetic_hero_animated")
    i = a.find("<!-- HERO 3D PERSPECTIVE SHOWCASE INTERACTIVE STAGE -->")
    j = a.find("</section>", i)
    bloque = a[i:j].rstrip()
    # el bloque termina cerrando su contenedor de sección: dejamos solo el escenario
    assert bloque.endswith("</div>\n</div>") or bloque.endswith("</div>"), "escenario: final inesperado"
    css = a[a.find("/* Kinetic Animations"):a.find("</style>", a.find("/* Kinetic Animations"))]
    js_i = a.find("// 3D Perspective Parallax")
    js_f = a.find("// Scroll-Triggered Reveals")
    js = a[js_i:js_f]

    e = lambda t: _h.escape(t, quote=False)
    S = hero.SLOTS
    c, iz, ce = S["centro"], S["izquierda"], S["celular"]
    # textos (en orden de aparición en Stitch)
    for viejo, nuevo in [
        (">monolith.spatial.os<", ">" + e(c["barra"]) + "<"),
        (">WEBGL / SHADER<", ">" + e(c["barra_derecha"]) + "<"),
        (">Next-Gen FinTech<", ">" + e(c["rubro"]) + "<"),
        (">Monolith Quantum Yield<", ">" + e(c["titulo"]) + "<"),
        (">+240% Conv Rate<", ">" + e(c["chip"]) + "<"),
        (">solana-orbit.app<", ">" + e(iz["barra"]) + "<"),
        ("\n              FWA of the Day\n            ", e(iz["chip"])),
        (">Apple Design Award Nominee<", ">" + e(ce["chip"]) + "<"),
        (">Aura KineticOS<", ">" + e(ce["titulo"]) + "<"),
        (">Benchmark Performance<", ">" + e(hero.CHIP_METRICA[0]) + "<"),
        (">0.18s FCP / 100 SEO<", ">" + e(hero.CHIP_METRICA[1]) + "<"),
        (">WebGL 2.0 Native Flow<", ">" + e(hero.CHIP_FLOTANTE) + "<"),
    ]:
        bloque = rep(bloque, viejo, nuevo)
    # imágenes de cada ventana
    slots = iter([c, iz, ce])
    def _img(m):
        sl = next(slots)
        tag = m.group(0)
        if sl["imagen"]:
            if sl["imagen"].startswith(portfolio_web.DEST):
                portfolio_web.ruta(sl["imagen"][len(portfolio_web.DEST):])   # se copia desde el portfolio
            tag = re.sub(r'src="[^"]*"', f'src="{pre}{sl["imagen"]}"', tag)
            tag = re.sub(r'data-alt="[^"]*"', f'alt="{_h.escape(sl.get("titulo") or sl.get("barra"))}"', tag)
        tag = tag.replace('class="w-full h-full object-cover"', 'class="w-full h-full object-cover object-top"')
        return tag
    bloque = re.sub(r'<img [^>]*>', _img, bloque, count=3)
    # ventanas con link al sitio (cuando Ber los pase)
    for marca, sl in (("CARD 1:", c), ("CARD 2:", iz), ("CARD 3:", ce)):
        if sl.get("url"):
            k = bloque.find(marca); d = bloque.find("<div ", k)
            bloque = bloque[:d] + f'<a href="{sl["url"]}" target="_blank" rel="noopener" class="contents">' + bloque[d:]
            # se cierra al final de la tarjeta: la siguiente marca "<!-- CARD" o el final
            n = bloque.find("<!--", d + 10)
            cierre = bloque.rfind("</div>", d, n) + len("</div>")
            bloque = bloque[:cierre] + "</a>" + bloque[cierre:]
    bloque, js_rot = rotacion_hero(bloque, pre)
    return bloque, css, js + js_rot


def rotacion_hero(bloque, pre):
    """Las tres ventanas cambian de proyecto cada hero.SEGUNDOS (pedido de Ber, 2026-11-25).
    Los datos van en <template> (así i18n traduce los textos y ajusta las rutas de las imágenes)."""
    import hero, html as _h
    e = lambda t: _h.escape(t, quote=False)
    # marcar las tres ventanas (los <a class="contents"> que puso escenario_hero, en orden)
    n = iter(["centro", "izquierda", "celular"])
    bloque = re.sub(r'<a href="([^"]*)" target="_blank" rel="noopener" class="contents">',
                    lambda m: f'<a href="{m.group(1)}" data-slot="{next(n)}"' + ('' if not m.group(1).startswith("http") else ' target="_blank" rel="noopener"') + ' class="contents">',
                    bloque, count=3)
    plantillas = []
    for slot, lista in hero.ROTACION.items():
        items = []
        for d in lista:
            src = portfolio_web.ruta(d["img"], pre)
            campos = "".join(f'<span data-k="{k}">{e(v)}</span>' for k, v in d.items() if k not in ("img", "url"))
            items.append(f'<div data-url="{d["url"]}"><img src="{src}" alt="{e(d.get("titulo") or d.get("chip"))}"/>{campos}</div>')
        plantillas.append(f'<template data-rot="{slot}">{"".join(items)}</template>')
    bloque += "\n" + "\n".join(plantillas)
    js = """
  // ROTACIÓN de proyectos en las ventanas del hero (cada %d s, con fundido)
  (function () {
    var quieto = matchMedia('(prefers-reduced-motion: reduce)').matches;
    // qué elemento de cada ventana muestra cada dato
    var SEL = {
      centro: { barra: '.ml-space-sm', tipo: '.text-primary-container:not(.ml-space-sm)', rubro: 'span.uppercase.text-primary-container', titulo: 'h4', chip: '.rounded-full.bg-primary-container' },
      izquierda: { barra: '.text-on-surface-variant', chip: '.rounded-full.bg-secondary-container' },
      celular: { chip: '.rounded-full', titulo: '.font-headline-sm' }
    };
    var slots = [];
    document.querySelectorAll('template[data-rot]').forEach(function (t) {
      var nombre = t.dataset.rot, a = document.querySelector('a[data-slot="' + nombre + '"]');
      if (!a) return;
      var datos = [].map.call(t.content.children, function (d) {
        var o = { url: d.dataset.url, img: d.querySelector('img').getAttribute('src'), alt: d.querySelector('img').alt };
        d.querySelectorAll('[data-k]').forEach(function (s) { o[s.dataset.k] = s.textContent; });
        new Image().src = o.img;   // precarga
        return o;
      });
      var tarjeta = a.firstElementChild, img = tarjeta.querySelector('img'), fondo = img.parentElement;
      var el = {}, s = SEL[nombre];
      // centro: el rótulo de arriba a la derecha es el último span de la barra
      if (nombre === 'centro') {
        var barra = tarjeta.firstElementChild;
        el.barra = barra.querySelector('.ml-space-sm'); el.tipo = barra.lastElementChild;
        el.rubro = fondo.querySelector('span.uppercase'); el.titulo = fondo.querySelector('h4');
        el.chip = fondo.querySelector('.rounded-full');
      } else if (nombre === 'izquierda') {
        el.barra = tarjeta.firstElementChild.firstElementChild; el.chip = fondo.querySelector('.rounded-full');
      } else {
        el.chip = fondo.querySelector('.rounded-full'); el.titulo = fondo.querySelector('.font-headline-sm');
      }
      [img].concat(Object.keys(el).map(function (k) { return el[k]; })).forEach(function (x) {
        if (x) x.style.transition = 'opacity .45s ease';
      });
      slots.push({ a: a, img: img, el: el, datos: datos, i: 0 });
    });
    if (!slots.length) return;
    function poner(sl, d) {
      sl.img.src = d.img; sl.img.alt = d.alt; sl.a.href = d.url;
      if (/^https?:/.test(d.url)) { sl.a.target = '_blank'; sl.a.rel = 'noopener'; } else { sl.a.removeAttribute('target'); }
      Object.keys(sl.el).forEach(function (k) { if (sl.el[k] && d[k] != null) sl.el[k].textContent = k === 'tipo' ? d[k].toUpperCase() : d[k]; });
    }
    function visible(sl, v) {
      [sl.img].concat(Object.keys(sl.el).map(function (k) { return sl.el[k]; })).forEach(function (x) { if (x) x.style.opacity = v ? '' : '0'; });
    }
    setInterval(function () {
      if (document.hidden) return;
      slots.forEach(function (sl, n) {
        sl.i = (sl.i + 1) %% sl.datos.length;
        var d = sl.datos[sl.i];
        if (quieto) { poner(sl, d); return; }
        setTimeout(function () {
          visible(sl, false);
          setTimeout(function () { poner(sl, d); visible(sl, true); }, 450);
        }, n * 180);
      });
    }, %d);
  })();
""" % (hero.SEGUNDOS, hero.SEGUNDOS * 1000)
    return bloque, js


# ---------------------------------------------------------------- HOME
FORMAS_PROVISORIAS = [
    '<circle cx="20" cy="20" r="14" fill="none" stroke="currentColor" stroke-width="3"/>',
    '<path d="M20 5 L35 33 H5 Z" fill="none" stroke="currentColor" stroke-width="3"/>',
    '<rect x="7" y="7" width="26" height="26" rx="4" fill="none" stroke="currentColor" stroke-width="3"/>',
    '<path d="M6 30 L20 8 L34 30" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="20" cy="27" r="3" fill="currentColor"/>',
]


def tarjeta_marca(m, i, grilla=False):
    import html as _h
    caja = "bg-surface-container-lowest"
    if m["imagen"]:
        # fondo del recuadro como en el portfolio: 'claro' = logo para fondo claro; 'lamina' = la imagen trae su fondo
        tam = "max-h-20 max-w-[70%] object-contain"
        if m.get("fondo") == "claro":
            caja = "bg-[#F3F2EC]"
        elif m.get("fondo") == "lamina":
            tam = "w-full h-full object-cover"
        logo = (f'<img src="{m["imagen"]}" alt="{_h.escape(m["nombre"])}" decoding="async" '
                f'class="{tam} grayscale opacity-80 '
                'group-hover:grayscale-0 group-hover:opacity-100 transition-all duration-300"/>')
    else:
        forma = FORMAS_PROVISORIAS[i % len(FORMAS_PROVISORIAS)]
        logo = (f'<span class="flex items-center gap-space-sm text-on-surface-variant group-hover:text-primary-container transition-colors duration-300">'
                f'<svg viewBox="0 0 40 40" class="w-10 h-10" aria-hidden="true">{forma}</svg>'
                f'<span class="font-label-lg text-label-lg uppercase">{_h.escape(m["nombre"])}</span></span>')
    dentro = (f'<div class="w-full h-40 md:h-44 rounded-lg {caja} flex items-center justify-center overflow-hidden">{logo}</div>'
              f'<div class="flex flex-col gap-space-xs">'
              f'<span class="font-label-sm text-label-sm uppercase text-primary-container">{_h.escape(m["tipo"])}</span>'
              f'<p class="font-body-sm text-body-sm text-on-surface-variant">{_h.escape(m["descripcion"])}</p></div>')
    clase = ('group ' + ('w-full scroll-mt-28' if grilla else 'shrink-0 w-72 md:w-80') + ' rounded-xl bg-surface-container p-space-md md:p-space-lg flex flex-col gap-space-md '
             'shadow-lg hover:bg-surface-container-high hover:-translate-y-1 transition-all duration-300')
    marca = f' data-marca="{m["clave"]}"' if m.get("clave") else ""
    url = m.get("url")
    if grilla:
        # en la página de logos: el logo lleva a su caso de estudio si lo tiene
        url = f'casos/{m["caso"]}.html' if m.get("caso") else None
        marca += f' id="{m["clave"]}"'
    if url:
        return f'<a class="{clase}"{marca} href="{url}">{dentro}</a>'
    return f'<article class="{clase}"{marca}>{dentro}</article>'


def seccion_marcas():
    """Sección «Identidad de marca»: dos filas de logos en carrusel infinito (sentidos opuestos),
    se frena al pasar el mouse y cada logo se enciende en lima. Logos en marcas.py."""
    import html as _h
    import marcas

    def fila(lista, reversa, desde):
        items = "".join(tarjeta_marca(m, desde + k) for k, m in enumerate(lista))
        return (f'<div class="marcas-fila flex w-max gap-space-lg pr-space-lg{" marcas-reversa" if reversa else ""}">'
                f'{items}<div class="flex gap-space-lg" aria-hidden="true">{items}</div></div>')

    fila_1, fila_2 = portfolio_web.marcas()   # logos reales del portfolio (2026-11-25)
    return f"""<!-- 4b. IDENTIDAD DE MARCA (logos del portfolio, portfolio_web.py) -->
<section class="w-full py-space-3xl overflow-hidden" id="marcas">
<style>
#marcas .marcas-fila {{ animation: marquee 40s linear infinite; }}
#marcas .marcas-reversa {{ animation-direction: reverse; animation-duration: 46s; }}
#marcas .marcas-pista:hover .marcas-fila {{ animation-play-state: paused; }}
#marcas .marcas-pista {{ -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent); }}
@media (prefers-reduced-motion: reduce) {{
  #marcas .marcas-fila {{ animation: none; }}
  #marcas .marcas-pista {{ overflow-x: auto; }}
}}
</style>
<div class="px-margin-mobile md:px-margin-tablet lg:px-margin flex flex-col md:flex-row md:items-end justify-between gap-space-lg mb-space-2xl">
<div class="flex flex-col gap-space-sm">
<span class="font-label-md text-label-md uppercase text-primary-container tracking-widest">// BRANDING</span>
<h2 class="titulo-seccion font-display-lg text-display-lg-mobile md:text-display-lg text-primary uppercase tracking-tighter font-extrabold md:font-extrabold md:tracking-[-0.04em]">IDENTIDAD DE MARCA</h2>
</div>
<p class="font-body-md text-body-md text-on-surface-variant max-w-md">Logos y sistemas visuales para marcas y proyectos.</p>
</div>
<div class="marcas-pista flex flex-col gap-space-sm">
<div class="overflow-hidden py-space-sm">{fila(fila_1, False, 0)}</div>
<div class="overflow-hidden py-space-sm">{fila(fila_2, True, 2)}</div>
</div>
</section>"""



BOTON_TODOS = ('<a class="self-start md:self-auto inline-flex items-center gap-space-xs px-space-lg py-space-md rounded-full bg-surface-container-high text-primary '
               'font-label-md text-label-md uppercase tracking-wider hover:bg-surface-bright transition-colors" href="{href}">'
               '<span>{texto}</span><span class="material-symbols-outlined text-[18px]">arrow_forward</span></a>')


def home():
    s = leer("kinetic_home_proyectos_reales")
    s = comun(s, "", "Malackath · Estudio de diseño y producto digital",
              "Apps móviles, plataformas web, sistemas de reservas e identidad visual para marcas y proyectos reales. Uruguay y Brasil.")
    s = cortar(s, "<!-- 3. IMPACT METRICS -->", "<!-- 4. FEATURED REAL WORK")
    # títulos de sección con la tipografía del titular del hero (Syne 800, mismo interletrado); pedido de Ber 2026-11-24
    s = rep(s, '<h2 class="font-display-lg text-display-lg-mobile md:text-display-lg text-primary uppercase tracking-tight">',
            '<h2 class="titulo-seccion font-display-lg text-display-lg-mobile md:text-display-lg text-primary uppercase tracking-tighter font-extrabold md:font-extrabold md:tracking-[-0.04em]">', 2)
    # CTA final: «Construyamos / tu próximo / producto» en tres líneas enteras; la letra baja sola si no entra
    s, n = re.subn(r'(<div class="relative z-10 flex flex-col gap-space-md) max-w-3xl(">\s*<span[^>]*>// DISPONIBLES PARA NUEVOS PROYECTOS</span>\s*)<h2 class="font-display-xl([^"]*)">\s*CONSTRUYAMOS TU PRÓXIMO PRODUCTO\s*</h2>',
                   r'\1 w-full cta-final-col\2<h2 class="cta-final font-display-xl\3"><span class="block whitespace-nowrap">CONSTRUYAMOS</span><span class="block whitespace-nowrap">TU PRÓXIMO</span><span class="block whitespace-nowrap">PRODUCTO</span></h2>', s)
    assert n == 1, n
    s = s.replace("</style>", """
@layer base {
.cta-final-col { container-type: inline-size; }
h2.cta-final { --r: 14.4; font-size: min(2.75rem, calc(100cqw / var(--r))) !important; }
@media (min-width: 768px) { h2.cta-final { font-size: min(80px, calc(100cqw / var(--r))) !important; } }
:lang(en) h2.cta-final { --r: 9.8; }
:lang(pt) h2.cta-final { --r: 11.8; }
/* «METODOLOGÍA» es la palabra más larga: en celular y tablet la letra baja lo justo para que entre */
h2.titulo-seccion { font-size: min(clamp(1.6rem, 7.6vw, 2.25rem), calc((100vw - 40px) / 12.8)) !important; }
@media (min-width: 768px) { h2.titulo-seccion { font-size: min(3.75rem, calc((100vw - 64px) / 12.8)) !important; } }
}
</style>""", 1)
    s = rep(s, "<!-- 5. PRINCIPIOS & METODOLOGÍA -->", "<!--MARCAS-->\n<!-- 5. PRINCIPIOS & METODOLOGÍA -->")  # va después de imagenes()
    # titular: el original de Stitch (Ber, 2026-11-24: «Diseñamos productos digitales que cobran vida»)
    s = rep(s, '<div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-gutter items-center">', '<div class="hero-grilla relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-gutter items-center">')
    s = rep(s, '<p class="font-body-lg text-body-lg text-on-surface-variant max-w-2xl">', '<p class="hero-bajada font-body-lg text-body-lg text-on-surface-variant max-w-2xl">')
    # composición pedida por Ber (captura 2026-11-24): de 1280px para arriba el collage va a la derecha,
    # subido y montado sobre el titular, igual que su captura a 1512 px; los otros anchos, proporcionales.
    s = s.replace("</style>", """
/* celular: sin etiquetas flotantes ni textos sobre la captura, y sin el hueco de abajo (pedido de Ber, 2026-11-25) */
@media (max-width: 767px) {
  #showcase-viewport .float-layer-4, #showcase-viewport .float-layer-5,
  #showcase-viewport .float-layer-1 .bottom-space-md, #showcase-viewport .float-layer-1 .bg-gradient-to-t { display: none !important; }
  #showcase-viewport { min-height: 430px !important; }
}
/* sombra del titular donde pisa las capturas del collage (pedido de Ber, 2026-11-25) */
.hero-grilla h1 { text-shadow: 0 3px 10px rgba(0,0,0,.75), 0 10px 40px rgba(0,0,0,.9); }
@media (min-width: 1280px) {
  .hero-grilla { pointer-events: none; }
  .hero-grilla a { pointer-events: auto; }
  .hero-grilla h1 { font-size: 5.5556vw !important; line-height: 5.8333vw !important; }
  #showcase-viewport { position: absolute; top: calc(86px + 5.5556vw); right: -1.2vw; width: 1160px; height: auto; min-height: 680px; margin: 0;
    z-index: 0; transform: scale(var(--esc)); transform-origin: top right; }
  section:has(> #showcase-viewport) { min-height: calc(86px + 5.5556vw + 640px * var(--esc) + 40px); }
}
@media (min-width: 1280px) { section:has(> #showcase-viewport) { --esc: 0.745; } }
@media (min-width: 1366px) { section:has(> #showcase-viewport) { --esc: 0.795; } }
@media (min-width: 1440px) { section:has(> #showcase-viewport) { --esc: 0.838; } }
@media (min-width: 1512px) { section:has(> #showcase-viewport) { --esc: 0.88; } }
@media (min-width: 1600px) { section:has(> #showcase-viewport) { --esc: 0.93; } }
@media (min-width: 1680px) { section:has(> #showcase-viewport) { --esc: 0.98; } }
@media (min-width: 1800px) { section:has(> #showcase-viewport) { --esc: 1.05; } }
@media (min-width: 1920px) { section:has(> #showcase-viewport) { --esc: 1.12; } }
</style>""", 1)
    P = "img/proyectos/"
    s = imagenes(s, [
        (None, "", ""),  # logo, ya reemplazado
        (P + "armapartido-mostrador.webp", "Armá Partido: pantalla del mostrador del club con las canchas del día", "object-position:left top"),
        (P + "pizcaya-desafio.webp", "Pizcaya: desafío de 15 platos en 30 días", "object-position:center 20%"),
        (P + "cartelera-noche.webp", "Cartelera Uruguay: buscador de eventos", "object-position:left top"),
        (P + "armapartido-torneo.webp", "Torneo nocturno de pádel con tribuna llena", ""),
        (P + "pizcaya-portada.webp", "Pizcaya: cociná 15 platos de casa en 30 días", "object-position:left center"),
        (P + "palquear-estadio.webp", "Estadio de fútbol lleno de noche", ""),
        (portfolio_web.ruta(portfolio_web.imagen("ravekit", "d")), "RaveKit: sitio getravekit.com", "object-position:left top"),
        (portfolio_web.ruta("cartelera-d-04-cc7215ae.webp"), "Cartelera Uruguay: la cartelera en el mapa del país", "object-position:left top"),
        (P + "mesaluma-salon.webp", "Salón del restaurante con paredes de piedra", ""),
    ], "")
    s = celulares(s, "")
    # proyectos con caso propio: título clickeable
    s = rep(s, 'transition-colors">Armá Partido</h3>', 'transition-colors"><a href="casos/arma-partido.html">Armá Partido</a></h3>')
    s = rep(s, 'transition-colors">Pizcaya</h3>', 'transition-colors"><a href="casos/pizcaya.html">Pizcaya</a></h3>')
    # el resto de los proyectos destacados también lleva a su caso (pedido de Ber, 2026-11-25)
    for nombre, caso in [("Palquear", "palquear"), ("RaveKit", "ravekit"), ("Cartelera Uruguay", "cartelera"),
                         ("Mesaluma &amp; La Gloria", "mesaluma")]:
        s = rep(s, f'transition-colors">{nombre}</h3>', f'transition-colors"><a href="casos/{caso}.html">{nombre}</a></h3>')
    # toda la tarjeta es clickeable: el link del título se estira sobre la tarjeta
    i, j = s.find('id="proyectos"'), s.find("<!--MARCAS-->")
    bloque = re.sub(r'<article class="', '<article class="relative ', s[i:j])
    bloque = re.sub(r'(<h3 [^>]*>)<a href="casos/', r'\1<a class="tarjeta-link" href="casos/', bloque)
    assert bloque.count("tarjeta-link") == 6, bloque.count("tarjeta-link")
    s = s[:i] + bloque + s[j:]
    s = s.replace("</style>", ".tarjeta-link::after{content:'';position:absolute;inset:0;z-index:5;border-radius:inherit}</style>", 1)
    s = link(s, "<span>INICIAR PROYECTO</span>", "estudio.html#contacto")
    # Hero: las tarjetas de proyectos de la derecha se reemplazan por el escenario de ventanas
    # flotantes de la pantalla animada de Stitch (pedido de Ber, 2026-11-24). Va debajo del texto,
    # a todo el ancho, como en esa pantalla.
    bloque, css, js = escenario_hero("")
    i = s.find("<!-- Right 3D Floating Mockup Composition -->")
    j = s.find("</section>", i)
    s = s[:i] + "</div>\n" + bloque + "\n" + s[j:]   # </div> cierra la grilla del texto
    s = s.replace("</style>", css + "</style>", 1)
    s = s.replace("</body>", "<script>\n(function () {\n  " + js + "})();\n</script></body>", 1)
    s = s.replace("</body>", """<script>
(function () {
  // proporción de la captura de Ber (1440 px): el collage escala con el ancho, igual que el titular
  var sec = document.getElementById('showcase-viewport');
  if (!sec) return;
  sec = sec.closest('section');
  function ajustar() {
    if (innerWidth >= 1280) sec.style.setProperty('--esc', (0.838 * innerWidth / 1440).toFixed(4));
    else sec.style.removeProperty('--esc');
  }
  ajustar();
  addEventListener('resize', ajustar);
})();
</script></body>""", 1)
    s = rep(s, "<!--MARCAS-->", seccion_marcas())
    s = rep(s, 'href="#casos-en-vivo">\n<span>VER CASOS EN VIVO</span>', 'href="casos-de-estudio.html">\n<span>CASOS DE ESTUDIO</span>')   # nombre pedido por Ber, 2026-11-25
    # «Explorar proyectos» lleva a la página con todos los proyectos (pedido de Ber, 2026-11-25)
    s = rep(s, 'shadow-xl" href="#proyectos">\n<span>EXPLORAR PROYECTOS</span>', 'shadow-xl" href="trabajo.html">\n<span>EXPLORAR PROYECTOS</span>')
    # links a todos los proyectos y a todos los logos (pedido de Ber, 2026-11-25); botón secundario de Stitch
    s = rep(s, """<p class="font-body-md text-body-md text-on-surface-variant max-w-md">
        Cada proyecto combina estrategia de producto, diseño de interfaz de alto contraste y desarrollo listo para producción.
      </p>""", """<div class="flex flex-col gap-space-md md:items-end"><p class="font-body-md text-body-md text-on-surface-variant max-w-md">
        Cada proyecto combina estrategia de producto, diseño de interfaz de alto contraste y desarrollo listo para producción.
      </p>""" + BOTON_TODOS.format(href="trabajo.html", texto="Ver todos los proyectos") + "</div>")
    s = rep(s, '<p class="font-body-md text-body-md text-on-surface-variant max-w-md">Logos y sistemas visuales para marcas y proyectos.</p>',
            '<div class="flex flex-col gap-space-md md:items-end"><p class="font-body-md text-body-md text-on-surface-variant max-w-md">Logos y sistemas visuales para marcas y proyectos.</p>'
            + BOTON_TODOS.format(href="marcas.html", texto="Ver todos los logos") + '</div>')
    guardar("index.html", s)


# ---------------------------------------------------------- ARMÁ PARTIDO
def arma_partido():
    s = leer("kinetic_case_study_arm_partido")
    s = comun(s, "../", "Armá Partido · Caso de estudio · Malackath",
              "App para armar partidos de pádel según categoría y horarios, reuniendo cuatro jugadores y reservando cancha en el club.")
    s = cortar(s, "<!-- SECTION: IMPACT METRICS RIBBON -->", "<!-- SECTION: THE CHALLENGE")
    P = "../img/proyectos/"
    s = fondos(s, [P + "armapartido-cancha.webp", P + "armapartido-categoria.webp", P + "armapartido-horarios.webp",
                   P + "armapartido-avisos.webp", P + "armapartido-perfil.webp", None, None])
    s = link(s, "<span>VOLVER AL PORTFOLIO // CASO DE ESTUDIO 01</span>", "../casos-de-estudio.html")
    s = link(s, "<span>Visitar armapartido.com</span>", "https://armapartido.com")
    s = link(s, "SIGUIENTE CASO DE ESTUDIO // 02", "pizcaya.html")
    s = link(s, "Iniciar Proyecto\n", "../estudio.html#contacto")
    s = link(s, "Agendar Llamada", WHATSAPP)
    # testimonios inventados por Stitch: afuera (decisión de Ber)
    s = cortar(s, "<!-- SECTION: USER & CLUB TESTIMONIALS -->", "<!-- SECTION: NEXT CASE STUDY")
    # demo navegable: no existe
    s = re.sub(r'<a [^>]*href="https://demo\.armapartido\.com/"[^>]*>.*?</a>', "", s, count=1, flags=re.S)
    s = textos(s, casos_textos.ARMA_PARTIDO)
    s = panel_capturas(s, "#571BC1")
    alts = iter(casos_textos.ALT_ARMA_PARTIDO)
    s = re.sub(r'data-alt="[^"]*"', lambda m: f'data-alt="{next(alts)}"', s, count=len(casos_textos.ALT_ARMA_PARTIDO))
    guardar("casos/arma-partido.html", s)
    return s


# --------------------------------------------------------------- PIZCAYA
def pizcaya():
    s = leer("kinetic_case_study_pizcaya")
    s = comun(s, "../", "Pizcaya · Caso de estudio · Malackath",
              "Plataforma para aprender a cocinar con lecciones cortas guiadas por voz e imagen.")
    s = cortar(s, "<!-- SECTION 3: Key Impact Metrics -->", "<!-- SECTION 4: Problem Diagnosis")
    P = "../img/proyectos/"
    s = imagenes(s, [
        (None, "", ""),
        (P + "pizcaya-cocina.webp", "Mesada de cocina con luz natural", ""),
        (P + "pizcaya-pollo.webp", "Plato terminado de una receta de Pizcaya", ""),
        (P + "pizcaya-recetario.webp", "Pizcaya: recetario agrupado por tipo e ingredientes", "object-position:center top"),
        (P + "pizcaya-mesada.webp", "Pizcaya: modo cocina, armá tu mesada", "object-position:center top"),
        (P + "pizcaya-desafio.webp", "Pizcaya: desafío de 15 platos en 30 días", "object-position:center top"),
        (P + "pizcaya-inicio.webp", "Pizcaya: pantalla de inicio", "object-position:center top"),
        (None, "", ""),  # retrato de testimonio (Sample)
        (None, "", ""),  # retrato de testimonio (Sample)
    ], P and "")
    s = link(s, "VOLVER AL PORTFOLIO // CASO DE ESTUDIO 02", "../casos-de-estudio.html")
    s = link(s, "VISITAR PIZCAYA.COM", "https://pizcaya.com")
    s = link(s, "SIGUIENTE CASO DE ESTUDIO // 03", "palquear.html")
    s = cortar(s, "<!-- SECTION 7: User & Chef Testimonials -->", "<!-- SECTION 8: Next Case Study")
    s = link(s, "PROBAR MODO COCINA EN VIVO", "https://pizcaya.com")
    s = re.sub(r"Procesamiento de lenguaje natural.*?campanas\.",
               "Pasos grandes en pantalla, la app lee cada paso en voz alta y pone el reloj cuando el paso lo pide. "
               "Para avanzar alcanza con decir <em>«listo»</em>.", s, count=1, flags=re.S)
    for viejo, nuevo in (("bg-[#FF9E00]", "bg-[#E8572A]"), ("bg-[#70A040]", "bg-[#3E8E5A]"),
                         ("bg-[#121214] shadow-sm", "bg-[#FFF7EC] shadow-sm"),
                         ('bg-primary-container shadow-sm"></div>\n<span class="font-label-sm text-label-sm text-on-surface">Acid Lime',
                          'bg-[#F4B740] shadow-sm"></div>\n<span class="font-label-sm text-label-sm text-on-surface">Acid Lime')):
        s = rep(s, viejo, nuevo)
    s = textos(s, casos_textos.PIZCAYA)
    # número no confirmado
    s = rep(s, "Validado con más de 120 pruebas de usabilidad en cocina real", "Gratis, sin publicidad y sin crear cuenta")
    s = link(s, "Agendar Llamada", WHATSAPP)
    s = link(s, "Ver Todos los Casos", "../casos-de-estudio.html")
    guardar("casos/pizcaya.html", s)




# ------------------------------------------- CASOS NUEVOS (Palquear, Cartelera, Mesaluma)
# Misma plantilla de caso de Stitch que Armá Partido: se cambian textos, capturas y colores.
def _hero_caso(d, pre):
    e = html.escape
    desk, m1, m2 = (portfolio_web.ruta(x, pre) for x in d["hero"])
    tel = lambda src, alt, extra="": (
        f'<div class="w-1/2 max-w-[220px] aspect-[9/19.5] rounded-[28px] bg-surface-container-low p-[6px] shadow-xl transition-transform hover:-translate-y-1 duration-300 {extra}">'
        f'<img alt="{alt}" loading="lazy" class="w-full h-full object-cover object-top rounded-[22px]" src="{src}"/></div>')
    return f"""<!-- Hero Multi-Screen Composition Mockup -->
<div class="relative w-full rounded-xl bg-surface-container p-space-lg md:p-space-2xl overflow-hidden shadow-2xl ring-1 ring-white/10">
<!-- Subtle Ambient Backdrops -->
<div class="absolute -top-24 -left-24 w-[32rem] h-[32rem] rounded-full bg-primary-container/20 blur-[110px] pointer-events-none"></div>
<div class="absolute -bottom-32 -right-24 w-[36rem] h-[36rem] rounded-full blur-[120px] pointer-events-none" style="background:{d['colores'][0][0]};opacity:.45"></div>
<div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-space-lg items-center">
<!-- Captura real: escritorio -->
<div class="lg:col-span-8 w-full rounded-xl bg-surface-container-low p-space-md flex flex-col gap-space-sm shadow-xl transition-transform hover:-translate-y-1 duration-300">
<div class="flex items-center gap-space-xs pb-space-xs">
<span class="h-2.5 w-2.5 rounded-full bg-surface-container-highest"></span><span class="h-2.5 w-2.5 rounded-full bg-surface-container-highest"></span><span class="h-2.5 w-2.5 rounded-full bg-surface-container-highest"></span>
<span class="ml-space-sm font-label-sm text-label-sm text-on-surface-variant">{e(d["visitar"][1].split("//")[1])}</span>
</div>
<div class="w-full aspect-[16/10] rounded-lg overflow-hidden bg-surface-container-highest">
<img alt="{e(d.get('nombre', d['titulo'].title()))}: versión escritorio" loading="lazy" class="w-full h-full object-cover object-top" src="{desk}"/>
</div>
</div>
<!-- Capturas reales: celular -->
<div class="lg:col-span-4 flex items-center justify-center gap-space-md">
{tel(m1, e(d.get('nombre', d['titulo'].title())) + ": versión celular")}
{tel(m2, e(d.get('nombre', d['titulo'].title())) + ": versión celular", "lg:translate-y-space-lg")}
</div>
</div>
</div>
"""


def panel_capturas(s, color):
    """Recuadro de las capturas con presencia (pedido de Ber): tono más claro, borde fino y brillo del color de la marca."""
    s = rep(s, '<div class="relative w-full rounded-xl bg-surface-container-lowest p-space-lg md:p-space-2xl overflow-hidden shadow-2xl">',
            '<div class="relative w-full rounded-xl bg-surface-container p-space-lg md:p-space-2xl overflow-hidden shadow-2xl ring-1 ring-white/10">')
    s = rep(s, '<div class="absolute -top-24 -left-24 w-96 h-96 rounded-full bg-primary-container/10 blur-[100px] pointer-events-none"></div>\n<div class="absolute -bottom-24 -right-24 w-96 h-96 rounded-full bg-secondary-container/20 blur-[120px] pointer-events-none"></div>',
            '<div class="absolute -top-24 -left-24 w-[32rem] h-[32rem] rounded-full bg-primary-container/20 blur-[110px] pointer-events-none"></div>\n'
            f'<div class="absolute -bottom-32 -right-24 w-[36rem] h-[36rem] rounded-full blur-[120px] pointer-events-none" style="background:{color};opacity:.45"></div>')
    return s


def caso_nuevo(base, clave):
    import casos_nuevos
    d = casos_nuevos.CASOS[clave]
    e = lambda t: html.escape(t, quote=False)
    s = base
    s = rep(s, "<title>Armá Partido · Caso de estudio · Malackath</title>", f"<title>{d.get('nombre', d['titulo'].title())} · Caso de estudio · Malackath</title>")
    s = re.sub(r'<meta name="description" content="[^"]*"/>', f'<meta name="description" content="{html.escape(d["vision"])}"/>', s, count=1)
    # cabecera
    s = rep(s, "<span>VOLVER AL PORTFOLIO // CASO DE ESTUDIO 01</span>", f"<span>VOLVER AL PORTFOLIO // CASO DE ESTUDIO {d['numero']}</span>")
    s = rep(s, ">2026 — EN DESARROLLO<", f">{e(d['estado'])}<")
    s = rep(s, ">SportTech · Pádel<", f">{e(d['rubro'])}<")
    s = rep(s, "\n            ARMÁ PARTIDO\n          </h1>", f"\n            {e(d['titulo'])}\n          </h1>")
    s = rep(s, "\n            Proyecto propio · Uruguay · App instalable para clubes y jugadores\n", f"\n            {e(d['bajada'])}\n")
    s = rep(s, 'href="https://armapartido.com"', f'href="{d["visitar"][1]}"')
    s = rep(s, "<span>Visitar armapartido.com</span>", f"<span>{e(d['visitar'][0])}</span>")
    i = s.find("<!-- Services & Meta Strip -->")
    j = s.find("</section>", i)
    tira = s[i:j]
    vals = iter(d["meta"])
    tira = re.sub(r'(<span class="font-body-md text-body-md text-on-surface font-medium">)[^<]*(</span>)',
                  lambda m: m.group(1) + e(next(vals)) + m.group(2), tira)
    s = s[:i] + tira + s[j:]
    # visión
    s = re.sub(r"(La Visión</span>\s*<h2[^>]*>)\s*[^<]*(</h2>\s*<p[^>]*>)\s*[^<]*(</p>)",
               lambda m: f"{m.group(1)}\n          {e(d['vision_titulo'])}\n        {m.group(2)}\n          {e(d['vision'])}\n        {m.group(3)}", s, count=1)
    i = s.find("<!-- Hero Multi-Screen Composition Mockup -->")
    j = s.find("</section>", i)
    s = s[:i] + _hero_caso(d, "../") + "</div>\n" + s[j:]
    # textos desde «El desafío» hasta el siguiente caso, por posición (los íconos no cuentan)
    nuevos = list(d["textos"])
    for k, (_, label) in zip((47, 48, 49), d["colores"]):
        nuevos[k] = label
    ini = s.find(">Diagnóstico & Fricción<") if ">Diagnóstico & Fricción<" in s else s.find(">Diagnóstico &amp; Fricción<")
    out, last, n = [], 0, 0
    for m in re.finditer(r">([^<>]+)<", s):
        if m.start() < ini or n >= len(nuevos) or not m.group(1).strip():
            continue
        abre = s[s.rfind("<", 0, m.start() + 1):m.start() + 1]
        if "material-symbols" in abre:
            continue
        if nuevos[n] is not None:
            crudo = m.group(1)
            pre_ = crudo[:len(crudo) - len(crudo.lstrip())]
            pos_ = crudo[len(crudo.rstrip()):]
            out.append(s[last:m.start()] + ">" + pre_ + e(nuevos[n]) + pos_ + "<")
            last = m.end()
        n += 1
    if n != len(nuevos):
        raise SystemExit(f"{clave}: {n} textos en la plantilla, {len(nuevos)} en casos_nuevos")
    s = "".join(out) + s[last:]
    # íconos del desafío y los pilares (los primeros 7 después de «El desafío»)
    iconos = iter(d["iconos"])
    def _icono(m):
        if m.start() < ini:
            return m.group(0)
        sig = next(iconos, None)
        return m.group(1) + sig + m.group(3) if sig else m.group(0)
    s = re.sub(r'(<span class="material-symbols-outlined[^"]*"[^>]*>)([a-z_]+)(</span>)', _icono, s)
    # 4 pantallas: capturas de celular, alineadas arriba
    viejas = ["armapartido-categoria", "armapartido-horarios", "armapartido-avisos", "armapartido-perfil"]
    for v, nueva, tit in zip(viejas, d["pantallas"], [d["textos"][k] for k in (32, 36, 40, 44)]):
        s = re.sub(rf'class="w-full h-full bg-cover bg-center" data-alt="[^"]*" style="background-image: url\(\'\.\./img/proyectos/{v}\.webp\'\)"',
                   f'class="w-full h-full bg-cover bg-top" data-alt="{html.escape(d.get("nombre", d["titulo"].title()))}: {html.escape(tit)}" style="background-image: url(\'{portfolio_web.ruta(nueva, "../")}\')"', s, count=1)
    # colores del sistema
    for viejo, (hexa, _) in zip(("bg-primary-container", "bg-surface-container-lowest", "bg-secondary-container"), d["colores"]):
        s = rep(s, f'<span class="h-4 w-4 rounded-full {viejo}"></span>', f'<span class="h-4 w-4 rounded-full bg-[{hexa}] ring-1 ring-white/10"></span>')
    s = rep(s, 'href="pizcaya.html">\n<div class="flex flex-col md:flex-row', f'href="{d["siguiente"]}">\n<div class="flex flex-col md:flex-row')
    guardar(f"casos/{clave}.html", s)


# ---------------------------------------------------------------- TRABAJO
def trabajo():
    s = leer("kinetic_selected_work_portfolio")
    s = comun(s, "", "Trabajo · Malackath",
              "Proyectos de Malackath: apps, plataformas web, reservas e identidad visual en Uruguay y Brasil.")
    s = cortar(s, "<!-- Interactive Project Impact Showcase Sparkline Strip -->", "<!-- Quick Collaboration Banner CTA -->")
    R = [  # (viejo, nuevo, veces) ; veces 0 = todas
        # encabezado
        ("KINETIC ARCHIVE", "MALACKATH", 1), ("INDEX 02", "ARCHIVO", 1), ("CURATED SELECTION", "SELECCIÓN", 1),
        ("WebGL v2.4 Active", "Uruguay &amp; Brasil", 1), ("Grid: Asymmetric 12-Col", "Producto digital", 1),
        ("[ ARCHIVE 2022—2024 ]", "[ PROYECTOS REALES ]", 1), ("Production Grade Deployments", "En producción y demos navegables", 1),
        ("\n          SELECTED WORK\n", "\n          TRABAJO\n", 1),
        ("Total Case Files", "Proyectos", 1), ("24 PROJECTS", "6 PROYECTOS", 1),
        ("<span>All Works</span>\n<span class=\"opacity-70 font-mono\">(24)</span>", "<span>Todos</span>\n<span class=\"opacity-70 font-mono\">(6)</span>", 1),
        ("<span>Branding &amp; Identity</span>\n<span class=\"opacity-60 font-mono\">(8)</span>", "<span>Marca &amp; Web</span>\n<span class=\"opacity-60 font-mono\">(1)</span>", 1),
        ("<span>Web Experiences</span>\n<span class=\"opacity-60 font-mono\">(9)</span>", "<span>Plataformas Web</span>\n<span class=\"opacity-60 font-mono\">(3)</span>", 1),
        ("<span>Mobile &amp; Spatial Apps</span>\n<span class=\"opacity-60 font-mono\">(7)</span>", "<span>Apps Móviles</span>\n<span class=\"opacity-60 font-mono\">(2)</span>", 1),
        ("<span>Visual Grid</span>", "<span>Grilla</span>", 1), ("<span>Editorial Index</span>", "<span>Índice</span>", 1),
        # 01 Armá Partido
        ("Web &amp; Spatial AI", "SportTech · App Móvil", 2), ("AWWWARDS SOTD", "EN PRODUCCIÓN", 2),
        ("Model Inference", "Sitio", 1), ("12ms Latency", "armapartido.com", 1),
        ("Active Retention", "Plataforma", 1), ("+84% WAU", "iOS &amp; Android", 1),
        ("CLIENT: AURA LABS INC.", "PROYECTO PROPIO · MONTEVIDEO", 1),
        ("AURA AI — SPATIAL OS", "ARMÁ PARTIDO", 1),
        ("Spatial intelligence OS architecture and global brand redesign, uniting neuro-symbolic algorithms with real-time responsive WebGL UI.",
         "App para armar partidos de pádel según categoría y horarios, reuniendo cuatro jugadores y reservando cancha en el club.", 1),
        ("<span>Brand Strategy</span>", "<span>Producto</span>", 1), ("<span>Spatial UX</span>", "<span>UX/UI</span>", 1),
        ("<span>WebGL Interface</span>", "<span>App Móvil</span>", 1),
        # 02 Pizcaya
        ("\n              Web Experience\n            </span>\n<span class=\"px-space-sm py-space-xs rounded-full bg-surface-container-lowest/80 backdrop-blur-md font-label-sm text-label-sm uppercase text-primary-container font-bold\">\n              2024",
         "\n              EdTech · Web &amp; App\n            </span>\n<span class=\"px-space-sm py-space-xs rounded-full bg-surface-container-lowest/80 backdrop-blur-md font-label-sm text-label-sm uppercase text-primary-container font-bold\">\n              2024", 1),
        ("FWA OF THE DAY", "BILINGÜE ES/EN", 2), ("Configurator Orders", "Sitio", 1), ("$42M PRE-ORDERS", "pizcaya.com", 1),
        ("CHRONO MOTORS</span>", "PROYECTO PROPIO</span>", 1), ("\n              CHRONO HYPERCAR\n", "\n              PIZCAYA\n", 1),
        ("Next-generation 3D WebGL car configurator with dynamic photorealistic ray-tracing in browser.",
         "Plataforma para aprender a cocinar con lecciones cortas guiadas por voz e imagen en español e inglés.", 1),
        ("3D Three.js • WebGL", "Web &amp; App • Modo Cocina", 1),
        # 03 Palquear
        ("\n              Mobile App\n", "\n              Ticketing\n", 1), ("RED DOT 2024", "DEMO NAVEGABLE", 2),
        ("Total Volume Custody", "Sitio", 1), ("$3.2B TVL", "palquear.arnelli.com", 1),
        ("SYNAPSE CAPITAL</span>", "PROYECTO PROPIO</span>", 1), ("\n              SYNAPSE FINTECH\n", "\n              PALQUEAR\n", 1),
        ("Neo-banking interface and institutional crypto asset custody design system built for speed.",
         "Sistema de cesión y reserva de sillas de camarote para partidos de fútbol con validación por documento.", 1),
        ("Design System • iOS/Android", "Reservas • Validación por documento", 1),
        # 04 Cartelera Uruguay
        ("\n              Branding &amp; Identity\n", "\n              Cultura · Buscador Web\n", 1), ("AWWWARDS BRAND OF THE YEAR", "BUSCADOR WEB", 1),
        ("Global Reach", "Sitio", 1), ("62 Countries", "cartelerauy.malackath.com", 1),
        ("Launch Sellout", "Cobertura", 1), ("18 Minutes", "Todo Uruguay", 1),
        ("KINETIC AUDIO LAB", "PROYECTO PROPIO", 1), ("KINETIC SOUND IDENTITY", "CARTELERA URUGUAY", 1),
        ("Spatial acoustic brand identity, physical packaging ecosystem, and custom variable acoustic typeface crafted for audiophiles.",
         "Guía nacional de espectáculos y eventos con filtros por fecha, región y categoría.", 1),
        ("<span>Packaging System</span>", "<span>Buscador</span>", 1), ("<span>Variable Font</span>", "<span>Mapa</span>", 1),
        ("<span>Sonic Identity</span>", "<span>Filtros</span>", 1),
        # 05 RaveKit
        ("\n              Web Experience\n", "\n              SaaS Local · Marca &amp; Web\n", 1), ("FWA OF THE MONTH", "WHATSAPP + QR", 2),
        ("Press Mentions", "Sitio", 1), ("Architectural Digest, Dezeen", "getravekit.com", 1),
        ("VOXEL ZURICH</span>", "COMERCIOS LOCALES</span>", 1), ("\n              VOXEL ARCHITECTURE\n", "\n              RAVEKIT\n", 1),
        ("Brutalist digital portfolio featuring dynamic modular grid viewports, blueprint overlays, and kinetic parallax.",
         "Plataforma que automatiza pedidos de reseñas en Google vía WhatsApp y QR para comercios locales.", 1),
        ("Editorial Layout • Custom CMS", "Marca • Web • SaaS", 1),
        # 06 Mesaluma & La Gloria
        ("\n              Mobile &amp; Hardware UI\n", "\n              Gastronomía · Web &amp; Menú QR\n", 1), ("RED DOT BEST OF THE BEST", "PRE-ORDER", 1),
        ("Fleet Sync Protocol", "Productos", 1), ("Sub-millisecond Realtime", "Reservas &amp; Carta Digital", 1),
        ("NEXUS AUTOMATION", "RESTAURANTE &amp; CAFETERÍA", 1), ("NEXUS ROBOTICS SUITE", "MESALUMA &amp; LA GLORIA", 1),
        ("Autonomous humanoid robot control suite UI/UX, mission dispatch tablets, and telemetry telemetry HUD.",
         "Reservas con pedido anticipado para restaurantes y carta digital multilingüe para cafetería en Punta Fría.", 1),
        ("Hardware Interface • Realtime HMI", "Pre-order • Menú QR Multilingüe", 1),
        # índice (vista lista)
        ("<div class=\"col-span-4\">Project &amp; Client</div>", "<div class=\"col-span-4\">Proyecto</div>", 1),
        ("<div class=\"col-span-3\">Discipline</div>", "<div class=\"col-span-3\">Disciplina</div>", 1),
        ("<div class=\"col-span-2\">Recognition</div>", "<div class=\"col-span-2\">Estado</div>", 1),
        ("<div class=\"col-span-1 text-right\">Year</div>", "<div class=\"col-span-1 text-right\">Año</div>", 1),
        ("<div class=\"col-span-1 text-right\">Action</div>", "<div class=\"col-span-1 text-right\">Ver</div>", 1),
        (">AURA AI</span>", ">ARMÁ PARTIDO</span>", 1), ("AURA LABS • Spatial Intelligence OS", "Proyecto propio • App de pádel", 1),
        (">CHRONO HYPERCAR</span>", ">PIZCAYA</span>", 1), ("CHRONO MOTORS • 3D WebGL Configurator", "Proyecto propio • Aprender a cocinar", 1),
        (">Web Experience</div>", ">EdTech · Web &amp; App</div>", 1),
        (">SYNAPSE FINTECH</span>", ">PALQUEAR</span>", 1), ("SYNAPSE CAPITAL • Neo-banking App", "Proyecto propio • Palcos de fútbol", 1),
        (">Mobile Application</div>", ">Ticketing · Demo Navegable</div>", 1),
        (">KINETIC SOUND</span>", ">CARTELERA URUGUAY</span>", 1), ("KINETIC LABS • Spatial Audio System", "Proyecto propio • Guía de eventos", 1),
        (">Branding &amp; Identity</div>", ">Cultura · Buscador Web</div>", 1), ("BRAND OF THE YEAR", "BUSCADOR WEB", 1),
        (">VOXEL ARCHITECTURE</span>", ">RAVEKIT</span>", 1), ("VOXEL ZURICH • Brutalist Studio Hub", "Comercios locales • Reseñas en Google", 1),
        (">Web Experience</div>", ">SaaS Local · Marca &amp; Web</div>", 1),
        (">NEXUS ROBOTICS</span>", ">MESALUMA &amp; LA GLORIA</span>", 1), ("NEXUS • Autonomous Humanoid UI Suite", "Restaurante y cafetería • Reservas y carta QR", 1),
        (">Mobile &amp; Hardware UI</div>", ">Gastronomía · Web &amp; Menú QR</div>", 1), ("<span>BEST OF THE BEST</span>", "<span>PRE-ORDER</span>", 1),
        # CTA final
        ("Next Cycle Availability", "Disponibles para nuevos proyectos", 1),
        ("HAVE AN AMBITIOUS PROJECT IN MIND? LET'S TALK.", "¿TENÉS UN PROYECTO EN MENTE? HABLEMOS.", 1),
        ("We partner with daring venture founders and tier-one enterprises to build flagship digital products that redefine market categories.",
         "Acompañamos a emprendedores, marcas y comercios desde la idea hasta un producto digital funcionando.", 1),
        ("<span>Start Collaboration</span>", "<span>Iniciar Proyecto</span>", 1), ("<span>Explore Capabilities</span>", "<span>Ver Capacidades</span>", 1),
    ]
    for viejo, nuevo, n in R:
        if n == 1 and s.count(viejo) > 1:
            i = s.find(viejo)
            s = s[:i] + nuevo + s[i + len(viejo):]
        else:
            s = rep(s, viejo, nuevo, n)
    # años: los proyectos son de 2026
    i, j = s.find("<main"), s.find("<footer")
    s = s[:i] + re.sub(r"\b202[34]\b", "2026", s[i:j]) + s[j:]
    # categorías para el filtro (6 tarjetas y 6 filas, en orden)
    cats = iter(["mobile", "mobile", "web", "web", "branding", "web"] * 2)
    s = re.sub(r'data-category="[a-z]+"', lambda m: f'data-category="{next(cats)}"', s)
    # íconos de estado
    s = s.replace('text-[14px]">star</span>\n<span>EN PRODUCCIÓN', 'text-[14px]">verified</span>\n<span>EN PRODUCCIÓN')
    # links de las filas del índice
    hrefs = iter(["casos/arma-partido.html", "casos/pizcaya.html", "https://palquear.arnelli.com",
                  "https://cartelerauy.malackath.com", "https://getravekit.com", "index.html#proyectos"])
    s = re.sub(r'(<a class="list-item-row[^"]*" data-category="[a-z]+") href="#"', lambda m: f'{m.group(1)} href="{next(hrefs)}"', s)
    # títulos con caso propio
    s = rep(s, "\n              ARMÁ PARTIDO\n", '\n              <a href="casos/arma-partido.html">ARMÁ PARTIDO</a>\n')
    s = rep(s, "\n              PIZCAYA\n", '\n              <a href="casos/pizcaya.html">PIZCAYA</a>\n')
    s = link(s, "<span>Iniciar Proyecto</span>", "estudio.html#contacto")
    P = "img/proyectos/"
    s = imagenes(s, [
        (None, "", ""),
        (P + "armapartido-torneo.webp", "Torneo nocturno de pádel con tribuna llena", ""),
        (P + "pizcaya-desafio.webp", "Pizcaya: desafío de 15 platos en 30 días", "object-position:center top"),
        (P + "palquear-estadio.webp", "Estadio de fútbol lleno de noche", ""),
        (portfolio_web.ruta("cartelera-d-04-cc7215ae.webp"), "Cartelera Uruguay: la cartelera en el mapa del país", "object-position:left top"),
        (portfolio_web.ruta(portfolio_web.imagen("ravekit", "d")), "RaveKit: sitio getravekit.com", "object-position:left top"),
        (P + "mesaluma-salon.webp", "Salón del restaurante con paredes de piedra", ""),
    ], "")
    # Alinear tarjetas de la misma fila (pedido de Ber): con subgrid, imagen y texto de cada
    # tarjeta comparten las filas de la grilla, así los bloques de texto arrancan a la misma altura.
    s = s.replace('class="project-card md:col-span-', 'class="project-card md:row-span-2 md:grid md:grid-rows-subgrid md:gap-0 md:col-span-')
    s = rep(s, 'class="relative w-full aspect-[4/5] overflow-hidden', 'class="relative w-full aspect-[4/5] md:aspect-auto md:h-full overflow-hidden', 2)
    # la foto no tiene que estirar la fila: en md+ va absoluta dentro de su caja
    s = re.sub(r'(md:aspect-auto md:h-full overflow-hidden[^>]*>\s*<img[^>]*class=")w-full h-full', r'\1md:absolute md:inset-0 w-full h-full', s)
    # mismo aire arriba y abajo que las tarjetas grandes, para que rótulos y flechas queden en línea
    s = re.sub(r'(md:col-span-4 .*?class="p-space-lg) (flex flex-col justify-between flex-1)', r'\1 md:py-space-xl \2', s, flags=re.S)
    s = rep(s, "card.style.display = 'flex';", "card.style.display = '';")
    casos_general(s)
    marcas_pagina(s)
    s = trabajo_portfolio(s)
    guardar("trabajo.html", s)


def marcas_pagina(s):
    """Página «Identidad de marca» con todos los logos (pedido de Ber, 2026-11-25): el encabezado y el cierre
    de la página Trabajo de Stitch y, en lugar de las tarjetas de proyectos, la grilla de tarjetas de logo
    del carrusel del home. Cada logo lleva a su caso de estudio si lo tiene."""
    todos = portfolio_web.marcas(todos=True)
    s = s.replace("<title>Trabajo · Malackath</title>", "<title>Identidad de marca · Malackath</title>")
    s = re.sub(r'(<meta name="description" content=")[^"]*', r'\1Logos y sistemas visuales que diseñamos para marcas y proyectos.', s, count=1)
    s = rep(s, "\n          TRABAJO\n", "\n          IDENTIDAD DE MARCA\n")
    s = rep(s, "<span>SELECCIÓN</span>", "<span>BRANDING</span>")
    s = rep(s, "En producción y demos navegables", "Logos y sistemas visuales")
    s = rep(s, "6 PROYECTOS", f"{len(todos)} LOGOS")
    s = rep(s, '<span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Proyectos</span>',
            '<span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Logos</span>')
    # sin filtros ni vista índice
    i = s.find("<!-- Filter Bar & Viewport Layout Switcher -->"); j = s.find("</section>", i)
    assert 0 < i < j; s = s[:i] + s[j:]
    # grilla de logos en lugar de las tarjetas y del índice
    i = s.find("<!-- Showcase Gallery (Grid Mode Default) -->"); j = s.find("<!-- Quick Collaboration Banner CTA -->")
    assert 0 < i < j
    grilla = "".join(tarjeta_marca(m, k, grilla=True) for k, m in enumerate(todos))
    s = s[:i] + ('<!-- Logos (tarjetas del carrusel del home) -->\n'
                 '<section class="w-full px-margin-mobile md:px-margin-tablet lg:px-margin pt-space-lg pb-space-3xl">'
                 f'<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-space-lg">{grilla}</div></section>\n') + s[j:]
    s = s.replace("</head>", "<style>" + CSS_CAJA_LIMA + "</style></head>", 1)
    # en el menú no se marca «Trabajo»
    act = re.search(r'<a aria-current="page" class="([^"]*)" data-path="portfolio"', s)
    norm = re.search(r'<a class="([^"]*)" data-path="studio"', s)
    if act and norm:
        s = s.replace(act.group(0), f'<a class="{norm.group(1)}" data-path="portfolio"', 1)
    guardar("marcas.html", s)


def casos_general(s):
    """Página «Casos de estudio» (pedido de Ber, 2026-11-25): la página Trabajo de Stitch con 5 casos.
    Sale del HTML de Trabajo antes de sumarle el portfolio: mismas tarjetas, mismo encabezado."""
    s = s.replace("<title>Trabajo · Malackath</title>", "<title>Casos de estudio · Malackath</title>")
    s = re.sub(r'(<meta name="description" content=")[^"]*', r'\1Casos de estudio de Malackath: Armá Partido, Pizcaya, Palquear, Cartelera Uruguay, RaveKit y Mesaluma.', s, count=1)
    # encabezado
    s = rep(s, "\n          TRABAJO\n", "\n          CASOS DE ESTUDIO\n")
    s = rep(s, "<span>SELECCIÓN</span>", "<span>CASOS</span>")
    s = rep(s, "6 PROYECTOS", "6 CASOS")
    s = rep(s, '<span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Proyectos</span>',
            '<span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface-variant">Casos</span>')
    # sin filtros por categoría (son 6): queda solo Grilla / Índice
    s = rep(s, 'id="filter-container"', 'id="filter-container" style="visibility:hidden"')
    # RaveKit tiene caso propio desde 2026-11-25 (pedido de Ber): su tarjeta y su fila quedan
    # Mesaluma sola (La Gloria no es caso), a todo el ancho
    for viejo, nuevo in [
        ("MESALUMA &amp; LA GLORIA", "MESALUMA"),
        ("Reservas con pedido anticipado para restaurantes y carta digital multilingüe para cafetería en Punta Fría.",
         "Sistema de salón, reservas y comandas para restaurantes: app para mozos, reservas web y panel de cocina."),
        ("Gastronomía · Web &amp; Menú QR", "Gastronomía · Reservas"),
        ("RESTAURANTE &amp; CAFETERÍA", "RESTAURANTES"),
        ("Pre-order • Menú QR Multilingüe", "Reservas • Salón • Cocina"),
        ('<span class="font-label-sm text-label-sm uppercase text-on-surface-variant">Productos</span>\n<span class="font-label-md text-label-md font-bold text-primary-container">Reservas &amp; Carta Digital</span>',
         '<span class="font-label-sm text-label-sm uppercase text-on-surface-variant">Sitio</span>\n<span class="font-label-md text-label-md font-bold text-primary-container">mesaluma.arnelli.com</span>'),
        ("Restaurante y cafetería • Reservas y carta QR", "Restaurantes • Reservas y comandas"),
    ]:
        s = s.replace(viejo, nuevo)
    # numeración 01..06 // 06
    n = iter(range(1, 7))
    s = re.sub(r"\d\d // 06<", lambda m: f"{next(n):02d} // 06<", s)
    n = iter(range(1, 7))
    s = re.sub(r'(<div class="col-span-1 font-label-md text-label-md text-on-surface-variant font-mono">)\d\d(</div>)', lambda m: f"{m.group(1)}{next(n):02d}{m.group(2)}", s)
    # cada tarjeta y fila lleva a su caso
    s = rep(s, "\n              PALQUEAR\n", '\n              <a href="casos/palquear.html">PALQUEAR</a>\n')
    s = rep(s, "\n              CARTELERA URUGUAY\n", '\n              <a href="casos/cartelera.html">CARTELERA URUGUAY</a>\n')
    s = rep(s, "\n              MESALUMA\n", '\n              <a href="casos/mesaluma.html">MESALUMA</a>\n')
    s = rep(s, "\n              RAVEKIT\n", '\n              <a href="casos/ravekit.html">RAVEKIT</a>\n')
    s = rep(s, 'href="https://getravekit.com"', 'href="casos/ravekit.html"')
    s = rep(s, 'href="https://palquear.arnelli.com"', 'href="casos/palquear.html"')
    s = rep(s, 'href="https://cartelerauy.malackath.com"', 'href="casos/cartelera.html"')
    s = rep(s, 'href="index.html#proyectos"', 'href="casos/mesaluma.html"')
    s = rep(s, ">MESALUMA &amp; LA GLORIA</span>", ">MESALUMA</span>") if ">MESALUMA &amp; LA GLORIA</span>" in s else s
    # en el menú se marca «Casos» y no «Trabajo»
    act = re.search(r'<a aria-current="page" class="([^"]*)" data-path="portfolio"', s)
    norm = re.search(r'<a class="([^"]*)" data-path="case-studies"', s)
    if act and norm:
        s = s.replace(act.group(0), f'<a class="{norm.group(1)}" data-path="portfolio"', 1)
        s = s.replace(norm.group(0), f'<a aria-current="page" class="{act.group(1)}" data-path="case-studies"', 1)
    s = celulares(s, "")
    guardar("casos-de-estudio.html", s)


def celulares(s, pre):
    """Armá Partido, Palquear y Mesaluma: la foto queda y se le suma un celular con una captura real."""
    for foto, c in [("armapartido-torneo.webp", "arma-partido"), ("palquear-estadio.webp", "palquear"),
                    ("mesaluma-salon.webp", "mesaluma")]:
        s, n = re.subn(r'(<img[^>]*src="' + re.escape(pre + "img/proyectos/" + foto) + r'"[^>]*>)',
                       lambda m: m.group(1) + portfolio_web.celular(c, pre), s)
        assert n >= 1, foto
    return s.replace("</style>", portfolio_web.CSS_CELULAR + "</style>", 1)


def trabajo_portfolio(s):
    """Suma los proyectos del portfolio a Trabajo (tarjetas y filas del índice) y actualiza los contadores."""
    total = 6 + len(portfolio_web.EXTRA)
    s = celulares(s, "")
    s = re.sub(r"(\d\d) // 06<", lambda m: f"{m.group(1)} // {total:02d}<", s)
    i = s.find('id="work-grid"'); j = s.find("</article>\n</div>\n</section>", i)
    assert i > 0 and j > 0
    j += len("</article>\n")
    s = s[:j] + portfolio_web.tarjetas_extra(7, total) + s[j:]
    i = s.find('id="work-list"'); j = s.find("</a>\n</div>\n</div>\n</section>", i)
    assert i > 0 and j > 0
    j += len("</a>\n")
    s = s[:j] + portfolio_web.filas_extra(7) + s[j:]
    # contadores del filtro, contados de las tarjetas
    cats = re.findall(r'class="project-card[^"]*" data-category="([a-z]+)"', s)
    n = {k: cats.count(k) for k in ("branding", "web", "mobile")}
    s = rep(s, "6 PROYECTOS", f"{total} PROYECTOS")
    s = rep(s, '<span>Todos</span>\n<span class="opacity-70 font-mono">(6)</span>', f'<span>Todos</span>\n<span class="opacity-70 font-mono">({total})</span>')
    s = rep(s, '<span>Marca &amp; Web</span>\n<span class="opacity-60 font-mono">(1)</span>', f'<span>Marca &amp; Web</span>\n<span class="opacity-60 font-mono">({n["branding"]})</span>')
    s = rep(s, '<span>Plataformas Web</span>\n<span class="opacity-60 font-mono">(3)</span>', f'<span>Plataformas Web</span>\n<span class="opacity-60 font-mono">({n["web"]})</span>')
    s = rep(s, '<span>Apps Móviles</span>\n<span class="opacity-60 font-mono">(2)</span>', f'<span>Apps Móviles</span>\n<span class="opacity-60 font-mono">({n["mobile"]})</span>')
    return s



# ---------------------------------------------------------------- ESTUDIO
def estudio():
    guardar("estudio.html", _estudio_base("Estudio y contacto · Malackath",
            "Malackath: estudio de diseño y producto digital en Uruguay y Brasil. Marca, diseño de producto, apps y web."))


def _estudio_base(titulo, descripcion):
    s = leer("kinetic_studio_contact")
    s = comun(s, "", titulo, descripcion)
    # equipo de Stitch: personas inventadas -> se saca (PENDIENTE: ¿va Ber como fundador?)
    s = cortar(s, "<!-- Section 2: Core Visionaries / Team -->", "<!-- Section 3: Services & Capabilities")
    # presupuestos en dólares: decisión de negocio pendiente -> se saca el selector
    s = cortar(s, "<!-- Selector: Budget Range -->", "<!-- Input Fields -->")
    s = re.sub(r'<div class="flex flex-col gap-1 p-space-md bg-surface-container-lowest rounded-lg">\s*'
               r'<span class="[^"]*">TOKYO</span>.*?</div>\s*', "", s, count=1, flags=re.S)
    R = [
        ("[ 001 // THE MANIFESTO ]", "[ 001 // MANIFIESTO ]"), ("DNA &amp; PHILOSOPHY", "ADN &amp; FILOSOFÍA"),
        ("PARIS • NYC • TOKYO", "MONTEVIDEO • BRASIL"),
        ("RADICAL SIMPLICITY.", "SIMPLICIDAD RADICAL."), ("UNCOMPROMISING CRAFT.", "OFICIO SIN ATAJOS."),
        ("We reject the bloat of traditional agencies. We build high-velocity digital experiences where bleeding-edge engineering meets uncompromising art direction.",
         "Sin vueltas de agencia tradicional. Diseñamos y construimos productos digitales donde la dirección de arte y la ingeniería trabajan juntas."),
        ("Purpose Over Decoration", "Propósito antes que decoración"),
        ("Every line of code and pixel coordinates serves commercial momentum and user obsession. We strip the noise until only essential gravity remains.",
         "Cada pantalla y cada línea de código tienen que servirle a quien la usa y al negocio. Sacamos el ruido hasta que queda lo esencial."),
        ("Speed As A Feature", "La velocidad también es diseño"),
        ("60fps transitions, instant paint benchmarks, and lightning development velocity. Performance is not an afterthought; it is our primary aesthetic metric.",
         "Pantallas que cargan rápido y prototipos que se prueban en días. El rendimiento no se deja para el final."),
        ("Zero Handoff Friction", "Del diseño al código sin pérdidas"),
        ("We write production code. Designers build shaders, engineers refine typographic kerning. No lost intent between Figma files and live deployment.",
         "El mismo equipo diseña y programa, así lo que se aprueba en el diseño es lo que sale publicado."),
        ("[ 003 // EXPERTISE ]", "[ 002 // CAPACIDADES ]"), ("Capabilities Matrix", "Qué hacemos"),
        ("We deploy modular cross-disciplinary teams to eliminate translation loss between brand strategy, tactile UI, and cutting-edge interactive shaders.",
         "Marca, diseño de producto y desarrollo bajo un mismo techo, para que nada se pierda entre una etapa y la otra."),
        ("Average Delivery", "Base"), ("6 – 10 Weeks", "Montevideo, Uruguay"),
        ("Brand Identity &amp; Strategy", "Marca &amp; Estrategia"),
        ("We crystallize distinctive brand codes that dominate crowded modern markets. From positioning narratives and radical logomarks to modular kinetic identity systems.",
         "Identidades que se distinguen: desde el posicionamiento y el logo hasta el sistema visual completo y su manual."),
        (">Strategic Positioning<", ">Posicionamiento<"), (">Custom Typography<", ">Logo &amp; Símbolo<"),
        (">Kinetic Brand Guidelines<", ">Manual de Marca<"), (">Verbal Tone<", ">Tono de Voz<"),
        ("Digital Product Design (UI/UX)", "Diseño de Producto (UI/UX)"),
        ("High-fidelity digital ecosystems built around human intent and visceral tactile response. We sculpt enterprise SaaS interfaces, consumer mobile applications, and bespoke web platforms.",
         "Interfaces pensadas para el uso real: apps móviles, plataformas web y sistemas de gestión para negocios."),
        (">Product Architecture<", ">Arquitectura de Producto<"), (">Micro-Interactions<", ">Microinteracciones<"),
        (">Clickable Prototypes<", ">Prototipos Navegables<"), (">Figma Multi-Token Repos<", ">Sistemas de Diseño<"),
        ("3D &amp; Creative Dev (WebGL / Three.js)", "Apps &amp; Plataformas Web"),
        ("Breathtaking spatial web experiences engineered directly in the browser canvas. Custom GLSL fragment shaders, interactive particle clusters, and photorealistic real-time assets.",
         "Desarrollo de apps para iOS y Android, plataformas web, reservas y paneles de gestión, listos para salir a producción."),
        (">Three.js / React Three Fiber<", ">iOS &amp; Android<"), (">Custom GLSL Shaders<", ">Web Apps<"),
        (">Houdini Particle Pipes<", ">Reservas &amp; Pagos<"), (">WebGPU Acceleration<", ">Paneles de Gestión<"),
        ("Design Systems &amp; Front-End Eng", "Lanzamiento &amp; Operación"),
        ("Production-grade code architecture built to survive intense scaling. We deliver fully documented atomic components, headless integrations, and sub-second rendering.",
         "Publicamos y acompañamos: dominio, hosting, correo, tiendas de apps y medición para seguir mejorando."),
        (">Next.js / TypeScript<", ">Firebase &amp; Google Cloud<"), (">Tailwind &amp; CSS Modules<", ">Dominios &amp; Correo<"),
        (">Storybook Architecture<", ">App Store &amp; Google Play<"), (">Automated CI/CD Tests<", ">Medición<"),
        ("[ 004 // ENGAGEMENT ]", "[ 003 // CONTACTO ]"), ("Initiate A Sprint", "Iniciemos un proyecto"),
        ("Have a game-changing ambition or an urgent venture to scale? Tell us your parameters and we will outline a production roadmap within 48 hours.",
         "¿Tenés una idea o un negocio que necesita su producto digital? Contanos qué querés lograr y te respondemos con un primer camino."),
        ("Direct Priority Inbox", "Escribinos"),
        ('href="mailto:hello@kinetic.studio">\n              hello@kinetic.studio', f'href="mailto:{MAIL}">\n              {MAIL}'),
        ("Need a rapid 20-min intro?", "¿Preferís WhatsApp?"), ("Direct with a partner", "Respuesta directa"),
        ("\n              Book Call\n", "\n              Escribir\n"),
        ("Physical Hubs", "Dónde estamos"),
        (">PARIS<", ">MONTEVIDEO<"), (">Rue de Turenne<", ">Estudio<"), (">Le Marais, 75003<", ">Uruguay<"),
        (">NEW YORK<", ">BRASIL<"), (">Crosby Street<", ">Proyectos gastronómicos<"), (">SoHo, NY 10012<", ">Consultoría<"),
        ("1. What are we engineering?", "1. ¿Qué necesitás?"),
        ("\n                Brand Identity\n", "\n                Marca\n"), ("\n                Web Design\n", "\n                Sitio Web\n"),
        ("\n                Mobile App\n", "\n                App Móvil\n"), ("\n                Design System\n", "\n                Plataforma / Sistema\n"),
        ("\n                Full Retainer\n", "\n                Acompañamiento Mensual\n"),
        (">Your Name *<", ">Tu nombre *<"), (">Work Email *<", ">Tu email *<"),
        (">Project Synopsis &amp; Objectives *<", ">Contanos el proyecto *<"),
        ('placeholder="Alex Morgan"', 'placeholder="Nombre y apellido"'), ('placeholder="alex@entity.xyz"', 'placeholder="nombre@empresa.com"'),
        ('placeholder="Tell us about the challenge, target timeline, and the desired outcome..."',
         'placeholder="Qué querés lograr, para cuándo y cualquier referencia que tengas..."'),
        ("Strict NDA preserved on all incoming drafts.", "Tus datos solo se usan para responderte."),
        ("<span>Send Project Proposal</span>", "<span>Enviar Proyecto</span>"),
        ("Inquiry received. A Kinetic partner will review and respond shortly.", "Listo: se abrió tu correo con el mensaje armado para enviarlo."),
        ("`<span>Transmitting Payload...</span>`", "`<span>Abriendo tu correo...</span>`"),
    ]
    for viejo, nuevo in R:
        s = rep(s, viejo, nuevo)
    s = link(s, "\n              Escribir\n", WHATSAPP)
    # acceso al formulario de presupuesto: mismo bloque de Stitch que "¿Preferís WhatsApp?"
    s = rep(s, "<!-- Quick Calendar Booking Link -->",
            '<div class="p-space-lg bg-surface-container rounded-xl flex items-center justify-between gap-space-md">'
            '<div class="flex flex-col"><span class="font-headline-sm text-headline-sm uppercase text-primary">¿Querés un presupuesto?</span>'
            '<span class="font-label-sm text-label-sm text-on-surface-variant">Armalo en cuatro pasos</span></div>'
            '<a class="shrink-0 px-space-md py-space-xs rounded-full bg-primary-container text-on-primary-fixed hover:bg-primary-fixed-dim font-label-sm text-label-sm uppercase transition-all duration-300" href="presupuesto.html">Armar</a>'
            '</div>\n<!-- Quick Calendar Booking Link -->')
    # anclas para el menú
    s = rep(s, '<section class="w-full px-margin-mobile md:px-margin-tablet lg:px-margin py-space-3xl relative">\n<div class="grid grid-cols-1 lg:grid-cols-12',
            '<section id="capacidades" class="w-full px-margin-mobile md:px-margin-tablet lg:px-margin py-space-3xl relative">\n<div class="grid grid-cols-1 lg:grid-cols-12')
    s = rep(s, 'id="inquiry">', 'id="inquiry"><a id="contacto"></a>')
    # el formulario no tiene servidor: arma un mail con los datos (sin backend, pedido de Ber)
    s = rep(s, "      btn.classList.add('hidden');\n      banner.classList.remove('hidden');",
            "      const tipo = (document.querySelector('.chip-item.active') || {}).textContent || '';\n"
            "      const nombre = document.getElementById('contact-name').value;\n"
            "      const email = document.getElementById('contact-email').value;\n"
            "      const texto = document.getElementById('contact-brief').value;\n"
            f"      location.href = 'mailto:{MAIL}?subject=' + encodeURIComponent('Proyecto: ' + tipo.trim() + ' / ' + nombre) +\n"
            "        '&body=' + encodeURIComponent(texto + '\\n\\n' + nombre + ' (' + email + ')');\n"
            "      btn.classList.add('hidden');\n      banner.classList.remove('hidden');")
    return s


# ---------------------------------------------------------------- SERVICIOS
# Página propia de Servicios (Ber, 2026-11-25: el menú «Servicios» caía a la mitad de Estudio).
# Mismas piezas de la pantalla Estudio de Stitch (encabezado, tarjetas, lista de capacidades, contacto),
# sin el manifiesto de Estudio. Las 4 áreas van abiertas y más desarrolladas.
SERV_FORMAS = [
    ("task_alt", "Proyecto cerrado", "Alcance, plazos y precio definidos por escrito antes de empezar. Para cuando ya sabés lo que necesitás."),
    ("schedule", "Por horas", "Para proyectos que van cambiando sobre la marcha: trabajamos por horas con un informe claro de lo hecho."),
    ("autorenew", "Acompañamiento mensual", "Una cuota fija con horas incluidas cada mes para mantener, actualizar y mejorar tu sitio o tu app."),
]
SERV_AREAS = [
    ("Marca &amp; Estrategia",
     "Identidades que se distinguen: desde el posicionamiento y el logo hasta el sistema visual completo y su manual, listas para usar en la web, en la app y en redes.",
     ["Posicionamiento", "Logo &amp; Símbolo", "Paleta &amp; Tipografías", "Manual de Marca", "Tono de Voz", "Piezas para Redes"],
     ("Ver identidades de marca", "marcas.html")),
    ("Diseño de Producto (UI/UX)",
     "Interfaces pensadas para el uso real: apps móviles, plataformas web y sistemas de gestión para negocios. Antes de programar, probás un prototipo navegable.",
     ["Arquitectura de Producto", "Flujos &amp; Wireframes", "Prototipos Navegables", "Microinteracciones", "Sistemas de Diseño", "Diseño Responsive"],
     ("Ver casos de estudio", "casos-de-estudio.html")),
    ("Apps &amp; Plataformas Web",
     "Desarrollo de apps para iOS y Android, sitios, tiendas online, plataformas con reservas y pagos y paneles de gestión, en varios idiomas y listos para salir a producción.",
     ["iOS &amp; Android", "Web Apps", "Sitios Web", "Tiendas Online", "Reservas &amp; Pagos", "Paneles de Gestión", "Multilenguaje"],
     ("Ver proyectos", "trabajo.html")),
    ("Lanzamiento &amp; Operación",
     "Publicamos y acompañamos: dominio, hosting, correo, tiendas de apps y medición. Con el acompañamiento mensual, tu producto queda monitoreado, con respaldos y actualizaciones.",
     ["Firebase &amp; Google Cloud", "Cloudflare", "Dominios &amp; Correo", "App Store &amp; Google Play", "Medición", "Respaldos &amp; Seguridad", "Mantenimiento Mensual"],
     ("Armá tu presupuesto", "presupuesto.html")),
]
SERV_PASOS = [
    ("forum", "Conversación", "Nos contás qué querés lograr, para quién y para cuándo. Sin compromiso."),
    ("description", "Propuesta", "Te mandamos alcance, plazos y precio por escrito, para que decidas con todo claro."),
    ("draw", "Diseño", "Marca y pantallas en un prototipo navegable que probás antes de programar."),
    ("code", "Desarrollo", "Construimos y te mostramos versiones de prueba para que veas el avance real."),
    ("rocket_launch", "Lanzamiento", "Salimos a producción y, si querés, seguimos con el acompañamiento mensual."),
]
TARJ = "group relative bg-surface-container rounded-xl flex flex-col justify-between hover:bg-surface-container-high transition-all duration-300"
RAYA = '<div class="h-1 w-8 bg-surface-container-highest group-hover:w-full group-hover:bg-primary-container transition-all duration-500 rounded-full"></div>'
CHIP_SERV = "font-label-sm text-label-sm uppercase px-space-sm py-1 bg-surface-container-high text-on-surface rounded-full"


def servicios():
    s = _estudio_base("Servicios · Malackath",
                      "Servicios de Malackath: marca, diseño de producto, apps y plataformas web, lanzamiento y acompañamiento mensual.")
    # menú: activo «Servicios» en vez de «Estudio»
    i, j = s.find("<nav "), s.find("</nav>")
    nav = s[i:j]
    act = re.search(r'<a aria-current="page" class="([^"]*)" data-path="studio"', nav).group(1)
    nor = re.search(r'<a class="([^"]*)" data-path="services"', nav).group(1)
    nav = nav.replace(f'<a aria-current="page" class="{act}" data-path="studio"', f'<a class="{nor}" data-path="studio"', 1)
    nav = nav.replace(f'<a class="{nor}" data-path="services"', f'<a aria-current="page" class="{act}" data-path="services"', 1)
    s = s[:i] + nav + s[j:]
    # 1) encabezado: mismo bloque del manifiesto, con texto de Servicios y las 3 formas de trabajar
    s = rep(s, "[ 001 // MANIFIESTO ]", "[ 001 // SERVICIOS ]")
    s = rep(s, "ADN &amp; FILOSOFÍA", "FORMAS DE TRABAJAR")
    s = rep(s, "SIMPLICIDAD RADICAL.", "SERVICIOS.")
    s = rep(s, "OFICIO SIN ATAJOS.", "DE LA IDEA AL PRODUCTO.")
    s = rep(s, "Sin vueltas de agencia tradicional. Diseñamos y construimos productos digitales donde la dirección de arte y la ingeniería trabajan juntas.",
            "Marca, diseño de producto y desarrollo bajo un mismo techo. Te acompañamos desde la primera idea hasta el producto funcionando, y después también.")
    tarjetas = "".join(
        f'<div class="{TARJ} p-space-lg md:p-space-xl gap-space-xl"><div class="flex items-center justify-between">'
        f'<span class="font-label-lg text-label-lg text-primary-container tracking-widest">0{n}</span>'
        f'<span class="material-symbols-outlined text-on-surface-variant group-hover:text-primary transition-colors">{ic}</span></div>'
        f'<div class="flex flex-col gap-space-sm"><h3 class="font-headline-md text-headline-sm md:text-headline-md uppercase tracking-tight text-primary">{t}</h3>'
        f'<p class="font-body-md text-body-md text-on-surface-variant leading-relaxed">{d}</p></div>{RAYA}</div>'
        for n, (ic, t, d) in enumerate(SERV_FORMAS, 1))
    s, n = re.subn(r'(<!-- Values Grid: Asymmetric Triple Modules -->\s*<div class="grid grid-cols-1 md:grid-cols-3 gap-gutter pt-space-lg">).*?(</div>\s*</div>\s*</section>)',
                   lambda m: m.group(1) + tarjetas + m.group(2), s, count=1, flags=re.S)
    assert n == 1, "servicios: tarjetas"
    # 2) capacidades: las 4 áreas abiertas y desarrolladas
    areas = ""
    for k, (t, d, chips, (lt, lh)) in enumerate(SERV_AREAS, 1):
        areas += (f'<div class="accordion-item bg-surface-container rounded-xl overflow-hidden transition-all duration-300">'
                  f'<div class="w-full p-space-lg md:p-space-xl pb-space-md md:pb-space-md flex items-center gap-space-md">'
                  f'<span class="font-label-sm text-label-sm text-primary-container">[ 0{k} ]</span>'
                  f'<h3 class="font-headline-md text-headline-md uppercase text-primary">{t}</h3></div>'
                  f'<div class="accordion-body px-space-lg md:px-space-xl pb-space-lg md:pb-space-xl flex flex-col gap-space-md">'
                  f'<p class="font-body-lg text-body-lg text-on-surface-variant">{d}</p>'
                  f'<div class="flex flex-wrap gap-space-xs pt-space-xs">' + "".join(f'<span class="{CHIP_SERV}">{c}</span>' for c in chips) + '</div>'
                  f'<a class="self-start inline-flex items-center gap-space-xs pt-space-sm font-label-md text-label-md uppercase tracking-wider text-primary-container hover:text-primary transition-colors" href="{lh}">'
                  f'<span>{lt}</span><span class="material-symbols-outlined text-[18px]">arrow_forward</span></a></div></div>')
    s, n = re.subn(r'(<div class="lg:col-span-8 flex flex-col gap-space-sm" id="services-accordion">).*?(</div>\s*</div>\s*</section>)',
                   lambda m: m.group(1) + areas + m.group(2), s, count=1, flags=re.S)
    assert n == 1, "servicios: áreas"
    # 3) proceso, antes del contacto (mismas tarjetas del encabezado)
    pasos = "".join(
        f'<div class="{TARJ} p-space-lg gap-space-lg"><div class="flex items-center justify-between">'
        f'<span class="font-label-lg text-label-lg text-primary-container tracking-widest">0{n}</span>'
        f'<span class="material-symbols-outlined text-on-surface-variant group-hover:text-primary transition-colors">{ic}</span></div>'
        f'<div class="flex flex-col gap-space-sm"><h3 class="font-headline-sm text-headline-sm uppercase tracking-tight text-primary">{t}</h3>'
        f'<p class="font-body-sm text-body-sm text-on-surface-variant leading-relaxed">{d}</p></div>{RAYA}</div>'
        for n, (ic, t, d) in enumerate(SERV_PASOS, 1))
    proceso = ('<section id="proceso" class="w-full px-margin-mobile md:px-margin-tablet lg:px-margin pb-space-3xl relative">'
               '<div class="flex flex-col gap-space-xl"><div class="flex flex-col gap-space-lg max-w-2xl">'
               '<span class="font-label-sm text-label-sm uppercase tracking-widest text-primary-container">[ 003 // PROCESO ]</span>'
               '<h2 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg uppercase text-primary tracking-tight">Cómo trabajamos</h2>'
               '<p class="font-body-md text-body-md text-on-surface-variant">Cinco pasos, siempre con algo concreto para ver y aprobar antes de seguir.</p></div>'
               f'<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-gutter">{pasos}</div></div></section>\n')
    s = rep(s, "<!-- Section 4: High-Converting Inquiry & Contact Section -->", proceso + "<!-- Section 4: High-Converting Inquiry & Contact Section -->")
    s = rep(s, "[ 003 // CONTACTO ]", "[ 004 // CONTACTO ]")
    s = s.replace('<section id="capacidades" ', '<section id="areas" ', 1)
    s = s.replace('id="inquiry"><a id="contacto"></a>', 'id="inquiry">', 1)
    guardar("servicios.html", s)


# ------------------------------------------------------------- PRESUPUESTO
# Formulario "Armá tu presupuesto" (como el de Marea Alta, aprobado por Ber 2026-11-25 con wireframe).
# No hay pantalla de Stitch para esto: se arma con los mismos componentes del formulario de contacto
# de la pantalla Estudio (chips, campos, botón, bloques) para no salirse del sistema.
CHIP = "px-space-md py-space-xs rounded-full font-label-sm text-label-sm uppercase transition-all duration-200"
CHIP_OFF = "bg-surface-container-high text-on-surface hover:text-primary"
CAMPO = ("w-full bg-surface-container-lowest px-space-md py-space-sm rounded-lg text-primary placeholder-on-surface-variant/40 "
         "font-body-md text-body-md focus:outline-none focus:ring-2 focus:ring-primary-container transition-all")
ETQ = "font-label-sm text-label-sm uppercase text-on-surface-variant"
AREAS = [  # las 4 áreas de la página Estudio, con sus servicios
    ("Marca &amp; Estrategia", ["Posicionamiento", "Logo &amp; Símbolo", "Manual de Marca", "Tono de Voz"]),
    ("Diseño de Producto (UI/UX)", ["Arquitectura de Producto", "Microinteracciones", "Prototipos Navegables", "Sistemas de Diseño"]),
    ("Apps &amp; Plataformas Web", ["iOS &amp; Android", "Web Apps", "Reservas &amp; Pagos", "Paneles de Gestión"]),
    ("Lanzamiento &amp; Operación", ["Firebase &amp; Google Cloud", "Dominios &amp; Correo", "App Store &amp; Google Play", "Medición", "Mantenimiento mensual"]),
]


def _chips(grupo, opciones, multi=False):
    b = "".join(f'<button type="button" class="pz-chip {CHIP} {CHIP_OFF}" data-grupo="{grupo}"{" data-multi" if multi else ""}>{o}</button>'
                for o in opciones)
    return f'<div class="flex flex-wrap gap-space-xs">{b}</div>'


def _paso(n, titulo, cuerpo, oculto=True):
    return (f'<div class="pz-paso flex flex-col gap-space-lg{" hidden" if oculto else ""}" data-paso="{n}">'
            f'<span class="font-label-sm text-label-sm uppercase tracking-wider text-primary-container">Paso 0{n} / 04</span>'
            f'<h3 class="font-headline-sm text-headline-sm uppercase text-primary">{titulo}</h3>{cuerpo}</div>')


def _campo(id_, etq, ph="", tipo="text", req=True, area=False):
    r = ' required=""' if req else ""
    ctrl = (f'<textarea class="{CAMPO} resize-none" id="{id_}" rows="4" placeholder="{ph}"{r}></textarea>' if area else
            f'<input class="{CAMPO}" id="{id_}" type="{tipo}" placeholder="{ph}"{r}>')
    return f'<div class="flex flex-col gap-space-xs"><label class="{ETQ}" for="{id_}">{etq}</label>{ctrl}</div>'


def presupuesto():
    s = leer("kinetic_studio_contact")
    s = comun(s, "", "Armá tu presupuesto · Malackath",
              "Marcá lo que necesitás y te mandamos una propuesta con alcance, plazos y precio. Sin compromiso.")
    p1 = (f'<div class="flex flex-col gap-space-sm"><span class="{ETQ}" data-et="tipo">¿Qué querés hacer? *</span>'
          + _chips("tipo", ["App Móvil", "Plataforma Web", "Sitio Web", "Tienda Online", "Marca", "Otro"]) + '</div>'
          f'<div class="flex flex-col gap-space-sm"><span class="{ETQ}" data-et="etapa">¿En qué etapa está? *</span>'
          + _chips("etapa", ["Es una idea", "Tengo el diseño", "Ya funciona: hay que mejorarlo o mantenerlo"]) + '</div>')
    p2 = f'<p class="font-body-md text-body-md text-on-surface-variant">Marcá todo lo que quieras cotizar. Podés combinar áreas.</p>'
    for i, (area, servs) in enumerate(AREAS, 1):
        p2 += (f'<div class="flex flex-col gap-space-sm"><span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface">[ 0{i} ] {area}</span>'
               + _chips("servicios", servs, multi=True) + '</div>')
    p3 = (f'<div class="flex flex-col gap-space-sm"><span class="{ETQ}" data-et="plazo">¿Para cuándo? *</span>'
          + _chips("plazo", ["Sin apuro", "En 1 a 2 meses", "Urgente"]) + '</div>'
          f'<div class="flex flex-col gap-space-sm"><span class="{ETQ}" data-et="modo">¿Cómo preferís trabajar? *</span>'
          + _chips("modo", ["Precio cerrado", "Por horas", "Recomiéndenme"]) + '</div>')
    p4 = ('<div class="grid grid-cols-1 md:grid-cols-2 gap-space-md">'
          + _campo("pz-nombre", "Tu nombre *", "Nombre y apellido")
          + _campo("pz-empresa", "Empresa o proyecto", "Nombre de la empresa", req=False)
          + _campo("pz-pais", "País *", "Uruguay, Brasil...")
          + _campo("pz-whatsapp", "WhatsApp *", "+598 ...", tipo="tel")
          + '</div>' + _campo("pz-email", "Tu email *", "nombre@empresa.com", tipo="email")
          + _campo("pz-mensaje", "Algo más que quieras contarnos", "Referencias, objetivos, fechas...", req=False, area=True))
    form = (
        '<div class="lg:col-span-7 bg-surface-container rounded-xl p-space-xl md:p-space-2xl shadow-xl flex flex-col gap-space-xl">'
        '<ol class="grid grid-cols-4 gap-space-xs" id="pz-pasos">'
        + "".join(f'<li class="pz-tab border-t-2 pt-space-xs font-label-sm text-label-sm uppercase {"border-primary-container text-primary" if n == 1 else "border-surface-container-highest text-on-surface-variant"}" data-tab="{n}">0{n} {t}</li>'
                  for n, t in enumerate(["Proyecto", "Servicios", "Plazo", "Datos"], 1))
        + '</ol>'
        '<form class="flex flex-col gap-space-xl" id="pz-form" novalidate>'
        + _paso(1, "¿Qué es tu proyecto?", p1, oculto=False) + _paso(2, "¿Qué necesitás?", p2)
        + _paso(3, "¿Para cuándo y cómo?", p3) + _paso(4, "¿A quién le mandamos la propuesta?", p4)
        + '<p class="hidden font-body-sm text-body-sm text-error" id="pz-error">Completá lo marcado con * para seguir.</p>'
        '<div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-space-md pt-space-xs" id="pz-nav">'
        f'<button type="button" class="invisible {CHIP} {CHIP_OFF} inline-flex items-center gap-space-xs" id="pz-atras"><span class="material-symbols-outlined text-[18px]">arrow_back</span><span>Volver</span></button>'
        '<button class="group relative inline-flex items-center justify-center gap-space-sm px-space-xl py-space-md rounded-full bg-primary-container text-on-primary-fixed font-label-md text-label-md uppercase tracking-wider hover:bg-primary-fixed-dim transition-all duration-300 transform active:scale-95 shadow-lg shadow-primary-container/10" id="pz-seguir" type="button">'
        '<span>Seguir</span><span class="material-symbols-outlined text-[18px] group-hover:translate-x-1 transition-transform">arrow_forward</span></button>'
        '</div>'
        '<div class="hidden flex-col gap-space-md" id="pz-enviar">'
        '<span class="font-label-sm text-label-sm uppercase tracking-wider text-on-surface">¿Por dónde nos lo mandás?</span>'
        '<div class="flex flex-col sm:flex-row gap-space-md">'
        '<a class="group inline-flex items-center justify-center gap-space-sm px-space-xl py-space-md rounded-full bg-primary-container text-on-primary-fixed font-label-md text-label-md uppercase tracking-wider hover:bg-primary-fixed-dim transition-all duration-300" id="pz-wa" href="#" target="_blank" rel="noopener"><span>Enviar por WhatsApp</span><span class="material-symbols-outlined text-[18px]">north_east</span></a>'
        '<a class="inline-flex items-center justify-center gap-space-sm px-space-xl py-space-md rounded-full bg-surface-container-high text-primary hover:bg-primary-container hover:text-on-primary-fixed font-label-md text-label-md uppercase tracking-wider transition-all duration-300" id="pz-mail" href="#"><span>Enviar por email</span><span class="material-symbols-outlined text-[18px]">mail</span></a>'
        '</div>'
        '<div class="p-space-md bg-surface-container-highest rounded-lg flex items-center gap-space-sm text-primary">'
        '<span class="material-symbols-outlined text-primary-container">check_circle</span>'
        '<span class="font-body-md text-body-md">Se abre tu WhatsApp o tu correo con el pedido ya escrito: solo tenés que enviarlo. Lo revisamos y te mandamos la propuesta.</span></div>'
        '</div>'
        '</form>'
        # textos que usa el mensaje (se traducen con el resto de la página)
        '<div class="hidden" id="pz-txt"><span data-t="titulo">Pedido de presupuesto</span><span data-t="servicios">Servicios</span>'
        '<span data-t="nombre">Nombre</span><span data-t="empresa">Empresa</span><span data-t="pais">País</span>'
        '<span data-t="email">Email</span><span data-t="mensaje">Mensaje</span><span data-t="codigo">Código para la propuesta (no borrar)</span></div>'
        '</div>')
    izq = (
        '<div class="lg:col-span-5 flex flex-col gap-space-lg">'
        '<div class="flex flex-col gap-space-xs"><span class="font-label-sm text-label-sm uppercase tracking-widest text-primary-container">[ PRESUPUESTO ]</span>'
        '<h1 class="font-headline-lg text-headline-lg-mobile md:text-headline-lg uppercase text-primary tracking-tight">Armá tu presupuesto</h1></div>'
        '<p class="font-body-lg text-body-lg text-on-surface-variant">Marcá lo que necesitás. Revisamos tu pedido a mano y te mandamos una propuesta con alcance, plazos y precio. Sin compromiso y sin precios automáticos.</p>'
        '<ol class="flex flex-col gap-space-sm mt-space-md">'
        + "".join(f'<li class="p-space-md bg-surface-container-lowest rounded-lg flex gap-space-md"><span class="font-label-sm text-label-sm text-primary-container">0{n}</span>'
                  f'<span class="flex flex-col gap-1"><span class="font-body-md text-body-md text-on-surface">{a}</span><span class="font-label-sm text-label-sm text-on-surface-variant">{b}</span></span></li>'
                  for n, (a, b) in enumerate([("Marcás lo que necesitás", "En cuatro pasos, sin compromiso."),
                                              ("Lo revisamos", "Si hace falta, te escribimos para aclarar algo."),
                                              ("Te llega la propuesta", "Con alcance, plazos y precio, por escrito.")], 1))
        + '</ol>'
        '<div class="p-space-lg bg-surface-container rounded-xl flex items-center justify-between">'
        '<div class="flex flex-col"><span class="font-headline-sm text-headline-sm uppercase text-primary">¿Preferís hablar?</span>'
        '<span class="font-label-sm text-label-sm text-on-surface-variant">Respuesta directa</span></div>'
        f'<a class="px-space-md py-space-xs rounded-full bg-surface-container-high text-primary hover:bg-primary-container hover:text-on-primary-fixed font-label-sm text-label-sm uppercase transition-all duration-300" href="{WHATSAPP}" target="_blank" rel="noopener">WhatsApp</a>'
        '</div></div>')
    seccion = ('<section class="w-full px-margin-mobile md:px-margin-tablet lg:px-margin pt-space-xl pb-space-3xl bg-surface-container-low relative overflow-hidden" id="presupuesto">'
               '<div class="absolute bottom-0 right-0 w-[45rem] h-[45rem] bg-primary-container/10 rounded-full blur-[170px] pointer-events-none"></div>'
               '<div class="grid grid-cols-1 lg:grid-cols-12 gap-space-2xl relative z-10">' + izq + form + '</div></section>')
    i, j = s.find('<main class="w-full pt-20 bg-background">'), s.find("</main>")
    if i < 0 or j < 0:
        raise SystemExit("presupuesto: no encontré <main>")
    s = s[:i] + '<main class="w-full pt-20 bg-background">' + seccion + s[j:]
    js = """<script>
(() => {
  const WA = '%s', MAIL = '%s';
  const ON = '%s'.split(' '), OFF = '%s'.split(' ');
  let paso = 1;
  const $ = q => document.querySelector(q), $$ = q => [...document.querySelectorAll(q)];
  const t = k => ($('#pz-txt [data-t="' + k + '"]') || {}).textContent || k;
  const marcar = (b, on) => { ON.forEach(c => b.classList.toggle(c, on)); OFF.forEach(c => b.classList.toggle(c, !on)); b.setAttribute('aria-pressed', on); b.dataset.on = on ? '1' : ''; };
  $$('.pz-chip').forEach(b => b.addEventListener('click', () => {
    if (b.hasAttribute('data-multi')) return marcar(b, !b.dataset.on);
    $$('.pz-chip[data-grupo="' + b.dataset.grupo + '"]').forEach(x => marcar(x, x === b));
  }));
  const elegidos = g => $$('.pz-chip[data-grupo="' + g + '"]').filter(b => b.dataset.on).map(b => b.textContent.trim());
  const val = id => ($('#' + id).value || '').trim();
  function valido(n) {
    if (n === 1) return elegidos('tipo').length && elegidos('etapa').length;
    if (n === 2) return elegidos('servicios').length;
    if (n === 3) return elegidos('plazo').length && elegidos('modo').length;
    return val('pz-nombre') && val('pz-pais') && val('pz-whatsapp') && /.+@.+\\..+/.test(val('pz-email'));
  }
  function ir(n) {
    paso = n;
    $$('.pz-paso').forEach(p => p.classList.toggle('hidden', +p.dataset.paso !== n));
    $$('.pz-tab').forEach(x => { const on = +x.dataset.tab <= n;
      ['border-primary-container', 'text-primary'].forEach(c => x.classList.toggle(c, on));
      ['border-surface-container-highest', 'text-on-surface-variant'].forEach(c => x.classList.toggle(c, !on)); });
    $('#pz-atras').classList.toggle('invisible', n === 1);
    $('#pz-error').classList.add('hidden');
    $('#presupuesto').scrollIntoView({ behavior: 'smooth' });
  }
  function codigo(d) {
    const b = new TextEncoder().encode(JSON.stringify(d)); let s = '';
    b.forEach(x => s += String.fromCharCode(x));
    return 'MLK1:' + btoa(s).replace(/\\+/g, '-').replace(/\\//g, '_');
  }
  function preparar() {
    const d = { v: 1, idioma: document.documentElement.lang, tipo: elegidos('tipo')[0], etapa: elegidos('etapa')[0],
      servicios: elegidos('servicios'), plazo: elegidos('plazo')[0], modo: elegidos('modo')[0],
      nombre: val('pz-nombre'), empresa: val('pz-empresa'), pais: val('pz-pais'), whatsapp: val('pz-whatsapp'),
      email: val('pz-email'), mensaje: val('pz-mensaje') };
    const et = k => (($('[data-et="' + k + '"]') || {}).textContent || k).replace(/\\s*\\*$/, '');
    const txt = [t('titulo'), '',
      et('tipo') + ' ' + d.tipo, et('etapa') + ' ' + d.etapa,
      t('servicios') + ': ' + d.servicios.join(', '),
      et('plazo') + ' ' + d.plazo, et('modo') + ' ' + d.modo, '',
      t('nombre') + ': ' + d.nombre, d.empresa ? t('empresa') + ': ' + d.empresa : null, t('pais') + ': ' + d.pais,
      'WhatsApp: ' + d.whatsapp, t('email') + ': ' + d.email, d.mensaje ? t('mensaje') + ': ' + d.mensaje : null, '',
      t('codigo') + ':', codigo(d)].filter(x => x != null).join('\\n');
    $('#pz-wa').href = WA + '?text=' + encodeURIComponent(txt);
    $('#pz-mail').href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(t('titulo') + ': ' + (d.empresa || d.nombre)) + '&body=' + encodeURIComponent(txt);
    $('#pz-nav').classList.add('hidden');
    $('#pz-enviar').classList.remove('hidden'); $('#pz-enviar').classList.add('flex');
  }
  $('#pz-seguir').addEventListener('click', () => {
    if (!valido(paso)) { $('#pz-error').classList.remove('hidden'); return; }
    if (paso < 4) ir(paso + 1); else preparar();
  });
  $('#pz-atras').addEventListener('click', () => paso > 1 && ir(paso - 1));
  const q = new URLSearchParams(location.search).get('tipo');
  if (q) $$('.pz-chip[data-grupo="tipo"]').forEach(b => b.textContent.trim() === q && marcar(b, true));
})();
</script>""" % (WHATSAPP, MAIL, "bg-primary-container text-on-primary-fixed", CHIP_OFF)
    s = s.replace("</body>", js + "</body>", 1)
    guardar("presupuesto.html", s)


if __name__ == "__main__":
    home()
    base_caso = arma_partido()
    pizcaya()
    for clave in ("palquear", "cartelera", "mesaluma", "ravekit"):
        caso_nuevo(base_caso, clave)
    trabajo()
    estudio()
    servicios()
    portfolio_web.copiar(OUT)
    presupuesto()
