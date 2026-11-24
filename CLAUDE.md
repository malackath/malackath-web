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
- Testimonios inventados por Stitch llevan el rótulo "Sample" hasta que Ber decida.

## Cómo se arma
- `stitch/<pantalla>/code.html` + `screen.png`: export original de Stitch (no tocar).
- `build.py`: toma cada pantalla de Stitch y aplica los cambios de arriba → `public/`.
- `tailwind.config.js`: la config exacta que trae Stitch; el CSS se compila (no se usa el CDN de Tailwind).
- `npm install` y después `npm run build` (genera las páginas y `public/css/estilos.css`).
- Ver localmente: `npm run dev`.

Páginas: `index.html` (home), `trabajo.html`, `estudio.html` (estudio + contacto), `casos/arma-partido.html`, `casos/pizcaya.html`.

## Contacto
Sin servidor: el formulario arma un mail (mailto) y el botón de WhatsApp abre wa.me. Las constantes `MAIL` y `WHATSAPP` están arriba en `build.py`.

## Publicación
- Hosting previsto: Firebase Hosting (`firebase.json`, carpeta `public/`), dominio malackath.com con DNS en Cloudflare.
- **No hacer deploy sin el OK de Ber.** Nada de claves en el código.

## Pendientes
Ver `docs/pendientes.md`.
