"""Ventanas flotantes del hero del home (bloque "showcase" de la pantalla
kinetic_home_kinetic_hero_animated de Stitch, con su flotado y su parallax).

Cada ventana es un "slot": se cambia acá y en ningún otro lado.
- imagen: ruta dentro de public/ (captura del sitio) o None para dejar la de Stitch.
- url: si se pone, la ventana es un link al sitio.
Los textos marcados PLACEHOLDER son los de Stitch (inventados): Ber pasa los sitios reales.
"""

SLOTS = {
    # ventana grande del centro (navegador)
    "centro": {
        # capturas reales del portfolio (pedido de Ber, 2026-11-25)
        "imagen": "img/portfolio/cartelera-d-01-818af77e.webp",
        "url": "https://cartelerauy.malackath.com",
        "barra": "cartelerauy.malackath.com",
        "barra_derecha": "APP",
        "rubro": "Agenda cultural",
        "titulo": "Cartelera Uruguay",
        "chip": "19 departamentos",
    },
    # ventana de la izquierda (navegador inclinado)
    "izquierda": {
        "imagen": "img/portfolio/ravekit-d-01-6c8c46e9.webp",
        "url": "https://getravekit.com",
        "barra": "getravekit.com",
        "chip": "RaveKit",
    },
    # celular de la derecha
    "celular": {
        "imagen": "img/portfolio/arma-partido-m-01-1e6e51fe.webp",
        "url": "casos/arma-partido.html",
        "chip": "App de pádel",
        "titulo": "Armá Partido",
    },
}

# chips flotantes sueltos
CHIP_METRICA = ("Proyectos", "22 en el portfolio")   # dato real (portfolio.malackath.com)
CHIP_FLOTANTE = "Marca, web y app"

# ---------------------------------------------------------------- ROTACIÓN
# Pedido de Ber (2026-11-25): las tres ventanas cambian de proyecto cada 5 segundos.
# La primera de cada lista es la de SLOTS (la que se ve al cargar). Capturas del portfolio:
# img = nombre del archivo en portfolio/public/img/p. url None = ficha en portfolio.malackath.com.
SEGUNDOS = 5
PF = "https://portfolio.malackath.com/#"
ROTACION = {
    "centro": [   # barra, tipo (arriba a la derecha), rubro, título, chip
        dict(img="cartelera-d-01-818af77e.webp", url="https://cartelerauy.malackath.com", barra="cartelerauy.malackath.com",
             tipo="App", rubro="Agenda cultural", titulo="Cartelera Uruguay", chip="19 departamentos"),
        dict(img="nunca-te-falla-d-01-81242e06.webp", url=PF + "nunca-te-falla", barra="Nunca Te Falla",
             tipo="App", rubro="Marketplace de oficios", titulo="Nunca Te Falla", chip="Cliente y profesional"),
        dict(img="marealta-consultora-d-01-3e963d07.webp", url="https://marealtagastro.com", barra="marealtagastro.com",
             tipo="Empresa", rubro="Consultoría gastronómica", titulo="Marea Alta", chip="Pernambuco, Brasil"),
        dict(img="barajala-d-01-71b09609.webp", url=PF + "barajala", barra="Barajala",
             tipo="App", rubro="Juegos de cartas", titulo="Barajala", chip="Baraja española"),
        dict(img="mesaluma-d-01-9a466b8e.webp", url="https://mesaluma.arnelli.com", barra="mesaluma.arnelli.com",
             tipo="App", rubro="Salón y reservas", titulo="Mesaluma", chip="App para mozos"),
    ],
    "izquierda": [   # barra, chip (nombre)
        dict(img="ravekit-d-01-6c8c46e9.webp", url="https://getravekit.com", barra="getravekit.com", chip="RaveKit"),
        dict(img="coinciva-d-01-1a29c0bc.webp", url=PF + "coinciva", barra="Coinciva", chip="Coinciva"),
        dict(img="zoomi-d-01-c4300158.webp", url=PF + "zoomi", barra="Zoomi", chip="Zoomi"),
        dict(img="jip-d-01-81bfe761.webp", url=PF + "jip", barra="JIP", chip="JIP"),
        dict(img="ecos-d-01-47491bb4.webp", url="https://ecos.arnelli.com", barra="ecos.arnelli.com", chip="ECOS"),
    ],
    "celular": [   # chip (rubro), título
        dict(img="arma-partido-m-01-1e6e51fe.webp", url="casos/arma-partido.html", chip="App de pádel", titulo="Armá Partido"),
        dict(img="pizcaya-m-01-cae56888.webp", url="casos/pizcaya.html", chip="Aprender a cocinar", titulo="Pizcaya"),
        dict(img="palquear-m-01-d953f0cc.webp", url="https://palquear.arnelli.com", chip="Palcos de fútbol", titulo="Palquear"),
        dict(img="ruvia-m-01-95ae4a53.webp", url=PF + "ruvia", chip="Transporte de Montevideo", titulo="RuVIA"),
        dict(img="patovava-m-01-0659b4b2.webp", url=PF + "patovava", chip="Traslados de noche", titulo="PatovaVa"),
    ],
}
