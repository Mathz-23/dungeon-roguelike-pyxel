class Upgrade:

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao



class Espada(Upgrade):

    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1

        super().__init__(
            "Espada" if nivel_atual == 0 else "Melhorar Espada",
            "Espada com 5 de dano"
            if nivel_atual == 0
            else "Aumenta o dano em 2"
        )


    def efeito(self, jogador):
        limite = 25 if getattr(jogador, "modo_infinito", False) else 15
        if jogador.upgrades["espada"] == 0 or jogador.upgrades["espada"] >= limite:
            return

        aumento = min(2, limite - jogador.upgrades["espada"])
        jogador.upgrades["espada"] += aumento

        if jogador.arma_equipada == "espada":
            jogador.dano = jogador.upgrades["espada"]


class EspadaoDano(Upgrade):
    def __init__(self, dano_atual):
        novo_dano = dano_atual + 4
        self.nivel = 2 + (dano_atual - 10) // 4

        super().__init__(
            "Melhorar dano do Espadao",
            "Aumenta o dano para " + str(novo_dano),
        )

    def efeito(self, jogador):
        dano_atual = jogador.upgrades["espadao_dano"]
        limite = 30 if getattr(jogador, "modo_infinito", False) else 18
        jogador.upgrades["espadao_dano"] = min(dano_atual + 4, limite)

        if jogador.arma_equipada == "espadao":
            jogador.dano = jogador.upgrades["espadao_dano"]


class EspadaoCooldown(Upgrade):
    def __init__(self, cooldown_atual):
        novo_cooldown = (cooldown_atual - 7.5) / 30
        self.nivel = 2 + int((90 - cooldown_atual) / 7.5)

        super().__init__(
            "Melhorar recarga do Espadao",
            "Diminui a recarga para " + str(novo_cooldown) + " segundos",
        )

    def efeito(self, jogador):
        cooldown_atual = jogador.upgrades["espadao_cooldown"]
        limite = 60 if getattr(jogador, "modo_infinito", False) else 75
        jogador.upgrades["espadao_cooldown"] = max(
            limite, cooldown_atual - 7.5
        )

        if jogador.arma_equipada == "espadao":
            jogador.cooldown_ataque_max = jogador.upgrades["espadao_cooldown"]


class ManoplaDano(Upgrade):
    def __init__(self, dano_atual):
        novo_dano = dano_atual + 1
        self.nivel = novo_dano - 1

        super().__init__(
            "Melhorar dano da Manopla",
            "Aumenta o dano para " + str(novo_dano),
        )

    def efeito(self, jogador):
        limite = 10 if getattr(jogador, "modo_infinito", False) else 5
        if jogador.upgrades["manopla_dano"] >= limite:
            return

        jogador.upgrades["manopla_dano"] += 1
        if jogador.arma_equipada == "manopla":
            jogador.dano = jogador.upgrades["manopla_dano"]


class ManoplaCooldown(Upgrade):
    def __init__(self, cooldown_atual):
        novo_cooldown = (cooldown_atual - 7.5) / 30
        self.nivel = 2 + int((30 - cooldown_atual) / 7.5)

        super().__init__(
            "Melhorar recarga da Manopla",
            "Diminui a recarga para " + str(novo_cooldown) + " segundos",
        )

    def efeito(self, jogador):
        cooldown_atual = jogador.upgrades["manopla_cooldown"]
        limite = 7.5 if getattr(jogador, "modo_infinito", False) else 15
        jogador.upgrades["manopla_cooldown"] = max(
            limite, cooldown_atual - 7.5
        )

        if jogador.arma_equipada == "manopla":
            jogador.cooldown_ataque_max = jogador.upgrades["manopla_cooldown"]


class ArmaduraRD(Upgrade):
    def __init__(self, reducao_atual):
        nova_reducao = reducao_atual + 3
        self.nivel = 2 + max(0, (reducao_atual - 4) // 3)

        super().__init__(
            "Melhorar reducao da Armadura",
            "Aumenta a reducao de dano para " + str(nova_reducao),
        )

    def efeito(self, jogador):
        limite = 20 if getattr(jogador, "modo_infinito", False) else 10
        jogador.upgrades["armadura"] = min(
            jogador.upgrades["armadura"] + 3, limite
        )

        if jogador.durabilidade_armadura > 0:
            jogador.defesa = jogador.upgrades["armadura"]


class ArmaduraDurabilidade(Upgrade):
    def __init__(self, durabilidade_max):
        nova_durabilidade = durabilidade_max + 10
        self.nivel = 2 + (durabilidade_max - 10) // 10

        super().__init__(
            "Melhorar durabilidade",
            "Aumenta e restaura a durabilidade para " + str(nova_durabilidade),
        )

    def efeito(self, jogador):
        limite = 60 if getattr(jogador, "modo_infinito", False) else 30
        if jogador.durabilidade_armadura_max >= limite:
            return

        jogador.durabilidade_armadura_max += 10
        jogador.durabilidade_armadura = jogador.durabilidade_armadura_max
        jogador.defesa = jogador.upgrades["armadura"]


class VidaExtra(Upgrade):

    def __init__(self):

        super().__init__(
            "Vida Extra",
            "Aumenta vida em 25"
        )


    def efeito(self, jogador):

        jogador.vida += 25
        jogador.vida_max += 25
        

class BotaCeleridade(Upgrade):
    
    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1
        
        super().__init__(
        "Bota de Celeridade",
        "Aumenta a velocidade de movimento"
    )
        
    def efeito(self, jogador):
        limite = 4 if getattr(jogador, "modo_infinito", False) else 2.5
        if jogador.upgrades["bota_celeridade"] >= limite:
            return

        jogador.velocidade_base += 0.5
        jogador.upgrades["bota_celeridade"] += 0.5
        
        
class PassoSombrio(Upgrade):

    def __init__(self):

        super().__init__(
            "Passo Sombrio",
            "Melhora a invencibilidade do dash"
        )


    def efeito(self, jogador):

        jogador.dash.duracao += 3
        jogador.upgrades["passo_sombrio"] = True
        

class AuraEspinhos(Upgrade):

    def __init__(self, porcentagem_atual=0):

        nova_porcentagem = 20 if porcentagem_atual == 0 else porcentagem_atual + 10
        self.nivel = nova_porcentagem // 10 - 1

        super().__init__(
            "Aura de Espinhos"
            if porcentagem_atual == 0
            else "Melhorar Aura de Espinhos",
            "Reflete " + str(nova_porcentagem) + "% do dano recebido"
        )


    def efeito(self, jogador):
        limite = 80 if getattr(jogador, "modo_infinito", False) else 50
        if jogador.upgrades["aura_espinhos"] == 0:
            jogador.upgrades["aura_espinhos"] = 20
        else:
            jogador.upgrades["aura_espinhos"] = min(
                limite,
                jogador.upgrades["aura_espinhos"] + 10
            )
        
    

class CuraContinua(Upgrade):

    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1

        super().__init__(
            "Cura Continua"
            if nivel_atual == 0
            else "Melhorar Cura Continua",
            "Regenera " + str(self.nivel) + " de vida a cada 3 segundos"
        )


    def efeito(self, jogador):
        limite = 10 if getattr(jogador, "modo_infinito", False) else 5
        jogador.upgrades["cura_continua"] = min(
            limite, jogador.upgrades["cura_continua"] + 1
        )
        jogador.timer_cura = 0
