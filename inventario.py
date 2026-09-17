import random

from upgrades import Espada, Armadura, VidaExtra, BotaCeleridade, PassoSombrio, AuraEspinhos, CuraContinua


upgrades = [
    Espada,
    Armadura,
    VidaExtra,
    BotaCeleridade,
    PassoSombrio,
    AuraEspinhos,
    CuraContinua
]


def sortear_upgrades():

    escolhas = random.sample(upgrades, 2)

    return [
        escolha()
        for escolha in escolhas
    ]