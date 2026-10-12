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
        modo_infinito = getattr(jogador, "modo_infinito", False)
        limite_aura = 80 if modo_infinito else 50
        limite_cura = 10 if modo_infinito else 5
        limite_espada = 25 if modo_infinito else 15
        limite_espadao_dano = 30 if modo_infinito else 18
        limite_espadao_cooldown = 60 if modo_infinito else 75
        limite_manopla_dano = 10 if modo_infinito else 5
        limite_manopla_cooldown = 7.5 if modo_infinito else 15
        limite_armadura = 20 if modo_infinito else 10
        limite_durabilidade = 60 if modo_infinito else 30
        limite_bota = 4 if modo_infinito else 2.5

        if jogador.upgrades["aura_espinhos"] >= limite_aura:
            disponiveis.remove(AuraEspinhos)

        if jogador.upgrades["passo_sombrio"]:
            disponiveis.remove(PassoSombrio)

        if jogador.upgrades["cura_continua"] >= limite_cura:
            disponiveis.remove(CuraContinua)

        if jogador.upgrades["bota_celeridade"] >= limite_bota:
            disponiveis.remove(BotaCeleridade)

        if (
            jogador.upgrades["espada"] == 0
            or jogador.upgrades["espada"] >= limite_espada
        ):
            disponiveis.remove(Espada)

        if jogador.upgrades["espadao_dano"] == 0:
            disponiveis.remove(EspadaoDano)
            disponiveis.remove(EspadaoCooldown)
        else:
            if jogador.upgrades["espadao_dano"] >= limite_espadao_dano:
                disponiveis.remove(EspadaoDano)
            if jogador.upgrades["espadao_cooldown"] <= limite_espadao_cooldown:
                disponiveis.remove(EspadaoCooldown)

        if jogador.upgrades["manopla_dano"] == 0:
            disponiveis.remove(ManoplaDano)
            disponiveis.remove(ManoplaCooldown)
        else:
            if jogador.upgrades["manopla_dano"] >= limite_manopla_dano:
                disponiveis.remove(ManoplaDano)
            if jogador.upgrades["manopla_cooldown"] <= limite_manopla_cooldown:
                disponiveis.remove(ManoplaCooldown)

        if jogador.upgrades["armadura"] == 0:
            disponiveis.remove(ArmaduraRD)
            disponiveis.remove(ArmaduraDurabilidade)
        else:
            if jogador.upgrades["armadura"] >= limite_armadura:
                disponiveis.remove(ArmaduraRD)
            if jogador.durabilidade_armadura_max >= limite_durabilidade:
                disponiveis.remove(ArmaduraDurabilidade)

    quantidade = min(2, len(disponiveis))
    escolhas = random.sample(disponiveis, quantidade)

    opcoes = []

    for escolha in escolhas:
        if jogador is not None and escolha is Espada:
            bonus_atual = jogador.upgrades["espada"]
            if bonus_atual == 0:
                nivel_atual = 0
            else:
                nivel_atual = 1 + (bonus_atual - 5) // 2
            upgrade = Espada(nivel_atual)
            novo_valor = min(bonus_atual + 2, limite_espada)
            upgrade.indicador_melhoria = (
                str(bonus_atual) + " --> " + str(novo_valor) + " de dano"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is CuraContinua:
            nivel_atual = jogador.upgrades["cura_continua"]
            upgrade = CuraContinua(nivel_atual)
            upgrade.indicador_melhoria = (
                str(nivel_atual) + " --> " + str(nivel_atual + 1) + " por cura"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is BotaCeleridade:
            nivel_atual = int(jogador.upgrades["bota_celeridade"] / 0.5)
            upgrade = BotaCeleridade(nivel_atual)
            velocidade_atual = jogador.velocidade_base
            upgrade.indicador_melhoria = (
                str(velocidade_atual)
                + " --> "
                + str(velocidade_atual + 0.5)
                + " velocidade"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is AuraEspinhos:
            porcentagem_atual = jogador.upgrades["aura_espinhos"]
            upgrade = AuraEspinhos(porcentagem_atual)
            nova_porcentagem = 20 if porcentagem_atual == 0 else porcentagem_atual + 10
            upgrade.indicador_melhoria = (
                str(porcentagem_atual) + "% --> " + str(nova_porcentagem) + "%"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is EspadaoDano:
            dano_atual = jogador.upgrades["espadao_dano"]
            upgrade = EspadaoDano(dano_atual)
            novo_dano = min(dano_atual + 4, limite_espadao_dano)
            upgrade.descricao = "Aumenta o dano do Espadao"
            upgrade.indicador_melhoria = (
                str(dano_atual) + " --> " + str(novo_dano) + " de dano"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is EspadaoCooldown:
            cooldown_atual = jogador.upgrades["espadao_cooldown"]
            upgrade = EspadaoCooldown(cooldown_atual)
            novo_cooldown = max(limite_espadao_cooldown, cooldown_atual - 7.5)
            upgrade.descricao = "Diminui a recarga do Espadao"
            upgrade.indicador_melhoria = (
                str(cooldown_atual / 30)
                + "s --> "
                + str(novo_cooldown / 30)
                + "s"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is ManoplaDano:
            dano_atual = jogador.upgrades["manopla_dano"]
            upgrade = ManoplaDano(dano_atual)
            novo_dano = min(dano_atual + 1, limite_manopla_dano)
            upgrade.descricao = "Aumenta o dano da Manopla"
            upgrade.indicador_melhoria = (
                str(dano_atual) + " --> " + str(novo_dano) + " de dano"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is ManoplaCooldown:
            cooldown_atual = jogador.upgrades["manopla_cooldown"]
            upgrade = ManoplaCooldown(cooldown_atual)
            novo_cooldown = max(limite_manopla_cooldown, cooldown_atual - 7.5)
            upgrade.descricao = "Diminui a recarga da Manopla"
            upgrade.indicador_melhoria = (
                str(cooldown_atual / 30)
                + "s --> "
                + str(novo_cooldown / 30)
                + "s"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is ArmaduraRD:
            reducao_atual = jogador.upgrades["armadura"]
            upgrade = ArmaduraRD(reducao_atual)
            nova_reducao = min(reducao_atual + 3, limite_armadura)
            upgrade.descricao = "Aumenta a reducao de dano"
            upgrade.indicador_melhoria = (
                str(reducao_atual) + " --> " + str(nova_reducao) + " de RD"
            )
            opcoes.append(upgrade)

        elif jogador is not None and escolha is ArmaduraDurabilidade:
            atual = jogador.durabilidade_armadura_max
            upgrade = ArmaduraDurabilidade(atual)
            nova_durabilidade = min(atual + 10, limite_durabilidade)
            upgrade.descricao = "Aumenta e restaura a durabilidade"
            upgrade.indicador_melhoria = (
                str(atual) + " --> " + str(nova_durabilidade)
            )
            opcoes.append(upgrade)

        else:
            upgrade = escolha()
            if escolha is VidaExtra:
                upgrade.indicador_melhoria = "+25 de vida maxima"
            elif escolha is PassoSombrio:
                upgrade.indicador_melhoria = "Reducao --> Invencivel"
            opcoes.append(upgrade)

    return opcoes
