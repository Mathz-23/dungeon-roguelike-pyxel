# Recargas em quadros; o jogo roda a 30 FPS.
ARMAS = {
    "soco": {
        "nome": "Soco", "dano": 3, "recarga": 45,
        "alcance": 15, "largura": 10,
    },
    "manopla": {
        "nome": "Manopla", "dano": 6, "recarga": 39,
        "alcance": 15, "largura": 10,
    },
    "espada": {
        "nome": "Espada", "dano": 8, "recarga": 30,
        "alcance": 16, "largura": 10,
    },
    "espada_grande": {
        "nome": "Espada Grande", "dano": 8, "recarga": 90,
        "alcance": 24, "largura": 30,
    },
}


def atributos_arma(tipo, nivel):
    arma = ARMAS[tipo]
    dano = arma["dano"] + 2 * nivel
    recarga = arma["recarga"]
    if tipo == "manopla":
        recarga = max(3, recarga - 3 * nivel)
    return dano, recarga
