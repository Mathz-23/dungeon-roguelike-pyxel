class Upgrade:

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao



class Espada(Upgrade):

    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1
        self.bonus_melhoria = "+2 de dano"

        super().__init__(
            "Espada" if nivel_atual == 0 else "Melhorar Espada",
            "Espada com 5 de dano"
            if nivel_atual == 0
            else "Aumenta o dano em 2"
        )


    def efeito(self, jogador):

        if jogador.upgrades["espada"] == 0 or jogador.upgrades["espada"] >= 15:
            return

        aumento = min(2, 15 - jogador.upgrades["espada"])
        jogador.upgrades["espada"] += aumento

        if jogador.arma_equipada == "espada":
            jogador.dano = jogador.upgrades["espada"]


class EspadaoDano(Upgrade):
    def __init__(self, dano_atual):
        novo_dano = 14 if dano_atual == 10 else 18
        self.nivel = 2 if dano_atual == 10 else 3
        self.bonus_melhoria = "+4 de dano"

        super().__init__(
            "Melhorar dano do Espadao",
            "Aumenta o dano para " + str(novo_dano),
        )

    def efeito(self, jogador):
        dano_atual = jogador.upgrades["espadao_dano"]
        if dano_atual == 10:
            jogador.upgrades["espadao_dano"] = 14
        elif dano_atual == 14:
            jogador.upgrades["espadao_dano"] = 18

        if jogador.arma_equipada == "espadao":
            jogador.dano = jogador.upgrades["espadao_dano"]


class EspadaoCooldown(Upgrade):
    def __init__(self, cooldown_atual):
        novo_cooldown = 2.75 if cooldown_atual == 90 else 2.5
        self.nivel = 2 if cooldown_atual == 90 else 3
        self.bonus_melhoria = str(novo_cooldown) + "s de recarga"

        super().__init__(
            "Melhorar recarga do Espadao",
            "Diminui a recarga para " + str(novo_cooldown) + " segundos",
        )

    def efeito(self, jogador):
        cooldown_atual = jogador.upgrades["espadao_cooldown"]
        if cooldown_atual == 90:
            jogador.upgrades["espadao_cooldown"] = 82.5
        elif cooldown_atual == 82.5:
            jogador.upgrades["espadao_cooldown"] = 75

        if jogador.arma_equipada == "espadao":
            jogador.cooldown_ataque_max = jogador.upgrades["espadao_cooldown"]


class ManoplaDano(Upgrade):
    def __init__(self, dano_atual):
        novo_dano = dano_atual + 1
        self.nivel = novo_dano - 1
        self.bonus_melhoria = "+1 de dano"

        super().__init__(
            "Melhorar dano da Manopla",
            "Aumenta o dano para " + str(novo_dano),
        )

    def efeito(self, jogador):
        if jogador.upgrades["manopla_dano"] >= 5:
            return

        jogador.upgrades["manopla_dano"] += 1
        if jogador.arma_equipada == "manopla":
            jogador.dano = jogador.upgrades["manopla_dano"]


class ManoplaCooldown(Upgrade):
    def __init__(self, cooldown_atual):
        novo_cooldown = 0.75 if cooldown_atual == 30 else 0.5
        self.nivel = 2 if cooldown_atual == 30 else 3
        self.bonus_melhoria = str(novo_cooldown) + "s de recarga"

        super().__init__(
            "Melhorar recarga da Manopla",
            "Diminui a recarga para " + str(novo_cooldown) + " segundos",
        )

    def efeito(self, jogador):
        cooldown_atual = jogador.upgrades["manopla_cooldown"]
        if cooldown_atual == 30:
            jogador.upgrades["manopla_cooldown"] = 22.5
        elif cooldown_atual == 22.5:
            jogador.upgrades["manopla_cooldown"] = 15

        if jogador.arma_equipada == "manopla":
            jogador.cooldown_ataque_max = jogador.upgrades["manopla_cooldown"]


class ArmaduraRD(Upgrade):
    def __init__(self, reducao_atual):
        nova_reducao = 7 if reducao_atual == 4 else 10
        self.nivel = 2 if reducao_atual == 4 else 3
        self.bonus_melhoria = str(nova_reducao) + " de RD"

        super().__init__(
            "Melhorar reducao da Armadura",
            "Aumenta a reducao de dano para " + str(nova_reducao),
        )

    def efeito(self, jogador):
        if jogador.upgrades["armadura"] == 4:
            jogador.upgrades["armadura"] = 7
        elif jogador.upgrades["armadura"] == 7:
            jogador.upgrades["armadura"] = 10

        if jogador.durabilidade_armadura > 0:
            jogador.defesa = jogador.upgrades["armadura"]


class ArmaduraDurabilidade(Upgrade):
    def __init__(self, durabilidade_max):
        nova_durabilidade = durabilidade_max + 10
        self.nivel = 2 if durabilidade_max == 10 else 3
        self.bonus_melhoria = str(nova_durabilidade) + " de durabilidade"

        super().__init__(
            "Melhorar durabilidade",
            "Aumenta e restaura a durabilidade para " + str(nova_durabilidade),
        )

    def efeito(self, jogador):
        if jogador.durabilidade_armadura_max >= 30:
            return

        jogador.durabilidade_armadura_max += 10
        jogador.durabilidade_armadura = jogador.durabilidade_armadura_max
        jogador.upgrades["armadura_durabilidade"] += 1
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
        jogador.upgrades["vida_extra"] += 25
        

class BotaCeleridade(Upgrade):
    
    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1
        self.bonus_melhoria = "+0.5 velocidade"
        
        super().__init__(
        "Bota de Celeridade",
        "Aumenta a velocidade de movimento e diminui o tempo de recarga do dash"
    )
        
    def efeito(self, jogador):
        jogador.velocidade_base += 0.5
        jogador.upgrades["bota_celeridade"] += 0.5
        jogador.dash.cooldown_max -= 15
        
        
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
        self.bonus_melhoria = "+10% refletido"

        super().__init__(
            "Aura de Espinhos"
            if porcentagem_atual == 0
            else "Melhorar Aura de Espinhos",
            "Reflete " + str(nova_porcentagem) + "% do dano recebido"
        )


    def efeito(self, jogador):

        if jogador.upgrades["aura_espinhos"] == 0:
            jogador.upgrades["aura_espinhos"] = 20
        else:
            jogador.upgrades["aura_espinhos"] = min(
                50,
                jogador.upgrades["aura_espinhos"] + 10
            )
        
    

class CuraContinua(Upgrade):

    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1
        self.bonus_melhoria = "+1 por cura"

        super().__init__(
            "Cura Continua"
            if nivel_atual == 0
            else "Melhorar Cura Continua",
            "Regenera " + str(self.nivel) + " de vida a cada 3 segundos"
        )


    def efeito(self, jogador):
        jogador.upgrades["cura_continua"] += 1
        jogador.timer_cura = 0
