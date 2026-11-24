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
        "imagen": "img/hero/slot-1-placeholder.webp",
        "url": None,
        "barra": "monolith.spatial.os",          # PLACEHOLDER
        "barra_derecha": "WEBGL / SHADER",       # PLACEHOLDER
        "rubro": "Next-Gen FinTech",             # PLACEHOLDER
        "titulo": "Monolith Quantum Yield",      # PLACEHOLDER
        "chip": "+240% Conv Rate",               # PLACEHOLDER (métrica inventada)
    },
    # ventana de la izquierda (navegador inclinado)
    "izquierda": {
        "imagen": "img/hero/slot-2-placeholder.webp",
        "url": None,
        "barra": "solana-orbit.app",             # PLACEHOLDER
        "chip": "FWA of the Day",                # PLACEHOLDER (premio inventado)
    },
    # celular de la derecha
    "celular": {
        "imagen": "img/hero/slot-3-placeholder.webp",
        "url": None,
        "chip": "Apple Design Award Nominee",    # PLACEHOLDER (premio inventado)
        "titulo": "Aura KineticOS",              # PLACEHOLDER
    },
}

# chips flotantes sueltos
CHIP_METRICA = ("Benchmark Performance", "0.18s FCP / 100 SEO")   # PLACEHOLDER (métrica inventada)
CHIP_FLOTANTE = "WebGL 2.0 Native Flow"                            # PLACEHOLDER
