import random


class Espada:
    def __init__(self):
        self.nome = "Espada"
        self.tipo = "espada"

    def pegar(self, jogador):
        if jogador.upgrades["espada"] > 0:
            return False

        jogador.inventario.append(self)
        jogador.upgrades["espada"] = 5
        jogador.arma_equipada = "espada"
        jogador.dano = 5
        jogador.cooldown_ataque_max = 52.5
        return True


class Espadao:
    def __init__(self):
        self.nome = "Espadao"
        self.tipo = "espadao"

    def pegar(self, jogador):
        if jogador.upgrades["espadao_dano"] > 0:
            return False

        jogador.inventario.append(self)
        jogador.upgrades["espadao_dano"] = 10
        jogador.upgrades["espadao_cooldown"] = 90
        jogador.arma_equipada = "espadao"
        jogador.dano = 10
        jogador.cooldown_ataque_max = 90
        return True


class Armadura:
    def __init__(self):
        self.nome = "Armadura"
        self.tipo = "armadura"

    def pegar(self, jogador):
        if jogador.upgrades["armadura"] > 0:
            jogador.durabilidade_armadura = jogador.durabilidade_armadura_max
            jogador.defesa = jogador.upgrades["armadura"]
            self.mensagem = "Voce trocou sua armadura por uma melhor"
            return True

        jogador.inventario.append(self)
        jogador.upgrades["armadura"] = 4
        jogador.defesa = 4
        jogador.durabilidade_armadura_max = 10
        jogador.durabilidade_armadura = 10
        self.mensagem = "Voce encontrou: Armadura"
        return True


class Manopla:
    def __init__(self):
        self.nome = "Manopla"
        self.tipo = "manopla"

    def pegar(self, jogador):
        if jogador.upgrades["manopla_dano"] > 0:
            return False

        jogador.inventario.append(self)
        jogador.upgrades["manopla_dano"] = 2
        jogador.upgrades["manopla_cooldown"] = 30
        jogador.arma_equipada = "manopla"
        jogador.dano = 2
        jogador.cooldown_ataque_max = 30
        return True


def sortear_item(jogador):
    itens_disponiveis = [Armadura]

    if jogador.upgrades["espada"] == 0:
        itens_disponiveis.append(Espada)
    if jogador.upgrades["espadao_dano"] == 0:
        itens_disponiveis.append(Espadao)
    if jogador.upgrades["manopla_dano"] == 0:
        itens_disponiveis.append(Manopla)

    item_sorteado = random.choice(itens_disponiveis)
    return item_sorteado()
