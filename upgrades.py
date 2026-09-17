class Upgrade:

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao



class Manopla(Upgrade):

    def __init__(self):
        super().__init__(
            "Manopla",
            "Socos com mais dano e menor recarga"
        )

    def efeito(self, jogador):

        if jogador.arma["tipo"] != "soco":
            return

        jogador.equipar_ou_melhorar_arma("manopla")


class Espada(Upgrade):

    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1

        super().__init__(
            "Espada" if nivel_atual == 0 else "Melhorar Espada",
            "Dano 8 e recarga de 1s"
            if nivel_atual == 0
            else "Melhora a espada: +2 de dano"
        )

    def efeito(self, jogador):

        jogador.equipar_ou_melhorar_arma("espada")



class EspadaGrande(Upgrade):

    def __init__(self, nivel_atual=0):

        self.nivel = nivel_atual + 1

        super().__init__(
            "Espada Grande"
            if nivel_atual == 0
            else "Melhorar Espada Grande",

            "Corte em area, dano minimo 8 e recarga de 3s"
            if nivel_atual == 0
            else "Melhora a espada grande: +2 de dano"
        )

    def efeito(self, jogador):

        jogador.equipar_ou_melhorar_arma("espada_grande")


class Armadura(Upgrade):

    def __init__(self):

        super().__init__(
            "Armadura",
            "Aumenta defesa em 4"
        )


    def efeito(self, jogador):

        if jogador.upgrades["armadura"]:
            return

        jogador.defesa += 4
        jogador.upgrades["armadura"] = True



class VidaExtra(Upgrade):

    def __init__(self):

        super().__init__(
            "Vida Extra",
            "Aumenta vida em 20"
        )


    def efeito(self, jogador):

        jogador.vida += 20
        jogador.vida_max += 20
        jogador.upgrades["vida_extra"] += 20
        

class BotaCeleridade(Upgrade):
    
    def __init__(self):
        
        super().__init__(
        "Bota de Celeridade",
        "Aumenta a velocidade de movimento e diminui o tempo de recarga do dash"
    )
        
    def efeito(self, jogador):
        jogador.velocidade_base += 0.5
        jogador.upgrades["bota_celeridade"] += 0.5
        jogador.dash.cooldown_max = max(10, jogador.dash.cooldown_max - 15)
        
        
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

    def __init__(self):

        super().__init__(
            "Aura de Espinhos",
            "Reflete 20% do dano recebido (minimo 1)"
        )


    def efeito(self, jogador):

        jogador.upgrades["aura_espinhos"] = True
        
    

class CuraContinua(Upgrade):

    def __init__(self, nivel_atual=0):
        self.nivel = nivel_atual + 1
        self.bonus_melhoria = "+1 por cura"
        super().__init__(
            "Cura Continua" if nivel_atual == 0 else "Melhorar Cura Continua",
            f"Regenera {self.nivel} de vida a cada 3 segundos"
        )


    def efeito(self, jogador):
        jogador.upgrades["cura_continua"] += 1
        jogador.timer_cura = 0
