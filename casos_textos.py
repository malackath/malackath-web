"""Textos reales de los casos (reemplazan lo que Stitch inventó).

Fuentes verificadas:
- Armá Partido: CLAUDE.md y docs/revision-prototipo.md del repo malackath/armapartido.
- Pizcaya: CocinaApp/CLAUDE.md y CocinaApp/tienda/ficha-google-play.md.
Clave = texto de Stitch (espacios normalizados). Valor = texto nuevo ("" lo vacía).
"""

ARMA_PARTIDO = {
    "2024 — EN PRODUCCIÓN": "2026 — EN DESARROLLO",
    "SportTech · Padel Ecosystem": "SportTech · Pádel",
    "Proyecto Propio · Montevideo, Uruguay · iOS & Android Native Ecosystem":
        "Proyecto propio · Uruguay · App instalable para clubes y jugadores",
    "Product Strategy & Architecture": "Estrategia de producto",
    "Mobile Design System (Dual OS)": "App del jugador, panel del club y mostrador",
    "Real-Time WebSockets & Geo-Radar": "React + Firebase · App instalable (PWA)",
    "Integraciones": "Modelo",
    "SaaS de Clubes & Split Payment": "Una plataforma, una app con la marca de cada club",
    "EL MATCHMAKING DEFINITIVO PARA EL PÁDEL URUGUAYO": "PARTIDOS DE PÁDEL PAREJOS, ARMADOS POR CATEGORÍA",
    "Cómo transformamos la frustración cotidiana de WhatsApp en una experiencia fluida de 3 clics: categorización técnica automatizada por nivel ELO, confirmaciones en tiempo real y reserva de cancha 100% sincronizada con los turnos de los clubes.":
        "Cada jugador tiene una cuenta y una categoría, de 1ra a 8va. La app arma partidos de 2 contra 2 con jugadores de categoría pareja y horarios compatibles, y el club gestiona la cancha desde su mostrador. Cada club tiene su propia app con su marca, sobre una sola plataforma.",
    # mockups
    "09:41 · FEED EN VIVO": "09:41 · PARTIDOS ABIERTOS",
    "RADAR ACTIVO": "HOY",
    "Club Carrasco Pádel": "Tu club",
    "Cancha 2 Cristal Panorámica · Turno 90 min · Split $350 c/u": "Cancha 2 · Turno de 90 min",
    "MATCH CENTER": "PARTIDO ARMADO",
    "PARTIDO #4829 · PRADO CLUB": "2 CONTRA 2 · TU CLUB",
    "Drive vs Revés Balanceado": "Categoría pareja",
    "Nivel Promedio: 4ta Cat · ELO 1,480": "Nivel: 4ta categoría",
    "DRIVE 1": "JUGADOR 1", "REVÉS 1": "JUGADOR 2", "DRIVE 2": "JUGADOR 3",
    "4ta Cat (ELO 1490)": "4ta categoría", "4ta Cat (ELO 1510)": "4ta categoría", "4ta Cat (ELO 1450)": "4ta categoría",
    "SLOT LIBRE": "LUGAR LIBRE", "Revés Vacante": "Falta 1", "Tu Posición": "Sumate",
    "Compatibilidad de mesa": "Confirmados", "96%": "3 de 4",
    "UNIRME AL PARTIDO ⚡": "SUMARME AL PARTIDO",
    "CHECK-IN DIGITAL": "RESERVA",
    "Acceso Cancha 1 · PIN: 8092": "Cancha 1 · Hoy 20:30",
    "Costo Total Cancha": "Pago", "$1.400 UYU": "En el club",
    "Split Automático (1/4)": "Jugadores", "$350 UYU / jugador": "4 confirmados",
    "Estado de pago": "Mercado Pago", "4 de 4 Aprobados": "Próximamente",
    "Sincronizado con": "Reservado en", "Montevideo Pádel Hub": "Tu club",
    # desafío
    "El pádel experimentó un crecimiento exponencial del 180% en Uruguay en dos años. Sin embargo, la infraestructura operativa dependía de dinámicas informales que destruían la experiencia de juego.":
        "Armar un partido de pádel dependía de grupos de WhatsApp: encontrar a cuatro jugadores de nivel parecido, coordinar horarios y conseguir cancha, todo a mano.",
    "Un jugador de 3ra categoría emparejado con uno de 6ta genera partidos unilaterales y aburridos. Los grupos de chat no tenían criterio objetivo de nivelación ni autoevaluación verificada.":
        "Un jugador de 3ra categoría con uno de 6ta da partidos desparejos. Los grupos de chat no tienen un criterio para emparejar por nivel.",
    "El 34% de los partidos programados se cancelaban 2 horas antes porque un jugador avisaba que no llegaba, obligando al organizador a pagar el turno completo o perder la cancha.":
        "Cuando alguien avisa a último momento que no llega, el organizador tiene que salir a buscar reemplazo o perder la cancha.",
    "Un solo usuario asumía la reserva y luego debía perseguir transferencias bancarias de $300 a $450 UYU con comprobantes por mensaje privado, generando tensiones y demoras.":
        "Un jugador reserva y después tiene que cobrarles a los otros tres, con transferencias y comprobantes por mensaje.",
    "Capacidad Ociosa en Clubes": "Turnos libres en los clubes",
    "Los clubes mantenían horas pico con turnos vacíos simplemente porque no existía un canal directo para alertar a jugadores listos en un radio cercano de 5 kilómetros.":
        "Los clubes tienen turnos sin ocupar y no tienen un canal directo para avisarles a los jugadores que podrían jugarlos.",
    # pilares
    "TRES PILARES: ALGORITMO, LOBBY EN TIEMPO REAL & SYNC CON CLUBES": "TRES PILARES: CATEGORÍA, ARMADO DE PARTIDOS Y GESTIÓN DEL CLUB",
    "Algoritmo de Calibración ELO Dinámico": "Una cuenta y una categoría",
    "Categorías de 1ª a 7ª con puntuación matemática progresiva. Al finalizar el encuentro, los 4 participantes cargan y validan el marcador. El sistema recalibra la reputación deportiva y el nivel competitivo del usuario.":
        "Cada jugador tiene una sola cuenta y una categoría, de 1ra a 8va, que vale en todos los clubes de la plataforma. Sin puntajes decimales: se usa la categoría, como en la cancha.",
    "Métricas Evaluadas": "Lo que se tiene en cuenta",
    "Historial de Sets · Consistencia de asistencia · Rol táctico (Drive / Revés)": "Categoría · Disponibilidad semanal · Amigos",
    "Radar Geoespacial & Push Ultra-segmentado": "Armado de partidos y avisos",
    "Cuando un partido queda a falta de 1 jugador a menos de 90 minutos de empezar, la plataforma activa un radar de micro-localización. Emite notificaciones push prioritarias solo a jugadores coincidentes en nivel dentro de un radio de 5km.":
        "El jugador carga cuándo puede jugar y la app le propone partidos de 2 contra 2 con gente de su categoría. Los cuatro confirman dentro de un plazo y, si alguien se baja, entra el siguiente de la lista de espera. Los avisos llegan al celular.",
    "Velocidad de Llenado": "Formato",
    "Tiempo récord: 58 segundos en Carrasco Pádel": "2 contra 2 · Lista de espera · Avisos al celular",
    "Sincronización Bidireccional de Reservas": "Una app para cada club",
    "Integración nativa vía API con los sistemas de gestión de canchas de los clubes uruguayos. El turno se reserva automáticamente en el club sin intermediación telefónica y cada jugador abona únicamente su 25% mediante pasarela integrada.":
        "Cada club tiene su app con su marca, su panel de administración y una pantalla de mostrador con la grilla de canchas del día. Reservas, torneos con cuadro y ranking en la misma plataforma.",
    "Impacto Administrativo": "Pago",
    "Cero no-shows · Facturación automatizada para el club": "En el club · Mercado Pago, próximamente",
    # pantallas
    "UI Systems & Visual Design": "Sistema de UI y diseño visual",
    "PANTALLAS EN PRODUCCIÓN": "PANTALLAS DE LA APP",
    "Diseñado bajo condiciones reales: pantalla táctil en movimiento, alto contraste para visibilidad bajo reflectores nocturnos de cancha y tipografía de lectura técnica rápida.":
        "Pensadas para usar en el club: el celular en la mano entre partido y partido, y la pantalla del mostrador a la vista de todos.",
    "SCREEN 01": "PANTALLA 01", "SCREEN 02": "PANTALLA 02", "SCREEN 03": "PANTALLA 03", "SCREEN 04": "PANTALLA 04",
    "Onboarding & Ranking ELO": "Tu categoría",
    "Evaluador inicial de 5 factores: años jugando, frecuencia semanal, golpe dominante, posición táctica y torneos federados previos.":
        "Cada jugador se ubica en su categoría, de 1ra a 8va, y con ella entra a los partidos de su nivel.",
    "01 // PRECISIÓN DE PERFIL": "01 // CATEGORÍA",
    "Radar & Filtros de Partidos": "Horarios",
    "Exploración por distancia, tipo de pista (blindex panorámica o muro clásico), horario nocturno y compatibilidad con el ELO del usuario.":
        "El jugador marca cuándo puede jugar en la semana y la app busca partidos en esos horarios.",
    "02 // EXPLORACIÓN GEO": "02 // DISPONIBILIDAD",
    "Lobby & Posición en Cancha": "Avisos",
    "Selección explícita de Drive o Revés para balancear la pareja, chat de mesa sincronizado y cuenta regresiva de confirmación de asistencia.":
        "Cuando se arma un partido o se libera un lugar llega el aviso, y se confirma con un toque.",
    "03 // LOBBY SINCRONIZADO": "03 // AVISOS",
    "Wallet & Registro de Resultados": "Perfil",
    "Carga del score (sets y super-tiebreak), verificación recíproca entre parejas y split payment con transferencias instantáneas.":
        "Categoría, amigos y ranking del jugador en un solo lugar.",
    "04 // SPLIT & RANKING": "04 // PERFIL",
    "Tipografías: Syne (Titulares Cinematográficos) & Space Mono (Data / ELO)": "Tipografías: Syne (titulares) & Space Mono (datos)",
    # siguiente caso y contacto
    "EdTech · UX Research · Gamificación interactiva en cocina paso a paso": "EdTech · Aprender a cocinar con lecciones cortas, voz y juego",
    "Desde la concepción del producto y UX architecture hasta el desarrollo de interfaces nativas de alto rendimiento. Construimos software con impacto comercial medible.":
        "Desde la idea y el diseño del producto hasta la app funcionando. Diseñamos y construimos productos digitales propios y para clientes.",
}

PIZCAYA = {
    "2024 — EN PRODUCCIÓN // BILINGÜE ES/EN": "2026 // WEB Y ANDROID",
    "PROYECTO PROPIO // EDTECH & FOOD INNOVATION": "PROYECTO PROPIO // EDTECH · COCINA",
    "Montevideo & San Pablo · Web & Mobile Dual Experience · Asistente Culinario Hands-Free":
        "Uruguay · App web instalable y Android · Modo cocina manos libres",
    "PROBAR MODO COCINA EN VIVO": "PROBAR PIZCAYA",
    "EdTech & Food Innovation": "EdTech · Cocina",
    "Pedagogía visual atomizada": "Lecciones cortas paso a paso",
    "Voice-Assisted Cooking UI": "Modo cocina con voz",
    "Gamified Micro-Lessons & Design System": "Juego, recetario y sistema de diseño",
    "Next.js + Web Audio API": "HTML, CSS y JavaScript + Firebase",
    "Real-time Speech Engine & Timers": "Voz del navegador · MediaPipe · IA",
    "Idiomas & Acentos": "Idioma",
    "ES & EN Native": "Español e inglés",
    "Rioplatense, Ibérico & General US": "Según el idioma del navegador",
    "APRENDER A COCINAR SIN MANCHAR LA PANTALLA: CULINARIA INTERACTIVA PASO A PASO":
        "APRENDER A COCINAR SIN MANCHAR LA PANTALLA: 15 PLATOS DE CASA EN 30 DÍAS",
    "Pizcaya nació para eliminar la frustración de pausar videos con las manos llenas de masa o aceite. Diseñamos un sistema de micro-lecciones audiovisuales con control por voz, sincronización de tiempos en tiempo real y una arquitectura pedagógica que convierte recetas complejas en secuencias modulares de 3 minutos.":
        "Pizcaya enseña a cocinar platos de casa con lecciones cortas, paso a paso, con imágenes y voz. En el modo cocina la app lee cada paso en voz alta y avanza cuando decís «listo», así no tocás el celular con las manos sucias.",
    # mockup modo cocina
    "Pizcaya Cooking Engine v2.4 // Modo Manos Libres Activo": "Pizcaya // Modo cocina manos libres",
    "Micrófono Omnidireccional: ON": "Micrófono: activado",
    "Paso 04 / 08 · Sofreír tomate y pimentón": "Paso 04 / 08 · Saltear la cebolla",
    "Técnica: Fuego Medio": "Técnica: salteado",
    "Escuchando comando:": "Escuchando:",
    "\"Siguiente paso\"": "\"Listo\"",
    "Confianza acústica: 98.4%": "Pasa al paso siguiente",
    "01 Mise": "01 Mesada", "02 Sellar": "02 Lavar", "03 Verdura": "03 Cortar", "04 Sofrito": "04 Saltear",
    "05 Caldo": "05 Cocinar", "06 Arroz": "06 Condimentar", "07 Socarrat": "07 Servir", "08 Reposo": "08 Foto",
    "Añadir el azafrán molido y sofreír por 45 seg.": "Saltear la cebolla a fuego medio durante 10 minutos.",
    "Remover continuamente para evitar que el pimentón dulce se queme con el fondo de la paella. Mantener temperatura a 140°C.":
        "Revolvé cada tanto para que no se pegue. Cuando esté transparente, decí «listo».",
    "Comando rápido": "Comando de voz",
    "«Repetir instrucción»": "«Listo»",
    "Multi-Timer Cruzado": "Reloj del paso",
    "SINCRONIZADO": "EN CURSO",
    "Reducción Sofrito": "Saltear la cebolla",
    "Fuego Medio-Bajo": "Fuego medio",
    "05:30": "10:00",
    "Cocción Arroz Bomba": "Paso siguiente",
    "En espera del hervor": "Cocinar",
    "18:00": "--:--",
    "\"Pizcaya, agregar 2 minutos\"": "\"listo\"",
    "para extender el timer en curso.": "y la app pasa al paso siguiente.",
    "Ingredientes en Mesa": "Armá tu mesada",
    "6 de 6 listos": "3 de 3 listos",
    "400g Arroz Bomba D.O. Valencia": "1 cebolla", "Medido": "Pelada",
    "1.2L Caldo de Pollo & Romero": "Aceite", "Caliente": "A mano",
    "Hebras de Azafrán Natural": "Sal", "Tostadas": "A mano",
    "Balance Nutricional": "Técnicas",
    "Porción 420 kcal": "Lecciones cortas",
    "Proteína": "Cortes", "28g": "✓", "Carbos": "Salteado", "54g": "✓", "Grasas": "Amasado", "11g": "✓",
    "Cálculo en vivo ajustado por número de comensales (4 pax).": "Cortes, salteado, hervido, amasado y más.",
    "Lupa de Textura": "Verificación por video",
    "Punto de Socarrat": "Grabá tu técnica",
    "AUDIO: Crujido óptimo": "La app te dice cómo te salió",
    "Validación acústica por micro-espectrograma de fritura.": "El video se analiza en tu celular: no se sube a ningún lado.",
    # diagnóstico
    "Diagnóstico del Problema": "Diagnóstico del problema",
    "Puntos de Dolor en la Cocina Doméstica Contemporánea": "Lo que frena a quien recién empieza a cocinar",
    "[FRICTION 01]": "[FRICCIÓN 01]", "[FRICTION 02]": "[FRICCIÓN 02]", "[FRICTION 03]": "[FRICCIÓN 03]", "[FRICTION 04]": "[FRICCIÓN 04]",
    "Tocar pantallas con manos mojadas, engrasadas o con harina interrumpe el flujo culinario y ensucia o deteriora tablets y teléfonos. La dependencia de toques físicos es el principal desincentivo para seguir recetas digitales.":
        "Tocar la pantalla con las manos mojadas, con aceite o con harina corta el ritmo y ensucia el celular.",
    "Sobrecarga Cognitiva en Videos Largos": "Videos largos",
    "Los videos de YouTube de 15 minutos obligan a rebobinar constantemente, perder el punto exacto de cocción de una salsa y memorizar listas extensas de pasos que saturan la atención de quien está frente al fuego.":
        "Los videos largos obligan a volver atrás para encontrar el paso y a recordar listas de pasos mientras estás frente al fuego.",
    "Falta de Validación de Técnicas": "Nadie te dice si te salió bien",
    "El cocinero principiante no sabe identificar visualmente cuándo una emulsión está a punto de cortarse o cuándo el sofrito alcanzó su caramelización idónea sin una referencia comparativa en primer plano.":
        "Quien recién empieza no sabe si cortó bien o si la técnica le salió, porque no tiene a nadie al lado que lo mire.",
    "Desincronización de Tiempos": "Recetas para los que ya saben",
    "Cocinar plato principal, guarnición y reducción a la vez produce platos servidos fríos o vegetales pasados. La falta de timers coordinados entre múltiples hornallas arruina el resultado final.":
        "Muchas recetas dan por sentado que sabés cortar, saltear o amasar. Primero hay que aprender la técnica.",
    # pilares
    "Arquitectura de Solución": "Cómo lo resolvimos",
    "Los Tres Pilares Tecnológicos de Pizcaya": "Los tres pilares de Pizcaya",
    "Hands-Free Voice Navigation": "Modo cocina manos libres",
    "Latencia de respuesta": "Voz",
    "< 140ms": "Del navegador, gratis",
    "Micro-Learning Modular Culinario": "Lecciones cortas y técnicas",
    "Deconstrucción de recetas en bloques atómicos autoconclusivos de 45 a 90 segundos. Cada micro-bloque contiene su video en bucle de la técnica, temperatura recomendada, checklist de control y lupas macro de textura culinaria.":
        "Tres caminos: cocina básica, técnicas y recetas. Cada lección es corta y va paso a paso, con imágenes y voz. Grabás tu técnica y la app te dice cómo te salió, sin subir el video.",
    "Granularidad pedagógica": "Caminos",
    "1 Acción = 1 Card": "Básica · Técnicas · Recetas",
    "Multi-Timer Inteligente Cruzado": "Recetario que crece y juego",
    "Algoritmo de solapamiento temporal que calcula los momentos exactos de inicio de cada preparación secundaria para que proteína, guarnición y emulsión lleguen al plato en el segundo exacto sin enfriamiento ni pérdidas organolépticas.":
        "Más de 30 recetas paso a paso, ordenadas por tipo e ingredientes. Si la que buscás no está, la inteligencia artificial te la arma con su clase. Puntos, racha, logros y una liga semanal para seguir con ganas.",
    "Precisión sincronizada": "Modelo",
    "Offset ± 0.5s": "Gratis · Sin publicidad",
    # pantallas
    "Showcase Visual": "Pantallas",
    "Pantallas Diseñadas para Alto Rendimiento": "Pantallas de la app",
    "Resolución: 4K Retina // Darkroom Ready": "Web y Android",
    "SCREEN 01 // BIBLIOTECA & FILTROS": "PANTALLA 01 // RECETARIO",
    "Explorador de Técnicas & Despensa Dinámica": "Recetario",
    "Filtrado inteligente que calcula recetas viables a partir de ingredientes ya existentes en la heladera, ordenadas por tiempo disponible del usuario.":
        "Recetas paso a paso con fotos, agrupadas por tipo e ingredientes.",
    "SCREEN 02 // MODO COCINA ACTIVO (HUD)": "PANTALLA 02 // MODO COCINA",
    "Modo Cocina Activo (Voice HUD a 2 Metros)": "Armá tu mesada",
    "Tipografía brutalista ultra-condensada de máxima legibilidad a distancia, pensada para apoyar la tablet en el alféizar o campana extractora.":
        "Antes de empezar, la app te muestra todo lo que tenés que tener a mano.",
    "SCREEN 03 // GESTIÓN DE FUEGOS": "PANTALLA 03 // DESAFÍO",
    "Multi-Timer Radial & Fuego Paralelo": "15 platos en 30 días",
    "Temporizadores radiales interactivos con código cromático según el grado de atención requerido (crítico, supervisión, fuego pasivo).":
        "Cada día un plato real, del tostado perfecto a la tarta de verdura.",
    "SCREEN 04 // PROGRESO GAMIFICADO": "PANTALLA 04 // INICIO",
    "Árbol de Habilidades & Masterclasses": "Progreso y liga",
    "Sistema de progresión inspirado en brigadas gastronómicas: dominio de cuchillo, emulsiones frías, fondos oscuros y panificación madre.":
        "Puntos, racha, logros y una liga semanal para competir con otros cocineros.",
    "Color Calibration": "Color",
    "Paleta Culinaria de Alto Contraste": "Paleta de Pizcaya",
    "Warm Saffron #FF9E00": "Paprika #E8572A",
    "Olive Herb #70A040": "Albahaca #3E8E5A",
    "Acid Lime #CAF300": "Miel #F4B740",
    "Obsidian Kitchen #121214": "Crema #FFF7EC",
    # siguiente y contacto
    "PALQUEAR — SISTEMA DE CESIÓN DE PALCOS & ENTRADAS": "PALQUEAR — PALCOS DE FÚTBOL",
    "Arquitectura de Ticketing en Tiempo Real & WebSockets para Estadios de Fútbol en América Latina.":
        "Proyecto propio. Mirá este y el resto de los proyectos.",
    "¿Tenés un producto de alto impacto en mente?": "¿Tenés un producto en mente?",
    "Llevemos tu visión a producción con diseño de precisión y código de escala.":
        "Lo diseñamos y lo construimos con vos, de la idea a la app funcionando.",
}


# Menú, pie y rótulos comunes de Stitch (venían en inglés) -> español
COMUN = {
    "Available for Q3/Q4 Projects": "Disponibles para proyectos nuevos",
    "Work": "Trabajo", "Services": "Servicios", "Studio": "Estudio", "Case Studies": "Casos",
    "Start a Project": "Iniciar proyecto",
    "Initiate Collaboration": "Empecemos",
    "LET'S BUILD THE FUTURE TOGETHER": "CONSTRUYAMOS EL FUTURO JUNTOS",
    "Global Timezones": "Husos horarios",
    "Privacy Policy": "Privacidad", "Terms of Service": "Términos", "Impressum": "Aviso legal",
    # Armá Partido es un prototipo (repo armapartido, docs/revision-prototipo.md)
    "EN PRODUCCIÓN": "EN DESARROLLO", "En Producción": "En Desarrollo",
}

# data-alt de los fondos del caso Armá Partido (Stitch traía sus prompts en inglés)
ALT_ARMA_PARTIDO = [
    "Cancha de pádel techada",
    "Armá Partido: elegí tu categoría",
    "Armá Partido: tus horarios de la semana",
    "Armá Partido: avisos de partidos",
    "Armá Partido: perfil del jugador",
]
