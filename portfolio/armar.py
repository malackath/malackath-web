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
tarjetas, secciones = [], []
for n, p in enumerate(lista, 1):
    d = json.load(open(os.path.join(SRC, p['c'] + '.json')))
    logo = next(l for l in d['logos'] if l['nombre'] == p['logo']) if p['logo'] else d['desk'][0]
    lsrc, lw, lh = guardar(p['c'], logo, 'logo')
    vistos, desk, mob = set(), [], []
    for k, dest in (('desk', desk), ('mob', mob)):
        for i in d[k]:
            if i['src'] in vistos: continue
            vistos.add(i['src']); dest.append(guardar(p['c'], i, k))
    if not desk and not mob:
        for i in d['lam']: desk.append(guardar(p['c'], i, 'lam'))
    num = f'{n:02d}'
    logo_html = (f'<div class="logo f-{p["fondo"]}"><img src="{lsrc}" width="{lw}" height="{lh}" alt="{e(p["n"])}" loading="lazy"></div>')
    tarjetas.append(f'''<a class="tarjeta" href="#{p["c"]}">{logo_html}
  <div class="info"><span class="tipo">{e(p["t"])}</span><h3>{e(p["n"])}</h3><p>{e(p["d"])}</p></div></a>''')
    figs = lambda L, cls: ''.join(f'<figure class="{cls}"><img src="{s}" width="{w}" height="{h}" alt="{e(p["n"])}" loading="lazy" decoding="async"></figure>' for s, w, h in L)
    tiras = ''
    if desk: tiras += f'<div class="tira">{figs(desk, "desk")}</div>'
    if mob: tiras += f'<div class="tira">{figs(mob, "mob")}</div>'
    secciones.append(f'''<section class="proyecto" id="{p["c"]}">
  <header class="cab">{logo_html}<div><span class="num">{num}</span><span class="tipo">{e(p["t"])}</span><h2>{e(p["n"])}</h2><p>{e(p["d"])}</p></div></header>
  {tiras}
</section>''')

plantilla = open(os.path.join(AQUI, 'plantilla.html')).read()
out = plantilla.replace('{{TARJETAS}}', '\n'.join(tarjetas)).replace('{{SECCIONES}}', '\n'.join(secciones)).replace('{{CANTIDAD}}', str(len(lista)))
open(f'{OUT}/index.html', 'w').write(out)
shutil.copy(os.path.join(AQUI, '..', 'public', 'img', 'marca', 'malackath-horizontal-color-negativo.svg'), f'{OUT}/img/logo.svg')
shutil.copy(os.path.join(AQUI, '..', 'public', 'img', 'marca', 'favicon.svg'), f'{OUT}/img/favicon.svg')
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print(f'{len(lista)} proyectos, {tot/1e6:.1f} MB en public/')
