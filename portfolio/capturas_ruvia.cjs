// Saca capturas de celular de la app RuVIA actual (claro y oscuro) para el portfolio.
// Uso: servir ~/Projects/RuVIA/app/dist en http://localhost:8765 y correr:
//   node portfolio/capturas_ruvia.cjs ~/Projects/Malackath/_capturas-vivas/ruvia
const { chromium } = require('playwright');
const fs = require('fs');
const OUT = process.argv[2]; fs.mkdirSync(OUT, { recursive: true });
const TABS = [['01','buscar','Buscar'],['02','mapa-rutas','Mapa y rutas'],['03','tarjeta-stm','Tarjeta STM'],['04','paradas','Paradas'],['05','mas','Más']];
const cerrarAviso = async pg => { const e = pg.getByRole('button', { name: 'Entendido' }); if (await e.count() && await e.first().isVisible()) { await e.first().click(); await pg.waitForTimeout(400); } };
// vuelve todo arriba (ventana y contenedores con scroll)
const scroll = pg => pg.evaluate(() => { window.scrollTo(0, 0); document.querySelectorAll('*').forEach(el => { if (el.scrollTop) el.scrollTop = 0; }); });
(async () => {
  const b = await chromium.launch();
  for (const tema of ['oscuro', 'claro']) {
    const ctx = await b.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2, isMobile: true, hasTouch: true, serviceWorkers: 'block', timezoneId: 'America/Montevideo', locale: 'es-UY' });
    const pg = await ctx.newPage();
    await pg.goto('http://localhost:8765/', { waitUntil: 'networkidle', timeout: 30000 }).catch(() => {});
    await pg.waitForTimeout(2000); await cerrarAviso(pg);
    if (tema === 'claro') { await pg.getByRole('button', { name: 'Modo claro' }).first().click(); await pg.waitForTimeout(800); }
    for (const [n, slug, label] of TABS) {
      await pg.locator('button').filter({ hasText: new RegExp('^' + label + '$') }).last().click();
      await pg.waitForTimeout(3500); await cerrarAviso(pg);
      await scroll(pg); await pg.waitForTimeout(600);
      await pg.screenshot({ path: `${OUT}/movil-${tema}-${n}a-${slug}.png` });
      await pg.mouse.move(195, 450); await pg.mouse.wheel(0, 600); await pg.waitForTimeout(1200);
      const movio = await pg.evaluate(() => Math.max(window.scrollY, ...[...document.querySelectorAll('*')].map(el => el.scrollTop)));
      if (movio > 300) await pg.screenshot({ path: `${OUT}/movil-${tema}-${n}b-${slug}.png` });
      console.log(tema, slug, 'scroll', movio);
    }
    await ctx.close();
  }
  await b.close();
})();
