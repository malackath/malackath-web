/* Generador de presupuestos y contratos de Malackath (uso interno).
   Todo se guarda en este navegador (localStorage). Respaldo: botón "Respaldo".
   Nada de datos inventados: lo que no se completa sale como campo vacío. */
(() => {
"use strict";

// ---------- Documentos ----------
const DOCS = [
  { k: "propuesta", n: "Propuesta" },
  { k: "marco", n: "Contrato marco" },
  { k: "sow", n: "SOW (alcance)" },
  { k: "tm", n: "Anexo T&M" },
  { k: "mantenimiento", n: "Mantenimiento" },
  { k: "cambio", n: "Orden de cambio" },
  { k: "pagos", n: "Términos de pago" },
  { k: "nda", n: "NDA" },
];

// ---------- Textos de la propuesta por idioma ----------
const TX = {
  es: { serv: "Servicio", inc: "Qué incluye", modo: "Modalidad", precio: "Precio", cerrado: "Precio cerrado", horas: "Por horas", hEst: "h estimadas", tope: "tope", sub: "Subtotal", total: "Total", etapa: "Etapa", dur: "Duración estimada", sin: "sin", pag: "Página" },
  en: { serv: "Service", inc: "What's included", modo: "Model", precio: "Price", cerrado: "Fixed price", horas: "Time & materials", hEst: "h estimated", tope: "cap", sub: "Subtotal", total: "Total", etapa: "Phase", dur: "Estimated duration", sin: "no", pag: "Page" },
  pt: { serv: "Serviço", inc: "O que inclui", modo: "Modalidade", precio: "Preço", cerrado: "Preço fechado", horas: "Por horas", hEst: "h estimadas", tope: "teto", sub: "Subtotal", total: "Total", etapa: "Etapa", dur: "Duração estimada", sin: "sem", pag: "Página" },
};
const MONEDAS = { "US$": { es: "dólares estadounidenses", en: "US dollars", pt: "dólares americanos" }, "$U": { es: "pesos uruguayos", en: "Uruguayan pesos", pt: "pesos uruguaios" }, "R$": { es: "reales", en: "Brazilian reais", pt: "reais" } };

// ---------- Sugerencias por país (solo se aplican si el campo está vacío o al tocar "Sugerir") ----------
const PAISES = ["Uruguay", "Brasil", "Argentina", "Estados Unidos", "Otro"];
const ID_FISCAL = { Uruguay: "RUT", Brasil: "CNPJ", Argentina: "CUIT", "Estados Unidos": "EIN" };
function sugerencias(emisorPais, clientePais) {
  const s = {};
  if (emisorPais === "Uruguay") {
    s.ley_aplicable = "la República Oriental del Uruguay";
    s.jurisdiccion = "la ciudad de Montevideo";
    s.ley_datos_personales = "la Ley N.º 18.331 de Protección de Datos Personales";
    s.zona_horaria = "hora de Montevideo";
    s.pais_dias_habiles = "Uruguay";
    if (clientePais === "Uruguay") { s.impuesto_nombre = "IVA"; s.impuesto_pct = "22"; s.nota_impuestos = "El IVA (22%) se suma en cada factura."; }
    else if (clientePais) { s.impuesto_nombre = "IVA"; s.impuesto_pct = "0"; s.nota_impuestos = "Se factura como exportación de servicios, sin IVA. [A confirmar con el contador.]"; }
  } else if (emisorPais === "Brasil") {
    s.ley_aplicable = "la República Federativa del Brasil";
    s.ley_datos_personales = "la Ley N.º 13.709 (LGPD)";
    s.pais_dias_habiles = "Brasil";
    s.impuesto_nombre = "ISS";
  }
  return s;
}

// ---------- Catálogo inicial: las 4 áreas de la página Estudio del sitio ----------
const CATALOGO_INICIAL = [
  "Marca & Estrategia · Posicionamiento", "Marca & Estrategia · Logo & Símbolo", "Marca & Estrategia · Manual de Marca", "Marca & Estrategia · Tono de Voz",
  "Diseño de Producto (UI/UX) · Arquitectura de Producto", "Diseño de Producto (UI/UX) · Prototipos Navegables", "Diseño de Producto (UI/UX) · Sistemas de Diseño",
  "Apps & Plataformas Web · iOS & Android", "Apps & Plataformas Web · Web Apps", "Apps & Plataformas Web · Reservas & Pagos", "Apps & Plataformas Web · Paneles de Gestión",
  "Lanzamiento & Operación · Firebase & Google Cloud", "Lanzamiento & Operación · Dominios & Correo", "Lanzamiento & Operación · App Store & Google Play", "Lanzamiento & Operación · Medición",
  "Mantenimiento mensual",
].map(s => ({ servicio: s, incluye: "" }));

// ---------- Etiquetas de campos ----------
const ETQ = {
  prestador_razon_social: "Razón social", prestador_nombre_fantasia: "Nombre comercial", prestador_id_fiscal_tipo: "Tipo de ID fiscal", prestador_id_fiscal: "N.º de ID fiscal", prestador_domicilio: "Domicilio", prestador_representante: "Quién firma", prestador_email: "Email", prestador_whatsapp: "WhatsApp",
  cliente_razon_social: "Razón social", cliente_contacto: "Persona de contacto", cliente_id_fiscal_tipo: "Tipo de ID fiscal", cliente_id_fiscal: "N.º de ID fiscal", cliente_domicilio: "Domicilio", cliente_representante: "Quién firma", cliente_email: "Email",
  impuesto_nombre: "Impuesto", impuesto_pct: "Impuesto %", nota_impuestos: "Nota de impuestos", ley_aplicable: "Ley aplicable (de…)", jurisdiccion: "Tribunales de…", ley_datos_personales: "Ley de datos personales",
  zona_horaria: "Zona horaria", pais_dias_habiles: "Días hábiles de", fuente_tipo_cambio: "Fuente del tipo de cambio",
  propuesta_numero: "N.º de propuesta", contrato_numero: "N.º de contrato marco", contrato_fecha: "Fecha del contrato marco", sow_numero: "N.º de SOW", oc_numero: "N.º de orden de cambio",
  proyecto_nombre: "Nombre del proyecto", fecha: "Fecha", validez_dias: "Validez (días)", resumen_necesidad: "1. Lo que entendimos", enfoque: "2. Qué proponemos", no_incluye: "No incluye",
  anticipo_pct: "Anticipo %", plan_mantenimiento: "Plan de mantenimiento", cuota_mensual: "Cuota mensual", horas_incluidas: "Horas incluidas por mes",
};
const AYUDA = {
  validez_dias: "ej.: 15", anticipo_pct: "ej.: 50", dias_vencimiento: "ej.: 10", plazo_aceptacion_dias: "ej.: 5", dias_garantia: "ej.: 30", impuesto_pct: "número, sin %",
};
const MULTILINEA = /resumen|enfoque|no_incluye|fuera_de_alcance|aportes|objetivo|descripcion|motivo|proposito|nota_|incluye/;

// Campos que calcula la herramienta (no se piden)
const CALC = new Set(["tabla_precios", "tabla_plazos", "subtotal", "total", "impuesto_linea", "iva_texto", "fecha_validez", "moneda_nombre", "moneda"]);

// ---------- Estado ----------
const LS = { aj: "mlk_ajustes", ex: "mlk_expedientes", act: "mlk_actual" };
const leer = (k, d) => { try { const v = localStorage.getItem(k); return v ? JSON.parse(v) : d; } catch { return d; } };
const guardarLS = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) { aviso("No se pudo guardar en este navegador: " + e.message); } };

let aj = leer(LS.aj, null) || { perfiles: [], tarifas: [], catalogo: CATALOGO_INICIAL, proximoNumero: 1 };
let exps = leer(LS.ex, {});
let actual = leer(LS.act, null);
let doc = "propuesta";

function nuevoExp(nombre) {
  const id = "e" + Date.now().toString(36);
  const anio = new Date().getFullYear();
  exps[id] = {
    nombre: nombre || "Nuevo expediente",
    idioma: "es", moneda: "US$", emisorPais: "Uruguay", clientePais: "",
    d: { fecha: hoy(), propuesta_numero: `P-${anio}-${String(aj.proximoNumero).padStart(3, "0")}` },
    lineas: [{ servicio: "", incluye: "", modo: "cerrado", horas: "", tarifa: "", precio: "", tope: "" }],
    etapas: [{ etapa: "", duracion: "" }],
    actualizado: Date.now(),
  };
  aj.proximoNumero++;
  guardarLS(LS.aj, aj);
  return id;
}
if (!actual || !exps[actual]) { actual = Object.keys(exps)[0] || nuevoExp(); }
const E = () => exps[actual];
function persistir() { E().actualizado = Date.now(); guardarLS(LS.ex, exps); guardarLS(LS.act, actual); }

// ---------- Utilidades ----------
function hoy() { const d = new Date(); return `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}/${d.getFullYear()}`; }
function sumarDias(fecha, dias) {
  const m = /^(\d{1,2})\/(\d{1,2})\/(\d{4})$/.exec(fecha || ""); const n = parseInt(dias, 10);
  if (!m || isNaN(n)) return "";
  const d = new Date(+m[3], +m[2] - 1, +m[1] + n);
  return `${String(d.getDate()).padStart(2, "0")}/${String(d.getMonth() + 1).padStart(2, "0")}/${d.getFullYear()}`;
}
const num = v => { const n = parseFloat(String(v ?? "").replace(/\./g, "").replace(",", ".")); return isNaN(n) ? 0 : n; };
const numSimple = v => { const n = parseFloat(String(v ?? "").replace(",", ".")); return isNaN(n) ? 0 : n; };
function dinero(n) {
  const loc = { es: "es-UY", en: "en-US", pt: "pt-BR" }[E().idioma] || "es-UY";
  return `${E().moneda} ${n.toLocaleString(loc, { minimumFractionDigits: 0, maximumFractionDigits: 2 })}`;
}
const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const etiqueta = k => ETQ[k] || (k.charAt(0).toUpperCase() + k.slice(1)).replace(/_/g, " ");
function aviso(t) { document.getElementById("aviso").textContent = t || ""; }

// ---------- Cálculos ----------
function montoLinea(l) { return l.modo === "horas" ? numSimple(l.horas) * numSimple(l.tarifa) : numSimple(l.precio); }
function calculos() {
  const e = E(), t = TX[e.idioma] || TX.es, d = e.d;
  const sub = e.lineas.reduce((a, l) => a + montoLinea(l), 0);
  const pct = numSimple(d.impuesto_pct);
  const imp = sub * pct / 100;
  const nombreImp = d.impuesto_nombre || "";
  const c = {
    moneda: e.moneda,
    moneda_nombre: (MONEDAS[e.moneda] || {})[e.idioma] || e.moneda,
    subtotal: dinero(sub), impuesto_linea: dinero(imp), total: dinero(sub + imp),
    iva_texto: !nombreImp ? "" : pct > 0 ? `+ ${nombreImp} ${pct}%` : `(${t.sin} ${nombreImp})`,
    fecha_validez: sumarDias(d.fecha, d.validez_dias),
    impuesto_pct: d.impuesto_pct ? `${d.impuesto_pct}%` : "",
  };
  const celda = s => String(s ?? "").replace(/\|/g, "/").replace(/\n/g, " ");
  let tp = `| ${t.serv} | ${t.inc} | ${t.modo} | ${t.precio} |\n|---|---|---|---|\n`;
  e.lineas.filter(l => l.servicio || montoLinea(l)).forEach(l => {
    const modo = l.modo === "horas" ? `${t.horas}: ${l.horas || "__"} ${t.hEst} × ${dinero(numSimple(l.tarifa))}${l.tope ? ` (${t.tope} ${l.tope} h)` : ""}` : t.cerrado;
    tp += `| ${celda(l.servicio)} | ${celda(l.incluye)} | ${modo} | ${dinero(montoLinea(l))} |\n`;
  });
  tp += `| | | **${t.sub}** | ${c.subtotal} |\n`;
  if (nombreImp) tp += `| | | **${nombreImp} ${pct}%** | ${c.impuesto_linea} |\n`;
  tp += `| | | **${t.total}** | **${c.total}** |\n`;
  c.tabla_precios = tp;
  let te = `| ${t.etapa} | ${t.dur} |\n|---|---|\n`;
  const et = e.etapas.filter(x => x.etapa || x.duracion);
  et.forEach(x => { te += `| ${celda(x.etapa)} | ${celda(x.duracion)} |\n`; });
  c.tabla_plazos = et.length ? te : "";
  return { c, sub, imp };
}

// ---------- Markdown mínimo ----------
function inline(s) {
  return s
    .replace(/\*\((.+?)\)\*/g, '<span class="hint">($1)</span>')
    .replace(/\*\[(.+?)\]\*/g, '<span class="nota">[$1]</span>')
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/\*(.+?)\*/g, "<em>$1</em>")
    .replace(/`(.+?)`/g, "<code>$1</code>");
}
function md(src) {
  const L = src.split("\n"); let h = "", i = 0;
  while (i < L.length) {
    const ln = L[i];
    if (!ln.trim()) { i++; continue; }
    let m;
    if ((m = /^(#{1,3}) (.*)/.exec(ln))) { h += `<h${m[1].length}>${inline(esc(m[2]))}</h${m[1].length}>`; i++; continue; }
    if (ln.startsWith(">")) { let b = []; while (i < L.length && L[i].startsWith(">")) b.push(L[i++].replace(/^> ?/, "")); h += `<blockquote>${b.map(x => inline(esc(x))).join("<br>")}</blockquote>`; continue; }
    if (ln.trim().startsWith("|")) {
      const rows = []; while (i < L.length && L[i].trim().startsWith("|")) rows.push(L[i++]);
      const cells = r => r.trim().replace(/^\||\|$/g, "").split("|").map(x => x.trim());
      const head = cells(rows[0]); const body = rows.slice(2).map(cells);
      const esNum = j => body.some(r => r[j]) && body.every(r => !r[j] || /^\**[A-Z$US€R]*\$?\s?[\d.,]+\**$|^\**(US\$|\$U|R\$)/.test(r[j]));
      h += "<table><thead><tr>" + head.map((x, j) => `<th${esNum(j) ? ' class="num"' : ""}>${inline(esc(x))}</th>`).join("") + "</tr></thead><tbody>";
      body.forEach(r => { const tot = r.some(x => /^\*\*(Total)\*\*$/.test(x)); h += `<tr${tot ? ' class="total"' : ""}>` + r.map((x, j) => `<td${esNum(j) ? ' class="num"' : ""}>${inline(esc(x))}</td>`).join("") + "</tr>"; });
      h += "</tbody></table>"; continue;
    }
    if (/^\s*- /.test(ln)) { h += "<ul>"; while (i < L.length && /^\s*- |^\s{2,}\S/.test(L[i])) { if (/^\s*- /.test(L[i])) h += `<li>${inline(esc(L[i].replace(/^\s*- /, "")))}`; else h += " " + inline(esc(L[i].trim())); i++; } h += "</ul>"; continue; }
    if (/^\d+\. /.test(ln)) { h += "<ol>"; while (i < L.length && /^\d+\. /.test(L[i])) h += `<li>${inline(esc(L[i++].replace(/^\d+\. /, "")))}</li>`; h += "</ol>"; continue; }
    let p = []; while (i < L.length && L[i].trim() && !/^(#|>|\||\s*- |\d+\. )/.test(L[i])) p.push(L[i++]);
    const txt = p.map(x => inline(esc(x))).join("<br>");
    h += /^<span class="hint">.*<\/span>$/.test(txt) ? `<p class="hint">${txt}</p>` : `<p>${txt}</p>`;
  }
  return h;
}

// ---------- Plantilla ----------
function plantilla() {
  const e = E(); const P = window.PLANTILLAS || {};
  const t = (P[e.idioma] || {})[doc];
  if (t) { aviso(""); return t; }
  aviso(e.idioma !== "es" ? `Este documento todavía no está traducido a ${e.idioma.toUpperCase()}: se muestra en español.` : "");
  return (P.es || {})[doc] || "# Falta la plantilla";
}
const claves = src => [...new Set([...src.matchAll(/\{\{(\w+)\}\}/g)].map(m => m[1]))];

function render() {
  const e = E(); const { c } = calculos();
  const val = k => (k in c && !["impuesto_pct"].includes(k) ? c[k] : k === "impuesto_pct" ? c.impuesto_pct : e.d[k]) || "";
  let src = plantilla()
    .split("\n").filter(ln => { const m = /^\{\{\?(\w+)\}\}/.exec(ln); return !m || !!val(m[1]); }).join("\n")
    .replace(/^\{\{\?\w+\}\}\s*/gm, "")
    .replace(/\{\{(tabla_\w+)\}\}/g, (_, k) => c[k] || "");
  let html = md(src);
  html = html.replace(/\{\{(\w+)\}\}/g, (_, k) => {
    const v = val(k);
    return v ? esc(v).replace(/\n/g, "<br>") : `<span class="vacio"><span>${esc(etiqueta(k))}</span></span>`;
  });
  const ref = doc === "propuesta" ? e.d.propuesta_numero : doc === "sow" ? e.d.sow_numero : doc === "cambio" ? e.d.oc_numero : e.d.contrato_numero;
  document.getElementById("papel").innerHTML =
    `<div class="cab"><img src="logo-positivo.svg" alt="Malackath"><div class="ref">${esc(ref || "")}<br>${esc(e.d.fecha || "")}</div></div>` + html +
    `<div class="pie"><span>${esc(e.d.prestador_nombre_fantasia || "Malackath")} · ${esc(e.d.prestador_email || "")}</span><span>${esc(e.d.cliente_razon_social || "")}</span></div>`;
  ajustarUnaPagina();
  const nd = DOCS.find(x => x.k === doc).n;
  document.title = `${nd} ${e.d.cliente_razon_social || ""} ${ref || ""}`.trim();
}

// La propuesta tiene que entrar en una sola A4 (pedido de Ber 2026-11-25):
// se mide con el ancho de impresión y se achica la letra hasta que entre.
const A4_ALTO_MM = 297 - 14 - 16, A4_ANCHO_MM = 210 - 28; // márgenes de @page
function ajustarUnaPagina() {
  const papel = document.getElementById("papel");
  papel.classList.toggle("una-pagina", doc === "propuesta");
  papel.style.removeProperty("--escala");
  document.getElementById("aviso").dataset.pagina = "";
  if (doc !== "propuesta") return;
  const mm = papel.getBoundingClientRect().width / 210; // px por mm en pantalla
  const medir = document.createElement("div");
  medir.className = "papel una-pagina medir";
  medir.innerHTML = papel.innerHTML;
  medir.style.width = A4_ANCHO_MM * mm + "px";
  document.body.appendChild(medir);
  let esc = 1;
  for (; esc > 0.62; esc -= 0.02) {
    medir.style.setProperty("--escala", esc);
    if (medir.scrollHeight <= A4_ALTO_MM * mm) break;
  }
  document.body.removeChild(medir);
  papel.style.setProperty("--escala", esc.toFixed(2));
  if (esc <= 0.62) aviso("La propuesta tiene demasiado texto para una sola página: acortá descripciones o líneas.");
}

// ---------- Formulario ----------
const F = document.getElementById("form");
function input(k, extra = {}) {
  const v = E().d[k] ?? "";
  const ml = extra.multi ?? MULTILINEA.test(k);
  const ph = AYUDA[k] ? ` placeholder="${esc(AYUDA[k])}"` : "";
  const list = extra.list ? ` list="${extra.list}"` : "";
  return `<div class="campo"><label class="etq" for="f_${k}">${esc(etiqueta(k))}</label>` +
    (ml ? `<textarea id="f_${k}" data-k="${k}"${ph}>${esc(v)}</textarea>` : `<input id="f_${k}" data-k="${k}" value="${esc(v)}"${ph}${list}>`) + `</div>`;
}
function sel(id, opts, v) { return `<select id="${id}">${opts.map(o => `<option${o === v ? " selected" : ""}>${esc(o)}</option>`).join("")}</select>`; }

function formulario() {
  const e = E(); const ks = claves(plantilla());
  const usadas = new Set();
  const usar = arr => arr.filter(k => !CALC.has(k)).map(k => { usadas.add(k); return input(k); }).join("");
  const pres = ks.filter(k => k.startsWith("prestador_"));
  const cli = ks.filter(k => k.startsWith("cliente_"));
  const ley = ["impuesto_nombre", "impuesto_pct", "nota_impuestos", "ley_aplicable", "jurisdiccion", "ley_datos_personales", "zona_horaria", "pais_dias_habiles"];
  let h = "";

  h += `<fieldset><legend>Documento</legend><div class="dos">
    <div class="campo"><label class="etq">Idioma</label>${sel("selIdioma", ["es", "en", "pt"], e.idioma)}</div>
    <div class="campo"><label class="etq">Moneda</label>${sel("selMoneda", Object.keys(MONEDAS), e.moneda)}</div></div>
    <div class="campo"><label class="etq" for="f_nombreExp">Nombre del expediente</label><input id="f_nombreExp" value="${esc(e.nombre)}"></div>
    ${usar([...ks.filter(k => /_numero$|^fecha$|^contrato_fecha$|^proyecto_nombre$|^validez_dias$/.test(k)), ...(doc === "propuesta" ? ["validez_dias"] : [])])}</fieldset>`;

  const perfiles = aj.perfiles.map((p, i) => `<option value="${i}">${esc(p.perfil || p.prestador_razon_social || "Perfil " + (i + 1))}</option>`).join("");
  h += `<fieldset><legend>Emisor (quien factura)</legend>
    <div class="dos"><div class="campo"><label class="etq">Cargar perfil</label><select id="selPerfil"><option value="">—</option>${perfiles}</select></div>
    <div class="campo"><label class="etq">País del emisor</label>${sel("selEmisorPais", PAISES, e.emisorPais)}</div></div>
    ${usar(pres.length ? pres : [])}
    ${aj.perfiles.length ? "" : '<p class="ayuda">Guardá tus datos como perfil en Ajustes para no tipearlos cada vez.</p>'}</fieldset>`;

  h += `<fieldset><legend>Cliente</legend>
    <div class="campo"><label class="etq">País del cliente</label>${sel("selClientePais", ["", ...PAISES], e.clientePais)}</div>
    ${usar(cli)}</fieldset>`;

  const leyDoc = ley.filter(k => ks.includes(k) || ["impuesto_nombre", "impuesto_pct"].includes(k));
  h += `<fieldset><legend>Impuesto y ley</legend>${usar(leyDoc)}
    <div class="fila-acc"><button type="button" id="btnSugerir">Sugerir según países</button></div>
    <p class="ayuda">Sugerencia, no asesoramiento: validar con contador y abogado.</p></fieldset>`;

  if (doc === "propuesta") {
    const tl = aj.tarifas.map(t => `<option value="${esc(t.tarifa)}">${esc(t.rol)} (${esc(t.moneda || "")})</option>`).join("");
    const cl = aj.catalogo.map(s => `<option value="${esc(s.servicio)}">`).join("");
    h += `<datalist id="dlTarifas">${tl}</datalist><datalist id="dlCatalogo">${cl}</datalist>`;
    h += `<fieldset><legend>Líneas del presupuesto</legend>` +
      e.lineas.map((l, i) => `<div class="linea" data-i="${i}">
        <input data-l="servicio" list="dlCatalogo" value="${esc(l.servicio)}" placeholder="Servicio (elegí del catálogo o escribí)">
        <input data-l="incluye" value="${esc(l.incluye)}" placeholder="Qué incluye">
        <div class="linea-n">
          <select data-l="modo"><option value="cerrado"${l.modo === "cerrado" ? " selected" : ""}>Precio cerrado</option><option value="horas"${l.modo === "horas" ? " selected" : ""}>Por horas</option></select>
          ${l.modo === "horas" ? `<input data-l="horas" value="${esc(l.horas)}" placeholder="Horas"><input data-l="tarifa" list="dlTarifas" value="${esc(l.tarifa)}" placeholder="Tarifa/h"><input data-l="tope" value="${esc(l.tope)}" placeholder="Tope h">` : `<input data-l="precio" value="${esc(l.precio)}" placeholder="Precio">`}
          <span class="monto">${esc(dinero(montoLinea(l)))}</span>
          <button type="button" class="mini" data-borrar="${i}" title="Quitar línea">×</button>
        </div></div>`).join("") +
      `<div class="fila-acc"><button type="button" id="btnLinea">+ Línea</button></div>
      <div class="tot" id="totales"></div></fieldset>`;
    h += `<fieldset><legend>Plazos</legend><table class="lineas"><tbody>` +
      e.etapas.map((x, i) => `<tr data-e="${i}"><td><input data-x="etapa" value="${esc(x.etapa)}" placeholder="Etapa"></td><td><input data-x="duracion" value="${esc(x.duracion)}" placeholder="Duración"></td><td><button type="button" class="mini" data-borrare="${i}">×</button></td></tr>`).join("") +
      `</tbody></table><div class="fila-acc"><button type="button" id="btnEtapa">+ Etapa</button></div></fieldset>`;
  }

  const resto = ks.filter(k => !usadas.has(k) && !CALC.has(k) && !k.startsWith("prestador_") && !k.startsWith("cliente_") && !ley.includes(k));
  if (resto.length) h += `<fieldset><legend>Campos de este documento</legend>${usar(resto)}</fieldset>`;
  h += `<p class="ayuda">Los campos vacíos se ven en amarillo en la vista previa y salen como línea en blanco en el PDF.</p>`;
  F.innerHTML = h;
  totales();
}
function totales() {
  const t = document.getElementById("totales"); if (!t) return;
  const { sub, imp } = calculos();
  t.innerHTML = `<span>Subtotal ${esc(dinero(sub))}</span><span>Imp. ${esc(dinero(imp))}</span><b>Total ${esc(dinero(sub + imp))}</b>`;
}

function aplicarSugerencias(forzar) {
  const e = E(); const s = sugerencias(e.emisorPais, e.clientePais);
  Object.entries(s).forEach(([k, v]) => { if (forzar || !e.d[k]) e.d[k] = v; });
  if (forzar || !e.d.prestador_id_fiscal_tipo) e.d.prestador_id_fiscal_tipo = ID_FISCAL[e.emisorPais] || e.d.prestador_id_fiscal_tipo || "";
  if (e.clientePais && (forzar || !e.d.cliente_id_fiscal_tipo)) e.d.cliente_id_fiscal_tipo = ID_FISCAL[e.clientePais] || e.d.cliente_id_fiscal_tipo || "";
}

// ---------- Eventos del formulario ----------
F.addEventListener("input", ev => {
  const el = ev.target, e = E();
  if (el.dataset.k) e.d[el.dataset.k] = el.value;
  else if (el.id === "f_nombreExp") { e.nombre = el.value; listaExp(); }
  else if (el.dataset.l) { const box = el.closest("[data-i]"); const i = +box.dataset.i; e.lineas[i][el.dataset.l] = el.value; if (el.dataset.l === "modo") { persistir(); formulario(); render(); return; } box.querySelector(".monto").textContent = dinero(montoLinea(e.lineas[i])); totales(); }
  else if (el.dataset.x) { const i = +el.closest("tr").dataset.e; e.etapas[i][el.dataset.x] = el.value; }
  persistir(); render();
});
F.addEventListener("change", ev => {
  const el = ev.target, e = E();
  if (el.id === "selIdioma") e.idioma = el.value;
  else if (el.id === "selMoneda") e.moneda = el.value;
  else if (el.id === "selEmisorPais") { e.emisorPais = el.value; aplicarSugerencias(false); }
  else if (el.id === "selClientePais") { e.clientePais = el.value; aplicarSugerencias(false); }
  else if (el.id === "selPerfil" && el.value !== "") {
    const p = aj.perfiles[+el.value]; Object.keys(p).forEach(k => { if (k.startsWith("prestador_")) e.d[k] = p[k]; });
    if (p.pais) e.emisorPais = p.pais; aplicarSugerencias(false);
  } else if (el.dataset.l === "modo") return; // ya manejado en input
  else return;
  persistir(); formulario(); render();
});
F.addEventListener("click", ev => {
  const el = ev.target, e = E();
  if (el.id === "btnLinea") e.lineas.push({ servicio: "", incluye: "", modo: "cerrado", horas: "", tarifa: "", precio: "", tope: "" });
  else if (el.dataset.borrar) e.lineas.splice(+el.dataset.borrar, 1);
  else if (el.id === "btnEtapa") e.etapas.push({ etapa: "", duracion: "" });
  else if (el.dataset.borrare) e.etapas.splice(+el.dataset.borrare, 1);
  else if (el.id === "btnSugerir") aplicarSugerencias(true);
  else return;
  persistir(); formulario(); render();
});

// ---------- Pestañas y barra ----------
function tabs() {
  document.getElementById("tabs").innerHTML = DOCS.map(d => `<button type="button" data-doc="${d.k}" class="${d.k === doc ? "on" : ""}">${esc(d.n)}</button>`).join("");
}
document.getElementById("tabs").addEventListener("click", ev => { const k = ev.target.dataset.doc; if (!k) return; doc = k; tabs(); formulario(); render(); });

function listaExp() {
  const s = document.getElementById("selExp");
  s.innerHTML = Object.entries(exps).filter(([, x]) => !x.archivado).sort((a, b) => b[1].actualizado - a[1].actualizado)
    .map(([id, x]) => `<option value="${id}"${id === actual ? " selected" : ""}>${esc(x.nombre)}${x.d.cliente_razon_social ? " · " + esc(x.d.cliente_razon_social) : ""}</option>`).join("");
}
document.getElementById("selExp").addEventListener("change", ev => { actual = ev.target.value; persistir(); todo(); });
document.getElementById("btnNuevo").addEventListener("click", () => { actual = nuevoExp(); persistir(); todo(); });
document.getElementById("btnDuplicar").addEventListener("click", () => {
  const copia = JSON.parse(JSON.stringify(E())); const id = nuevoExp();
  const numero = exps[id].d.propuesta_numero; exps[id] = copia; copia.nombre += " (copia)"; copia.d.propuesta_numero = numero; copia.d.fecha = hoy();
  actual = id; persistir(); todo();
});
document.getElementById("btnPDF").addEventListener("click", () => { document.body.classList.toggle("con-notas", document.getElementById("chkNotas").checked); window.print(); });

// Respaldo / restaurar
document.getElementById("btnRespaldo").addEventListener("click", () => {
  const blob = new Blob([JSON.stringify({ version: 1, ajustes: aj, expedientes: exps }, null, 1)], { type: "application/json" });
  const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = `malackath-presupuestos-${hoy().split("/").reverse().join("-")}.json`; a.click();
});
document.getElementById("btnRestaurar").addEventListener("click", () => document.getElementById("fileRestaurar").click());
document.getElementById("fileRestaurar").addEventListener("change", async ev => {
  const f = ev.target.files[0]; if (!f) return;
  try {
    const j = JSON.parse(await f.text());
    if (!j.expedientes || !j.ajustes) throw new Error("no es un respaldo de esta herramienta");
    // Suma, no reemplaza: lo que ya hay se conserva
    exps = Object.assign({}, j.expedientes, exps); aj = Object.assign({}, j.ajustes, { perfiles: [...j.ajustes.perfiles || [], ...aj.perfiles] });
    guardarLS(LS.aj, aj); persistir(); todo(); aviso("");
  } catch (e) { aviso("No se pudo cargar el respaldo: " + e.message); }
  ev.target.value = "";
});

// ---------- Pegar pedido del formulario público ----------
function decodificarPedido(txt) {
  const m = /MLK1:([A-Za-z0-9+/=_-]+)/.exec(txt || "");
  if (m) { const b = atob(m[1].replace(/-/g, "+").replace(/_/g, "/")); return JSON.parse(new TextDecoder().decode(Uint8Array.from(b, c => c.charCodeAt(0)))); }
  return JSON.parse(txt);
}
const dlg = document.getElementById("dlg"), dlgF = document.getElementById("dlgForm");
document.getElementById("btnPegar").addEventListener("click", () => {
  dlgF.innerHTML = `<h2>Pegar pedido</h2><p class="ayuda">Pegá el mail o el WhatsApp que llegó desde el formulario de malackath.com (incluye una línea que empieza con MLK1:). Se crea un expediente nuevo con esos datos.</p>
    <textarea id="txtPedido" style="min-height:180px"></textarea><p class="aviso" id="errPedido"></p>
    <div class="dlg-pie"><button value="cancel">Cancelar</button><button class="prim" id="btnImportar" value="">Crear expediente</button></div>`;
  dlg.showModal();
  document.getElementById("btnImportar").addEventListener("click", ev => {
    ev.preventDefault();
    try {
      const p = decodificarPedido(document.getElementById("txtPedido").value);
      const id = nuevoExp(p.empresa || p.nombre || "Pedido web"); const e = exps[id];
      e.d.cliente_razon_social = p.empresa || ""; e.d.cliente_contacto = p.nombre || ""; e.d.cliente_representante = p.nombre || "";
      e.d.cliente_email = p.email || ""; e.d.cliente_whatsapp = p.whatsapp || "";
      e.clientePais = PAISES.includes(p.pais) ? p.pais : (p.pais ? "Otro" : "");
      e.idioma = ["es", "en", "pt"].includes(p.idioma) ? p.idioma : "es";
      e.d.resumen_necesidad = [p.tipo && `Tipo: ${p.tipo}`, p.etapa && `Etapa: ${p.etapa}`, p.plazo && `Para: ${p.plazo}`, p.modo && `Forma de trabajo preferida: ${p.modo}`, p.mensaje].filter(Boolean).join("\n");
      const modo = /hora/i.test(p.modo || "") ? "horas" : "cerrado";
      e.lineas = (p.servicios || []).map(s => ({ servicio: s, incluye: "", modo, horas: "", tarifa: "", precio: "", tope: "" }));
      if (!e.lineas.length) e.lineas = [{ servicio: "", incluye: "", modo: "cerrado", horas: "", tarifa: "", precio: "", tope: "" }];
      actual = id; aplicarSugerencias(false); persistir(); dlg.close(); todo();
    } catch (err) { document.getElementById("errPedido").textContent = "No pude leer el pedido: " + err.message; }
  });
});

// ---------- Ajustes ----------
const CAMPOS_PERFIL = ["perfil", "pais", "prestador_razon_social", "prestador_nombre_fantasia", "prestador_id_fiscal_tipo", "prestador_id_fiscal", "prestador_domicilio", "prestador_representante", "prestador_email", "prestador_whatsapp"];
function ajustes() {
  const fila = (arr, campos, nombre) => arr.map((o, i) => `<tr>${campos.map(c => `<td><input data-a="${nombre}" data-i="${i}" data-c="${c}" value="${esc(o[c] || "")}" placeholder="${esc(c)}"></td>`).join("")}<td><button class="mini" data-q="${nombre}" data-i="${i}">×</button></td></tr>`).join("");
  dlgF.innerHTML = `<h2>Ajustes</h2><p class="ayuda">Se guardan solo en este navegador. Usá "Respaldo" para tener una copia.</p>
    <h3>Perfiles de emisor</h3>
    ${aj.perfiles.map((p, i) => `<div class="perfil">${CAMPOS_PERFIL.map(c => `<div class="campo"><label class="etq">${c === "perfil" ? "Nombre del perfil (ej.: Malackath Uruguay)" : c === "pais" ? "País" : esc(etiqueta(c))}</label>${c === "pais" ? `<select data-a="perfiles" data-i="${i}" data-c="pais">${PAISES.map(x => `<option${x === p.pais ? " selected" : ""}>${x}</option>`).join("")}</select>` : `<input data-a="perfiles" data-i="${i}" data-c="${c}" value="${esc(p[c] || "")}">`}</div>`).join("")}<button class="mini" data-q="perfiles" data-i="${i}">Quitar perfil</button></div>`).join("")}
    <button data-add="perfiles">+ Perfil</button>
    <h3>Tarifas sugeridas por hora</h3><table class="lineas"><tbody>${fila(aj.tarifas, ["rol", "tarifa", "moneda"], "tarifas")}</tbody></table><button data-add="tarifas">+ Tarifa</button>
    <h3>Catálogo de servicios</h3><table class="lineas"><tbody>${fila(aj.catalogo, ["servicio", "incluye"], "catalogo")}</tbody></table><button data-add="catalogo">+ Servicio</button>
    <h3>Numeración</h3><div class="campo"><label class="etq">Próximo número de propuesta</label><input data-num="1" value="${aj.proximoNumero}"></div>
    <div class="dlg-pie"><button class="prim" value="ok">Listo</button></div>`;
}
document.getElementById("btnAjustes").addEventListener("click", () => { ajustes(); dlg.showModal(); });
dlgF.addEventListener("input", ev => {
  const el = ev.target;
  if (el.dataset.a) { aj[el.dataset.a][+el.dataset.i][el.dataset.c] = el.value; guardarLS(LS.aj, aj); }
  if (el.dataset.num) { aj.proximoNumero = parseInt(el.value, 10) || 1; guardarLS(LS.aj, aj); }
});
dlgF.addEventListener("click", ev => {
  const el = ev.target;
  if (el.dataset.add) { ev.preventDefault(); aj[el.dataset.add].push(el.dataset.add === "perfiles" ? { pais: "Uruguay" } : {}); }
  else if (el.dataset.q) { ev.preventDefault(); aj[el.dataset.q].splice(+el.dataset.i, 1); }
  else return;
  guardarLS(LS.aj, aj); ajustes();
});
dlg.addEventListener("close", () => { if (dlgF.querySelector("h2")?.textContent === "Ajustes") { formulario(); render(); } });

// ---------- Inicio ----------
function todo() { listaExp(); tabs(); formulario(); render(); }
if (!E().d.impuesto_nombre && !E().d.ley_aplicable) aplicarSugerencias(false);
todo();
})();
