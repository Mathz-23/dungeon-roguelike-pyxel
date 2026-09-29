import random

from upgrades import (
    Espada,
    EspadaoDano,
    EspadaoCooldown,
    ManoplaDano,
    ManoplaCooldown,
    ArmaduraRD,
    ArmaduraDurabilidade,
    VidaExtra,
    BotaCeleridade,
    PassoSombrio,
    AuraEspinhos,
    CuraContinua,
)


upgrades = [
    Espada,
    EspadaoDano,
    EspadaoCooldown,
    ManoplaDano,
    ManoplaCooldown,
    ArmaduraRD,
    ArmaduraDurabilidade,
    VidaExtra,
    BotaCeleridade,
    PassoSombrio,
    AuraEspinhos,
    CuraContinua
]


def sortear_upgrades(jogador=None):

    disponiveis = list(upgrades)

    if jogador is not None:
        if jogador.upgrades["aura_espinhos"] >= 50:
            disponiveis.remove(AuraEspinhos)

        if jogador.upgrades["passo_sombrio"]:
            disponiveis.remove(PassoSombrio)

        if jogador.upgrades["cura_continua"] >= 5:
            disponiveis.remove(CuraContinua)

        if jogador.upgrades["espada"] == 0 or jogador.upgrades["espada"] >= 15:
            disponiveis.remove(Espada)

        if jogador.upgrades["espadao_dano"] == 0:
            disponiveis.remove(EspadaoDano)
            disponiveis.remove(EspadaoCooldown)
        else:
            if jogador.upgrades["espadao_dano"] >= 18:
                disponiveis.remove(EspadaoDano)
            if jogador.upgrades["espadao_cooldown"] <= 75:
                disponiveis.remove(EspadaoCooldown)

        if jogador.upgrades["manopla_dano"] == 0:
            disponiveis.remove(ManoplaDano)
            disponiveis.remove(ManoplaCooldown)
        else:
            if jogador.upgrades["manopla_dano"] >= 5:
                disponiveis.remove(ManoplaDano)
            if jogador.upgrades["manopla_cooldown"] <= 15:
                disponiveis.remove(ManoplaCooldown)

        if jogador.upgrades["armadura"] == 0:
            disponiveis.remove(ArmaduraRD)
            disponiveis.remove(ArmaduraDurabilidade)
        else:
            if jogador.upgrades["armadura"] >= 10:
                disponiveis.remove(ArmaduraRD)
            if jogador.durabilidade_armadura_max >= 30:
                disponiveis.remove(ArmaduraDurabilidade)

    escolhas = random.sample(disponiveis, 2)

    opcoes = []

    for escolha in escolhas:
        if jogador is not None and escolha is Espada:
            bonus_atual = jogador.upgrades["espada"]
            if bonus_atual == 0:
                nivel_atual = 0
            else:
                nivel_atual = 1 + (bonus_atual - 5) // 2
            opcoes.append(Espada(nivel_atual))

        elif jogador is not None and escolha is CuraContinua:
            nivel_atual = jogador.upgrades["cura_continua"]
            opcoes.append(CuraContinua(nivel_atual))

        elif jogador is not None and escolha is BotaCeleridade:
            nivel_atual = int(jogador.upgrades["bota_celeridade"] / 0.5)
            opcoes.append(BotaCeleridade(nivel_atual))

        elif jogador is not None and escolha is AuraEspinhos:
            porcentagem_atual = jogador.upgrades["aura_espinhos"]
            opcoes.append(AuraEspinhos(porcentagem_atual))

        elif jogador is not None and escolha is EspadaoDano:
            dano_atual = jogador.upgrades["espadao_dano"]
            opcoes.append(EspadaoDano(dano_atual))

        elif jogador is not None and escolha is EspadaoCooldown:
            cooldown_atual = jogador.upgrades["espadao_cooldown"]
            opcoes.append(EspadaoCooldown(cooldown_atual))

        elif jogador is not None and escolha is ManoplaDano:
            dano_atual = jogador.upgrades["manopla_dano"]
            opcoes.append(ManoplaDano(dano_atual))

        elif jogador is not None and escolha is ManoplaCooldown:
            cooldown_atual = jogador.upgrades["manopla_cooldown"]
            opcoes.append(ManoplaCooldown(cooldown_atual))

        elif jogador is not None and escolha is ArmaduraRD:
            reducao_atual = jogador.upgrades["armadura"]
            opcoes.append(ArmaduraRD(reducao_atual))

        elif jogador is not None and escolha is ArmaduraDurabilidade:
            opcoes.append(
                ArmaduraDurabilidade(jogador.durabilidade_armadura_max)
            )

        else:
            opcoes.append(escolha())

    return opcoes
