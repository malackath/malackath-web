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
