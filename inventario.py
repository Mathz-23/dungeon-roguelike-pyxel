import random

from upgrades import Espada, Armadura, VidaExtra, BotaCeleridade


upgrades = [
    Espada,
    Armadura,
    VidaExtra,
    BotaCeleridade
]


def sortear_upgrades():

    escolhas = random.sample(upgrades, 2)

    return [
        escolha()
        for escolha in escolhas
    ]