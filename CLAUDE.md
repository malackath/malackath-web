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
- Menú para celular (Stitch no lo traía): botón redondo que abre los links del menú (`menu_celular()`, Ber 2026-11-25).
- Pie: logo de Malackath arriba de los husos horarios; sin los links de redes y legales que no llevaban a ningún lado; sin «Construyamos el futuro juntos» en ninguna página (repetía el cierre) (`pie()`, Ber 2026-11-25).
- Textos inventados de los casos → textos reales en `casos_textos.py` (fuentes: repos de Armá Partido y Pizcaya).

## Casos de estudio (regla de Ber, 2026-11-25: vale para todos los casos, actuales y futuros)
- Hero con fondo de foto: 2 fotos genéricas que se alternan cada 5 s, velo claro y degradé que termina en negro a la altura del título de «La visión».
- Sección de los pilares con una foto a todo el ancho y velo oscuro.
- Recuadro de las capturas con presencia: tono más claro, borde fino y brillo del color de la marca del caso (`panel_capturas()`).
- Las fotos se generan en Flow (prompts en `/mnt/project-files/malackath/casos-fondos/prompts-flow.md`) y van en `design/fondos-casos/` por convención de nombre: `<clave>-1-*.webp` y `<clave>-2-*.webp` (hero) y `<clave>-pilares.webp` (pilares), con `<clave>` = nombre de la página sin guiones (`casos/arma-partido.html` → `armapartido`). `build.py` las toma solas (`fotos_caso()`).
- Caso nuevo: agregar sus datos en `casos_nuevos.py` + sus 3 fotos en `design/fondos-casos/`.

## Cómo se arma
- `stitch/<pantalla>/code.html` + `screen.png`: export original de Stitch (no tocar).
- `build.py`: toma cada pantalla de Stitch y aplica los cambios de arriba → `public/`.
- `tailwind.config.js`: la config exacta que trae Stitch; el CSS se compila (no se usa el CDN de Tailwind).
- `npm install` y después `npm run build` (genera las páginas y `public/css/estilos.css`).
- Ver localmente: `npm run dev`.

Páginas: `index.html` (home), `trabajo.html`, `casos-de-estudio.html`, `estudio.html` (estudio + contacto), `presupuesto.html` ("Armá tu presupuesto", 4 pasos, sin precios; arma un WhatsApp o mail con un código `MLK1:` para la herramienta interna), `casos/arma-partido.html`, `casos/pizcaya.html`, `casos/palquear.html`, `casos/cartelera.html`, `casos/mesaluma.html`, `casos/ravekit.html`. Cada una en español (raíz), inglés (`/en/`) y portugués (`/pt/`).

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
