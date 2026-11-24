#!/usr/bin/env python3
# Junta TODAS las capturas de escritorio y celular de cada proyecto (sin logos ni láminas)
# y las exporta en webp para el visor del portfolio. Solo lee extraido/.
import os, re, json, tarfile
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
RAIZ = next(p for p in (os.path.expanduser('~/Projects'), os.path.expanduser('~/mnt/Projects')) if os.path.isdir(p))
BASE = os.path.join(RAIZ, 'Malackath/malackath-web/identidades-zips/extraido')
OUT = os.path.join(RAIZ, 'Malackath/_portfolio-capturas-' + (__import__('sys').argv[1] if len(__import__('sys').argv) > 1 else 'v1'))
DIRS = {'arma-partido':'ArmaPartido','barajala':'Barajala','coat-n-nest':'Coat n Nest','pizcaya':'CocinaApp','coinciva':'Coinciva',
 'ecos':'ECOS','jip':'JLP','la-gloria':'LaGloria','marea-alta':'MareAlta','mesaluma':'Mesaluma','nunca-te-falla':'NuncaTeFalla',
 'palquear':'Palquear','patovava':'PatovaVa','ravekit':'RaveKit','ruvia':'RuVIA','banana-team':'The.Banana.Team',
 'usa-storefront':'UsaStorefront','velvet':'Velvet','web-arnelli':'WebArnelli','cartelera':'cartelerauy','sitios-gastro':'sitios-gastro-portfolio-2026-11-24'}
FUERA = re.compile(r'logo|lamina|mockup|telefono-suelto|vista-previa|presentacion|seleccion|hoja|og-image|completa|/en/|/en-|idioma-en|-en-|_en_', re.I)
DESK_DIR = re.compile(r'desktop|escritorio|compu', re.I)
MOB_DIR = re.compile(r'movil|mobile|celular', re.I)
MAX = 14
# Proyectos con capturas armadas aparte (no se regeneran desde los zips).
SALTEAR = {'mesaluma'}
# Capturas de celular metidas en un lienzo de compu, montajes, o pantallas que no van.
FUERA_PROY = {
 'ruvia': re.compile(r'marco|pantallas', re.I),
 'nunca-te-falla': re.compile(r'desktop/app-', re.I),
 'velvet': re.compile(r'portada', re.I),            # portada = aviso de mayoría de edad
 'palquear': re.compile(r'desktop-0[1456789]', re.I),  # 01, 04-09: celular dentro de lienzo de compu
 'marea-alta': re.compile(r'-pt-', re.I),            # versión en portugués = misma pantalla repetida
}
# Capturas reales de escritorio sacadas aparte (van primero).
EXTRA_D = {'palquear': os.path.join(RAIZ, 'Malackath/_palquear-desktop')}
TEMA = re.compile(r'(?<![a-z])(claro|oscuro|dark|light|scroll)(?![a-z])', re.I)
def pantalla(p):
    # misma pantalla en claro/oscuro o con scroll = una sola
    n = os.path.basename(p).lower().rsplit('.', 1)[0]
    if TEMA.search(n): n = re.sub(r'^[^a-z]*\d+', '', re.sub(r'[-_ ]+', '-', TEMA.sub('', n)).strip('-_ '))
    return re.sub(r'[^a-z0-9]+', '', n)
man = {}
for clave, d in DIRS.items():
    if clave in SALTEAR: continue
    fs = []
    for r, _, files in os.walk(os.path.join(BASE, d)):
        for f in sorted(files):
            if f.lower().rsplit('.', 1)[-1] not in ('png', 'jpg', 'jpeg', 'webp'): continue
            p = os.path.join(r, f); rel = os.path.relpath(p, BASE)
            if clave == 'arma-partido' and 'celular-pantallas' not in rel and 'compu' not in rel: continue
            elif clave != 'arma-partido' and (FUERA.search(rel) or re.search(r'portfolio-\d', f)): continue
            if clave in FUERA_PROY and FUERA_PROY[clave].search(rel): continue
            fs.append(p)
    def orden(p):
        n = os.path.basename(p).lower(); m = re.search(r'(\d+)', re.sub(r'\d{3,4}x\d{3,4}', '', n))
        return (int(m.group(1)) if m else 999, os.path.relpath(p, BASE).lower())
    fs.sort(key=orden)
    vistos = set(); unicos = []
    for p in fs:
        k = pantalla(p)
        if k in vistos: continue
        vistos.add(k); unicos.append(p)
    fs = unicos
    extra = EXTRA_D.get(clave)
    extra_fs = sorted(os.path.join(extra, f) for f in os.listdir(extra) if f.lower().endswith(('.png', '.jpg', '.webp'))) if extra and os.path.isdir(extra) else []
    desk, mob = [], []
    for p in extra_fs: desk.append((p, Image.open(p)))
    for p in fs:
        try: im = Image.open(p); w, h = im.size
        except Exception: continue
        rel = os.path.relpath(p, BASE).lower(); nom = os.path.basename(rel)
        if DESK_DIR.search(nom) or (DESK_DIR.search(rel) and not MOB_DIR.search(nom)):
            tipo = 'd' if w >= 900 else 'm'
        elif MOB_DIR.search(rel): tipo = 'm' if h / w > 1.3 else 'd'
        else: tipo = 'm' if h / w > 1.3 else ('d' if w / h > 1.2 else None)
        if tipo is None: continue
        (desk if tipo == 'd' else mob).append((p, im))
    res = {'d': [], 'm': []}
    os.makedirs(os.path.join(OUT, clave), exist_ok=True)
    for tipo, lista, (tw, ratio) in (('d', desk, (1280, 10/16)), ('m', mob, (390, 844/390))):
        for i, (p, im) in enumerate(lista[:MAX]):
            im = im.convert('RGB'); w, h = im.size
            rh = int(w * ratio)
            if h > rh: im = im.crop((0, 0, w, rh))
            elif h < rh * 0.97:  # más baja que el marco: se centra sobre su propio color
                pass
            im.thumbnail((tw, int(tw * ratio) + 2), Image.LANCZOS)
            n = f'{tipo}-{i+1:02d}.webp'
            im.save(os.path.join(OUT, clave, n), 'WEBP', quality=72, method=6)
            res[tipo].append(dict(f=n, w=im.width, h=im.height, origen=os.path.relpath(p, BASE) if p.startswith(BASE) else os.path.basename(p)))
    man[clave] = res
    print(clave, 'escritorio', len(desk), '→', len(res['d']), '| celular', len(mob), '→', len(res['m']), flush=True)
json.dump(man, open(os.path.join(OUT, 'manifest.json'), 'w'), ensure_ascii=False, indent=1)
with tarfile.open(OUT + '.tar', 'w') as t: t.add(OUT, arcname='_portfolio-capturas-' + (__import__('sys').argv[1] if len(__import__('sys').argv) > 1 else 'v1'))
print('tar', os.path.getsize(OUT + '.tar'))
