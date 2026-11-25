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
 dict(c='marea-alta', n='Marea Alta Digital', t='Empresa', d='La parte digital de Marea Alta: sitios, apps y casos para gastronomía.',
      logo='logo-MareAlta-transparente-para-fondo-oscuro.png', fondo='oscuro'),
 dict(c='marealta-consultora', n='Marea Alta Consultoría y Escuela', t='Empresa', d='Consultoría gastronómica y escuela de cocina profesional en Pernambuco, Brasil.',
      logo=None, fondo='oscuro', logo_archivo='assets/marealta-logo-oscuro.png'),
 dict(c='mesaluma', n='Mesaluma', t='App', d='Sistema de salón, reservas y comandas para restaurantes: app para mozos, reservas web y panel de cocina.',
      logo='mesaluma-horizontal.png', fondo='claro'),
 dict(c='palquear', n='Palquear', t='App', d='Marketplace de palcos para partidos: comprador, titular del palco y panel del club.',
      logo='logo-transparente-para-fondo-oscuro.png', fondo='oscuro'),
 dict(c='pizcaya', n='Pizcaya', t='App', d='Aprender a cocinar jugando.',
      logo='logo-horizontal-transparente.png', fondo='claro'),
 dict(c='ruvia', n='RuVIAJE', t='App', d='Rutas, paradas y tarjeta STM del transporte de Montevideo.',
      logo=None, fondo='oscuro', logo_archivo='assets/ruviaje-logo-oscuro.png'),  # logo nuevo RuVIAJE (RuVIA/design/logo-ruviaje/final)
 dict(c='banana-team', n='The Banana Team', t='Empresa', d='Helping customers go live.',
      logo='02-logo-sobre-negro.png', fondo='lamina'),
 dict(c='nunca-te-falla', n='Nunca Te Falla', t='App', d='Marketplace de oficios: el cliente pide presupuesto y reserva, el profesional gestiona desde su panel.',
      logo='ntf-logo-horizontal-negativo-2000.png', fondo='oscuro',
      logo_archivo='assets/ntf-logo-horizontal-sobre-negro.svg', temas=('Cliente', 'Profesional')),  # sobre negro (pedido de Ber): crema pasa a lima, lima pasa a negro
 dict(c='ravekit', n='RaveKit', t='App', d='Autonomous reputation.', logo='01-logo-fondo-oscuro.png', fondo='lamina'),
 dict(c='ecos', n='ECOS', t='App', d='Ecos de vos: comunidad de contención emocional.', logo='logo-02-fondo-oscuro.png', fondo='lamina'),
 dict(c='velvet', n='Velvet', t='App', d='Perfiles, agenda y reservas con seña en custodia.', logo='velvet-logo-light-outline-tight.png', fondo='oscuro'),
 dict(c='patovava', n='PatovaVa', t='App', d='Acompañantes verificadas que llevan y traen a tus hijos de noche.', logo='lockup-color-fondo-oscuro.png', fondo='oscuro'),
 dict(c='jip', n='JIP', t='Tienda', d='Jamás lo permitiría: remeras con configurador y fábulas.', logo='B_parche_sobre_negro.png', fondo='lamina'),
 dict(c='zoomi', n='Zoomi', t='Tienda online', d='Tienda online de Zoomi, la pelota interactiva que entretiene a tu gato cuando no estás.', logo='zoomi-transparente.png', fondo='claro', json='coat-n-nest'),
 dict(c='coat-n-nest', n='Coat n Nest', t='Logo', d='Identidad de Coat n Nest, la empresa detrás de Zoomi.', logo='coatnnest-una-tinta.png', fondo='oscuro', solo_logo=True),
 dict(c='sitios-gastro', n='Sitios Gastro', t='Sitios web', d='5 sitios de restaurantes: Botánica Bistro, Brisa & Marea, Fuego & Puerto, Fuego Silvestre y Oceánica.',
      logo='fuego-silvestre__logo__para-fondo-oscuro__con-fondo.png', fondo='oscuro'),
 dict(c='la-gloria', n='La Gloria', t='Sitio web', d='Sitio del restaurante La Gloria.', logo=None, fondo='lamina'),
 dict(c='usa-storefront', n='UsaStorefront', t='Empresa', d='Tienda de insumos de tapicería en EE. UU. (Upholstery Supplies of America).', logo=None, fondo='lamina'),
 dict(c='web-arnelli', n='Web Arnelli', t='Sitio web', d='Sitio del artista plástico Bernardo Arnelli: obras, exposiciones y contacto.', logo=None, fondo='lamina'),
]

# Sin logo propio (La Gloria, UsaStorefront, Web Arnelli): el recuadro usa la primera captura de escritorio.
PENDIENTES = {}
