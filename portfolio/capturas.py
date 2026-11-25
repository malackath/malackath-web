#!/usr/bin/env python3
# Junta TODAS las capturas de escritorio y celular de cada proyecto (sin logos ni láminas)
# y las exporta en webp para el visor del portfolio. Solo lee extraido/.
import os, re, json, tarfile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
RAIZ = next(p for p in (os.path.expanduser('~/Projects'), os.path.expanduser('~/mnt/Projects')) if os.path.isdir(p))
BASE = os.path.join(RAIZ, 'Malackath/malackath-web/identidades-zips/extraido')
OUT = os.path.join(RAIZ, 'Malackath/_portfolio-capturas-' + (__import__('sys').argv[1] if len(__import__('sys').argv) > 1 else 'v1'))
DIRS = {'arma-partido':'ArmaPartido','barajala':'Barajala','zoomi':'Coat n Nest','pizcaya':'CocinaApp','coinciva':'Coinciva',
 'ecos':'ECOS','jip':'JLP','la-gloria':'LaGloria','marea-alta':'MareAlta','mesaluma':'Mesaluma','nunca-te-falla':'NuncaTeFalla',
 'palquear':'Palquear','patovava':'PatovaVa','ravekit':'RaveKit','ruvia':'RuVIA','banana-team':'The.Banana.Team',
 'usa-storefront':'UsaStorefront','velvet':'Velvet','web-arnelli':'WebArnelli','cartelera':'cartelerauy','sitios-gastro':'sitios-gastro-portfolio-2026-11-24'}
FUERA = re.compile(r'logo|lamina|mockup|telefono-suelto|vista-previa|presentacion|seleccion|hoja|og-image|/en/|/en-|idioma-en|-en-|_en_', re.I)
DESK_DIR = re.compile(r'desktop|escritorio|compu', re.I)
MOB_DIR = re.compile(r'movil|mobile|celular', re.I)
MAX = 14
# Proyectos con capturas armadas aparte (no se regeneran desde los zips).
SALTEAR = {'mesaluma'}
# Capturas de celular metidas en un lienzo de compu, montajes, o pantallas que no van.
FUERA_PROY = {
 'ruvia': re.compile(r'marco|pantallas|desktop', re.I),  # la web es un prototipo que no tiene el estilo de la app: solo celular
 'nunca-te-falla': re.compile(r'desktop/app-', re.I),
 'velvet': re.compile(r'portada', re.I),            # portada = aviso de mayoría de edad
 'palquear': re.compile(r'Palquear/desktop-', re.I),  # las del zip: celular en lienzo de compu o repetidas de _palquear-desktop
 'marea-alta': re.compile(r'-pt-', re.I),            # versión en portugués = misma pantalla repetida
 'usa-storefront': re.compile(r'-A(-completa)?\.png$|nails-'),  # variante A: se sale del ancho del celular; nails: el sitio muestra "Placeholder list"
 'patovava': re.compile(r'resumen', re.I),           # montajes de varias pantallas juntas
 'cartelera': re.compile(r'idioma-pt', re.I),         # versión en portugués = misma pantalla repetida
 'coinciva': re.compile(r'/sitio/|desktop-(02|10|11|12)-', re.I),  # celular: solo la app; compu: sin celulares metidos en la lámina
 'pizcaya': re.compile(r'12-tutor-ia', re.I),         # pantalla casi vacía
 'jip': re.compile(r'05_inicio_oscuro|oscuro_01_inicio|oscuro_04_fabula', re.I),  # oscuro con la barra de arriba gris clara (así es el sitio)
}
# Capturas reales de escritorio sacadas aparte (van primero).
EXTRA_D = {'palquear': os.path.join(RAIZ, 'Malackath/_palquear-desktop'),
           'jip': os.path.join(RAIZ, 'Malackath/_jip-desktop')}  # jip: "The good stuff" oscuro recortado de inicio_completa_oscuro (sin la barra gris)
# Capturas nuevas sacadas de los sitios en vivo: si existen para un proyecto, reemplazan a las del zip.
VIVAS = os.path.join(RAIZ, 'Malackath/_capturas-vivas')
# Proporción mínima (alto/ancho) para que una captura llene el marco sin franjas.
MIN_RATIO = {'m': 2.0, 'd': 0.6}
RATIO = {'d': 10/16, 'm': 844/390}
COMPLETA = re.compile(r'completa', re.I)
GRUPOS = {'sitios-gastro': re.compile(r'([a-z0-9-]+)__')}
TEMA = re.compile(r'(?<![a-z])(claro|oscuro|dark|light|scroll)(?![a-z])', re.I)
def pantalla(p):
    # misma pantalla en claro/oscuro o con scroll = una sola
    n = os.path.basename(p).lower().rsplit('.', 1)[0]
    if TEMA.search(n): n = re.sub(r'^[^a-z]*\d+', '', re.sub(r'[-_ ]+', '-', TEMA.sub('', n)).strip('-_ '))
    carpeta = re.sub(r'[^a-z0-9]+', '', TEMA.sub('', os.path.dirname(p).lower()))
    return carpeta + '/' + re.sub(r'[^a-z0-9]+', '', n)
def procesar(clave, fs, pre):
    OSC = re.compile(r'oscuro|dark', re.I)
    vistos = set(); normales = {}; completas = {}
    for p, rel in fs:
        tema = 'osc' if OSC.search(rel) else 'cla'
        k = (tema, pantalla(p))
        if k in vistos: continue
        vistos.add(k)
        try: im = Image.open(p); w, h = im.size
        except Exception: continue
        t = tipo_de(rel.lower(), w, h)
        if t is None: continue
        (completas if COMPLETA.search(rel) else normales).setdefault((tema, t), []).append((p, im))
    extra = EXTRA_D.get(clave)
    extra_fs = sorted(os.path.join(extra, f) for f in os.listdir(extra) if f.lower().endswith(('.png', '.jpg', '.webp'))) if extra and os.path.isdir(extra) else []
    res = {'d': [], 'm': []}
    os.makedirs(os.path.join(OUT, clave), exist_ok=True)
    def armar_lista(tema, t):
        norm = normales.get((tema, t), []); comp = completas.get((tema, t), [])
        buenas = [(p, im) for p, im in norm if im.size[1] / im.size[0] >= MIN_RATIO[t]]
        malas = len(norm) - len(buenas)
        if (malas or not buenas) and comp:
            cupo = max(3, MAX // len(comp))
            return [x for p, im in comp for x in rebanar(p, im.convert('RGB'), t, cupo)], f'{len(comp)} páginas completas cortadas'
        return buenas, (f'{malas} descartadas por medida' if malas else 'ok')
    for t, tw in (('d', 1280), ('m', 390)):
        listas = {}
        for tema in ('cla', 'osc'):
            listas[tema] = armar_lista(tema, t)
        if not listas['cla'][0] and listas['osc'][0]:
            listas['cla'], listas['osc'] = listas['osc'], ([], '')
        if t == 'd' and extra_fs:
            ex_osc = [p for p in extra_fs if OSC.search(os.path.basename(p))]
            ex_cla = [p for p in extra_fs if p not in ex_osc]
            listas['cla'] = ([(p, Image.open(p)) for p in ex_cla] + listas['cla'][0], listas['cla'][1])
            if ex_osc: listas['osc'] = ([(p, Image.open(p)) for p in ex_osc] + listas['osc'][0], listas['osc'][1])
        for tema, (lista, modo) in listas.items():
            if tema == 'osc' and len(lista) < 2: continue
            clave_res = t if tema == 'cla' else t + '_osc'
            res[clave_res] = []
            for i, (p, im) in enumerate(lista[:MAX]):
                im = im.convert('RGB'); w, h = im.size
                rh = int(w * RATIO[t])
                if h > rh: im = im.crop((0, 0, w, rh))
                im = im.resize((tw, int(tw * RATIO[t])), Image.LANCZOS)
                n = f'{pre}{t}-{"osc-" if tema == "osc" else ""}{i+1:02d}.webp'
                im.save(os.path.join(OUT, clave, n), 'WEBP', quality=74, method=6)
                src = p.split('#')[0]
                org = os.path.relpath(src, BASE) if src.startswith(BASE) else os.path.relpath(src, RAIZ)
                res[clave_res].append(dict(f=n, w=im.width, h=im.height, origen=org + ('#' + p.split('#')[1] if '#' in p else '')))
            print(clave, clave_res, len(res[clave_res]), '|', modo, flush=True)
    return res

man = {}
def tipo_de(rel, w, h):
    nom = os.path.basename(rel)
    if DESK_DIR.search(nom) or (DESK_DIR.search(rel) and not MOB_DIR.search(nom)): return 'd' if w >= 900 else 'm'
    if MOB_DIR.search(rel): return 'm' if h / w > 1.3 else 'd'
    return 'm' if h / w > 1.3 else ('d' if w / h > 1.2 else None)
def rebanar(p, im, t, cupo):
    # una página completa se corta en pantallas consecutivas del tamaño del marco
    w, h = im.size; sh = int(w * RATIO[t]); out = []
    for y in range(0, h - int(sh * .9), sh):
        c = im.crop((0, y, w, min(y + sh, h)))
        if c.height < sh: continue
        g = c.convert('L').resize((40, 40))
        if max(g.getdata()) - min(g.getdata()) < 12: continue  # pantalla vacía
        out.append((f'{p}#{len(out)+1}', c))
        if len(out) >= cupo: break
    return out
for clave, d in DIRS.items():
    if clave in SALTEAR: continue
    raiz_v = os.path.join(VIVAS, clave)
    fuentes = [raiz_v] if os.path.isdir(raiz_v) else [os.path.join(BASE, d)]
    fs = []
    for fuente in fuentes:
        for r, _, files in os.walk(fuente):
            for f in sorted(files):
                if f.lower().rsplit('.', 1)[-1] not in ('png', 'jpg', 'jpeg', 'webp'): continue
                p = os.path.join(r, f); rel = os.path.relpath(p, BASE) if p.startswith(BASE) else os.path.relpath(p, VIVAS)
                if clave == 'arma-partido' and 'celular-pantallas' not in rel and 'compu' not in rel: continue
                elif clave != 'arma-partido' and (FUERA.search(rel) or re.search(r'portfolio-\d', f)): continue
                if clave in FUERA_PROY and FUERA_PROY[clave].search(rel): continue
                fs.append((p, rel))
    def orden(x):
        n = os.path.basename(x[0]).lower(); m = re.search(r'(\d+)', re.sub(r'\d{3,4}x\d{3,4}', '', n))
        return (int(m.group(1)) if m else 999, x[1].lower())
    fs.sort(key=orden)
    if clave in GRUPOS:
        # varios sitios dentro de un mismo proyecto: un juego de capturas por sitio
        ids = []
        for p, rel in fs:
            g = GRUPOS[clave].match(os.path.basename(p))
            if g and g.group(1) not in ids: ids.append(g.group(1))
        res = {'grupos': []}
        for g in ids:
            sub = [x for x in fs if os.path.basename(x[0]).startswith(g + '__')]
            r = procesar(clave, sub, g + '-'); r['id'] = g; res['grupos'].append(r)
    else:
        res = procesar(clave, fs, '')
    man[clave] = res
json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
with tarfile.open(OUT + '.tar', 'w') as t: t.add(OUT, arcname=os.path.basename(OUT))
print('tar', os.path.getsize(OUT + '.tar'))
