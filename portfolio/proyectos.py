# Proyectos que salen en portfolio.malackath.com (versión pública).
# Solo datos públicos: nombre, tipo, descripción de una línea y qué logo usar.
# logo: nombre del archivo dentro del JSON del fichero; fondo: color del recuadro del logo
# ('oscuro', 'claro' o 'lamina' si la imagen ya trae su fondo).
PUBLICOS = [
 dict(c='arma-partido', n='Armá Partido', t='App', d='Reservas, partidos y torneos de pádel para clubes.',
      logo='logo-transparente-para-fondo-oscuro.png', fondo='oscuro'),
 dict(c='barajala', n='Barajala', t='App', d='Juegos de cartas con baraja española: truco, escoba, tute, canasta y más.',
      logo='barajala-logo-fondo-oscuro.png', fondo='lamina'),
 dict(c='cartelera', n='Cartelera Uruguay', t='App', d='Agenda cultural de los 19 departamentos, con mapa, calendario y fichas de evento.',
      logo='logo-horizontal-sobre-oscuro-3200x2400.png', fondo='lamina'),
 dict(c='coinciva', n='Coinciva', t='App', d='Descubrimiento social para eventos presenciales.',
      logo='coinciva-logo-transparente-para-fondo-oscuro.png', fondo='oscuro'),
 dict(c='marea-alta', n='Marea Alta', t='Empresa', d='Consultora gastronómica.',
      logo='logo-MareAlta-transparente-para-fondo-oscuro.png', fondo='oscuro'),
 dict(c='mesaluma', n='Mesaluma', t='App', d='Reservas inteligentes, prepedido y coordinación salón-cocina para restaurantes.',
      logo='mesaluma-horizontal.png', fondo='claro'),
 dict(c='palquear', n='Palquear', t='App', d='Marketplace de palcos para partidos: comprador, titular del palco y panel del club.',
      logo='logo-transparente-para-fondo-oscuro.png', fondo='oscuro'),
 dict(c='pizcaya', n='Pizcaya', t='App', d='Aprender a cocinar jugando.',
      logo='logo-horizontal-transparente.png', fondo='claro'),
 dict(c='ruvia', n='RuVIA', t='App', d='Rutas, paradas y tarjeta STM del transporte de Montevideo.',
      logo='RuVIA-logo-oscuro-transparente.png', fondo='oscuro'),
 dict(c='banana-team', n='The Banana Team', t='Empresa', d='Helping customers go live.',
      logo='02-logo-sobre-negro.png', fondo='lamina'),
]

# Esperan el OK de Ber para salir (no se publican):
# Nunca Te Falla, RaveKit, ECOS, Velvet, PatovaVa, JIP, Coat n Nest, Sitios Gastro.
# Sin logo (fuera): La Gloria, UsaStorefront, Web Arnelli.
PENDIENTES = {
 'nunca-te-falla': dict(n='Nunca Te Falla', t='App', d='Marketplace de oficios: el cliente pide presupuesto y reserva, el profesional gestiona desde su panel.',
      logo='ntf-logo-horizontal-negativo-2000.png', fondo='oscuro'),
 'ravekit': dict(n='RaveKit', t='App', d='Autonomous reputation.', logo='01-logo-fondo-oscuro.png', fondo='lamina'),
 'ecos': dict(n='ECOS', t='App', d='Ecos de vos: comunidad de contención emocional.', logo='logo-02-fondo-oscuro.png', fondo='lamina'),
}
