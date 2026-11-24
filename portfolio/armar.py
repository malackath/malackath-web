#!/usr/bin/env python3
"""Arma portfolio/public/ (sitio estático) desde los JSON del fichero de 21 proyectos.
Uso: python3 armar.py <carpeta con los .json> [clave-extra ...]
Las claves extra (de PENDIENTES) se agregan solo si se pasan explícitamente."""
import json, os, sys, base64, hashlib, html, shutil
from proyectos import PUBLICOS, PENDIENTES

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = sys.argv[1]
EXTRA = sys.argv[2:]
OUT = os.path.join(AQUI, 'public')
lista = PUBLICOS + [dict(c=k, **PENDIENTES[k]) for k in EXTRA]

if os.path.isdir(OUT + '/img/p'):
    shutil.rmtree(OUT + '/img/p')
os.makedirs(OUT + '/img/p', exist_ok=True)

def guardar(c, i, prefijo):
    head, b64 = i['src'].split(',', 1)
    ext = 'webp' if 'webp' in head else 'png'
    data = base64.b64decode(b64)
    nombre = f"{c}-{prefijo}-{hashlib.sha1(data).hexdigest()[:8]}.{ext}"
    open(f'{OUT}/img/p/{nombre}', 'wb').write(data)
    return f'img/p/{nombre}', i['w'], i['h']

e = html.escape
MANIFEST = json.load(open(os.path.join(AQUI, 'capturas', 'manifest.json')))
tarjetas, secciones = [], []
for n, p in enumerate(lista, 1):
    d = json.load(open(os.path.join(SRC, p['c'] + '.json')))
    logo = next(l for l in d['logos'] if l['nombre'] == p['logo']) if p['logo'] else d['desk'][0]
    lsrc, lw, lh = guardar(p['c'], logo, 'logo')
    if p.get('logo_archivo'):
        dst = f"img/p/{p['c']}-logo.svg"
        shutil.copy(os.path.join(AQUI, p['logo_archivo']), f'{OUT}/{dst}')
        os.remove(f'{OUT}/{lsrc}'); lsrc = dst
    man = MANIFEST.get(p['c'], {'d': [], 'm': []})
    def copiar(tipo):
        out = []
        for x in man[tipo]:
            dst = f"img/p/{p['c']}-{x['f']}"
            shutil.copy(os.path.join(AQUI, 'capturas', p['c'], x['f']), f'{OUT}/{dst}')
            out.append((dst, x['w'], x['h']))
        return out
    desk, mob, lam = copiar('d'), copiar('m'), []
    if not desk and not mob:
        lam = [guardar(p['c'], i, 'lam') for i in d['lam']]
    num = f'{n:02d}'
    logo_html = (f'<div class="logo f-{p["fondo"]}"><img src="{lsrc}" width="{lw}" height="{lh}" alt="{e(p["n"])}" loading="lazy"></div>')
    tarjetas.append(f'''<a class="tarjeta" href="#{p["c"]}">{logo_html}
  <div class="info"><span class="tipo">{e(p["t"])}</span><h3>{e(p["n"])}</h3><p>{e(p["d"])}</p></div></a>''')
    def visor(L, clase, etiqueta):
        if not L: return ''
        imgs = ''.join(f'<img data-src="{s}" width="{w}" height="{h}" alt="{e(p["n"])}: {etiqueta} {k+1} de {len(L)}"{" class=on" if k == 0 else ""}>' for k, (s, w, h) in enumerate(L))
        puntos = ''.join(f'<button type="button" aria-label="Ver {k+1}"{" class=on" if k == 0 else ""}></button>' for k in range(len(L))) if len(L) > 1 else ''
        nav = (f'<div class="nav"><button type="button" class="ant" aria-label="Anterior">&#8592;</button><span class="cuenta">1 / {len(L)}</span>'
               f'<button type="button" class="sig" aria-label="Siguiente">&#8594;</button></div><div class="puntos">{puntos}</div>') if len(L) > 1 else ''
        barra = '<div class="barra-nav"><i></i><i></i><i></i></div>' if clase == 'compu' else ('<div class="isla"></div>' if clase == 'cel' else '')
        return f'<figure class="sim {clase}"><div class="marco">{barra}<div class="pantalla">{imgs}</div></div>{nav}<figcaption>{etiqueta}</figcaption></figure>'
    sims = visor(desk, 'compu', 'Escritorio') + visor(mob, 'cel', 'Celular') + visor(lam, 'lam', 'Identidad')
    secciones.append(f'''<section class="proyecto" id="{p["c"]}">
  <header class="cab">{logo_html}<div><span class="num">{num}</span><span class="tipo">{e(p["t"])}</span><h2>{e(p["n"])}</h2><p>{e(p["d"])}</p></div></header>
  <div class="sims">{sims}</div>
</section>''')

plantilla = open(os.path.join(AQUI, 'plantilla.html')).read()
out = plantilla.replace('{{TARJETAS}}', '\n'.join(tarjetas)).replace('{{SECCIONES}}', '\n'.join(secciones)).replace('{{CANTIDAD}}', str(len(lista)))
open(f'{OUT}/index.html', 'w').write(out)
shutil.copy(os.path.join(AQUI, '..', 'public', 'img', 'marca', 'malackath-horizontal-color-negativo.svg'), f'{OUT}/img/logo.svg')
shutil.copy(os.path.join(AQUI, '..', 'public', 'img', 'marca', 'favicon.svg'), f'{OUT}/img/favicon.svg')
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print(f'{len(lista)} proyectos, {tot/1e6:.1f} MB en public/')
