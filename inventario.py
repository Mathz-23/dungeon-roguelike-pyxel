import random

from upgrades import Manopla, Espada, EspadaGrande, Armadura, VidaExtra, BotaCeleridade, PassoSombrio, AuraEspinhos, CuraContinua


upgrades = [
    Manopla,
    Espada,
    EspadaGrande,
    Armadura,
    VidaExtra,
    BotaCeleridade,
    PassoSombrio,
    AuraEspinhos,
    CuraContinua
]


def sortear_upgrades(jogador=None):

    disponiveis = list(upgrades)

    if jogador is not None:

        tipo_arma = jogador.arma["tipo"]

        # Manopla só pode ser pega enquanto ainda está no soco.
        if tipo_arma != "soco":
            disponiveis.remove(Manopla)

        # Depois de pegar Espada Grande,
        # a espada comum não aparece mais.
        if tipo_arma == "espada_grande":
            disponiveis.remove(Espada)

        # Upgrades únicos
        if jogador.upgrades["armadura"]:
            disponiveis.remove(Armadura)

        if jogador.upgrades["aura_espinhos"]:
            disponiveis.remove(AuraEspinhos)

    escolhas = random.sample(disponiveis, 2)

    opcoes = []

    for escolha in escolhas:

        if jogador is not None and escolha is Espada:

            if jogador.arma["tipo"] == "espada":
                nivel_atual = jogador.arma["nivel"] + 1
            else:
                nivel_atual = 0

            opcoes.append(Espada(nivel_atual))

        elif jogador is not None and escolha is EspadaGrande:

            if jogador.arma["tipo"] == "espada_grande":
                nivel_atual = jogador.arma["nivel"] + 1
            else:
                nivel_atual = 0

            opcoes.append(EspadaGrande(nivel_atual))

        elif jogador is not None and escolha is CuraContinua:

            opcoes.append(
                CuraContinua(jogador.upgrades["cura_continua"])
            )

        else:
            opcoes.append(escolha())

    return opcoes
