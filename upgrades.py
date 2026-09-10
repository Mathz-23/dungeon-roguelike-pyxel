class Upgrade:

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao



class Espada(Upgrade):

    def __init__(self):

        super().__init__(
            "Espada",
            "Aumenta o dano em 5"
        )


    def efeito(self, jogador):

        jogador.dano += 5
        jogador.upgrades["espada"] += 5



class Armadura(Upgrade):

    def __init__(self):

        super().__init__(
            "Armadura",
            "Aumenta defesa em 4"
        )


    def efeito(self, jogador):

        jogador.defesa += 4
        jogador.upgrades["armadura"] += 4



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
    
    def __init__(self):
        
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

    def __init__(self):

        super().__init__(
            "Aura de Espinhos",
            "Reflete 20% do dano recebido"
        )


    def efeito(self, jogador):

        jogador.upgrades["aura_espinhos"] = True
        
    

class CuraContinua(Upgrade):

    def __init__(self):

        super().__init__(
            "Cura Contínua",
            "Regenera 1 de vida a cada 2 segundos"
        )


    def efeito(self, jogador):
        if jogador.vida < jogador.vida_max:
            jogador.vida += 1
        jogador.upgrades["cura_continua"] = True