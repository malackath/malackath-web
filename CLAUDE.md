# malackath-web

Sitio de Malackath (estudio de diseño y producto digital de Ber). Sitio estático en español.

## Regla principal
El diseño es el que Ber hizo en **Stitch** (carpeta `stitch/`, sistema "Obsidian Kinetic": fondo #131315, lima #CAF300/#D4FF00, Syne + DM Sans + Space Mono). Se respeta tal cual: no rediseñar, no cambiar tipografías ni colores, no "adaptar a la marca". Si algo del diseño no se puede replicar, avisarle a Ber antes de cambiarlo.

Cambios permitidos sobre el HTML de Stitch (todos en `build.py`, nunca a mano en `public/`):
- Logo Kinetic → logo Malackath (`public/img/marca/`, sale del kit `design/marca-v1/`).
- Imágenes generadas por Stitch → fotos y capturas reales de los proyectos (`public/img/proyectos/`).
- Sacar números y métricas no confirmados por Ber.
- Datos falsos de la agencia de ejemplo (Kinetic, París/NY/Tokio, equipo inventado) → datos reales o se sacan.
- Ajustes para que en celular nada se salga de la pantalla (usando los tamaños mobile del propio sistema de Stitch).
- Testimonios inventados por Stitch: se sacaron (decisión de Ber, 2026-11-24).
- Textos inventados de los casos → textos reales en `casos_textos.py` (fuentes: repos de Armá Partido y Pizcaya).

## Cómo se arma
- `stitch/<pantalla>/code.html` + `screen.png`: export original de Stitch (no tocar).
- `build.py`: toma cada pantalla de Stitch y aplica los cambios de arriba → `public/`.
- `tailwind.config.js`: la config exacta que trae Stitch; el CSS se compila (no se usa el CDN de Tailwind).
- `npm install` y después `npm run build` (genera las páginas y `public/css/estilos.css`).
- Ver localmente: `npm run dev`.

Páginas: `index.html` (home), `trabajo.html`, `estudio.html` (estudio + contacto), `presupuesto.html` ("Armá tu presupuesto", 4 pasos, sin precios; arma un WhatsApp o mail con un código `MLK1:` para la herramienta interna), `casos/arma-partido.html`, `casos/pizcaya.html`. Cada una en español (raíz), inglés (`/en/`) y portugués (`/pt/`).

## Idiomas
- El español es la fuente: sale de `build.py`. `i18n.py generar` traduce con `i18n/en.json` y `i18n/pt.json` (clave = texto en español) y agrega el selector ES / EN / PT al menú.
- Si cambia un texto en español: `python3 i18n.py extraer` agrega las claves nuevas vacías a los .json; completarlas y `npm run build` (falla si falta alguna).
- Las traducciones al portugués de Brasil y al inglés están pendientes de revisión de Ber.

## Contacto
Sin servidor: el formulario arma un mail (mailto) y el botón de WhatsApp abre wa.me. Las constantes `MAIL` y `WHATSAPP` están arriba en `build.py`.

## Publicación
- Hosting previsto: Firebase Hosting (`firebase.json`, carpeta `public/`), dominio malackath.com con DNS en Cloudflare.
- **No hacer deploy sin el OK de Ber.** Nada de claves en el código.

## Contratos y presupuestos (no se publican)
- `contratos/`: plantillas de propuesta, contrato marco, SOW, T&M, mantenimiento, orden de cambio, términos de pago y NDA (es/; en/ y pt/ pendientes). Todo dato es un campo `{{...}}` que se completa por documento. A revisar por abogado y contador.
- `herramientas/presupuestos/`: herramienta interna (HTML local) que arma propuesta y contratos y exporta PDF. Después de tocar una plantilla: `python3 herramientas/presupuestos/armar.py`.
- Decisiones de Ber (2026-11-25): moneda US$ con opción $U/R$; IVA 22% a clientes de Uruguay y exportación sin IVA al exterior; mantenimiento = cuota con horas incluidas no acumulables.

## Pendientes
Ver `docs/pendientes.md`.
