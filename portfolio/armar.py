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
NOMBRES_GRUPO = {'botanica-bistro': 'Botánica Bistro', 'brisa-marea': 'Brisa & Marea', 'fuego-puerto': 'Fuego & Puerto',
                 'fuego-silvestre': 'Fuego Silvestre', 'oceanica': 'Oceánica'}
MANIFEST = json.load(open(os.path.join(AQUI, 'capturas', 'manifest.json')))
tarjetas, secciones = [], []
for n, p in enumerate(lista, 1):
    jp = os.path.join(SRC, p.get('json', p['c']) + '.json')
    d = json.load(open(jp)) if os.path.exists(jp) else dict(logos=[], desk=[], mob=[], lam=[])
    if p.get('logo_archivo'):
        ext = p['logo_archivo'].rsplit('.', 1)[-1]
        lsrc = f"img/p/{p['c']}-logo.{ext}"
        shutil.copy(os.path.join(AQUI, p['logo_archivo']), f'{OUT}/{lsrc}')
        lw, lh = 560, 129
        if ext != 'svg':
            from PIL import Image
            im = Image.open(f'{OUT}/{lsrc}'); im.thumbnail((1120, 400)); im.save(f'{OUT}/{lsrc}'); lw, lh = im.size
    else:
        logo = next(l for l in d['logos'] if l['nombre'] == p['logo']) if p['logo'] else d['desk'][0]
        lsrc, lw, lh = guardar(p['c'], logo, 'logo')
    man = {'d': [], 'm': []} if p.get('solo_logo') else MANIFEST.get(p['c'], {'d': [], 'm': []})
    def color_pie(f):
        # color del borde de abajo: rellena el marco cuando la captura es más baja que la pantalla
        from PIL import Image
        im = Image.open(f).convert('RGB'); w, h = im.size
        c = im.crop((0, h - 3, w, h)).resize((1, 1), Image.BOX).getpixel((0, 0))
        return '#%02x%02x%02x' % c
    def copiar(tipo, man=man):
        out = []
        for x in man.get(tipo, []):
            dst = f"img/p/{p['c']}-{x['f']}"
            shutil.copy(os.path.join(AQUI, 'capturas', p['c'], x['f']), f'{OUT}/{dst}')
            out.append((dst, x['w'], x['h'], color_pie(os.path.join(AQUI, 'capturas', p['c'], x['f']))))
        return out
    desk, mob, lam = copiar('d'), copiar('m'), []
    if not desk and not mob and not p.get('solo_logo') and not man.get('grupos'):
        lam = [guardar(p['c'], i, 'lam') for i in d['lam']]
    num = f'{n:02d}'
    logo_html = (f'<div class="logo f-{p["fondo"]}"><img src="{lsrc}" width="{lw}" height="{lh}" alt="{e(p["n"])}" loading="lazy"></div>')
    tarjetas.append(f'''<a class="tarjeta" href="#{p["c"]}">{logo_html}
  <div class="info"><span class="tipo">{e(p["t"])}</span><h3>{e(p["n"])}</h3><p>{e(p["d"])}</p></div></a>''')
    def visor(L, clase, etiqueta):
        if not L: return ''
        imgs = ''.join(f'<img data-src="{x[0]}" width="{x[1]}" height="{x[2]}"{f' style="background:{x[3]}"' if len(x) > 3 else ''} alt="{e(p["n"])}: {etiqueta} {k+1} de {len(L)}"{" class=on" if k == 0 else ""}>' for k, x in enumerate(L))
        puntos = ''.join(f'<button type="button" aria-label="Ver {k+1}"{" class=on" if k == 0 else ""}></button>' for k in range(len(L))) if len(L) > 1 else ''
        nav = (f'<div class="nav"><button type="button" class="ant" aria-label="Anterior">&#8592;</button><span class="cuenta">1 / {len(L)}</span>'
               f'<button type="button" class="sig" aria-label="Siguiente">&#8594;</button></div><div class="puntos">{puntos}</div>') if len(L) > 1 else ''
        barra = '<div class="barra-nav"><i></i><i></i><i></i></div>' if clase == 'compu' else ('<div class="isla"></div>' if clase == 'cel' else '')
        return f'<figure class="sim {clase}"><div class="marco">{barra}<div class="pantalla">{imgs}</div></div>{nav}<figcaption>{etiqueta}</figcaption></figure>'
    sims = visor(desk, 'compu', 'Escritorio') + visor(mob, 'cel', 'Celular') + visor(lam, 'lam', 'Identidad')
    variantes = []  # (id, etiqueta, visores)
    if man.get('grupos'):
        for g in man['grupos']:
            variantes.append((g['id'], NOMBRES_GRUPO.get(g['id'], g['id']), visor(copiar('d', g), 'compu', 'Escritorio') + visor(copiar('m', g), 'cel', 'Celular')))
        sims = variantes[0][2] if variantes else sims
        etiqueta_sel = 'Sitio'
    else:
        desk_o, mob_o = copiar('d_osc'), copiar('m_osc')
        if desk_o or mob_o:
            variantes = [('cla', 'Claro', sims), ('osc', 'Oscuro', visor(desk_o or desk, 'compu', 'Escritorio') + visor(mob_o or mob, 'cel', 'Celular'))]
        etiqueta_sel = 'Modo de color'
    temas, bloques = '', f'<div class="sims">{sims}</div>' if sims else ''
    if len(variantes) > 1:
        # selector: cada botón muestra otro juego de capturas en los mismos marcos
        temas = (f'<div class="temas" role="group" aria-label="{etiqueta_sel}">' + ''.join(
            f'<button type="button"{" class=on" if k == 0 else ""} data-tema="{v}" aria-pressed="{"true" if k == 0 else "false"}">{e(et)}</button>'
            for k, (v, et, _) in enumerate(variantes)) + '</div>')
        bloques = '\n  '.join(f'<div class="sims" data-tema="{v}"{" hidden" if k else ""}>{h}</div>' for k, (v, _, h) in enumerate(variantes))
    secciones.append(f'''<section class="proyecto" id="{p["c"]}">
  <header class="cab">{logo_html}<div><span class="num">{num}</span><span class="tipo">{e(p["t"])}</span><h2>{e(p["n"])}</h2><p>{e(p["d"])}</p>{temas}</div></header>
  {bloques}
</section>''')

plantilla = open(os.path.join(AQUI, 'plantilla.html')).read()
out = plantilla.replace('{{TARJETAS}}', '\n'.join(tarjetas)).replace('{{SECCIONES}}', '\n'.join(secciones)).replace('{{CANTIDAD}}', str(len(lista)))
open(f'{OUT}/index.html', 'w').write(out)
shutil.copy(os.path.join(AQUI, '..', 'public', 'img', 'marca', 'malackath-horizontal-color-negativo.svg'), f'{OUT}/img/logo.svg')
shutil.copy(os.path.join(AQUI, '..', 'public', 'img', 'marca', 'favicon.svg'), f'{OUT}/img/favicon.svg')
tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(OUT) for f in fs)
print(f'{len(lista)} proyectos, {tot/1e6:.1f} MB en public/')
