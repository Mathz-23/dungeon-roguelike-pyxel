class Upgrade:

    def __init__(self, nome, descricao):
        self.nome = nome
        self.descricao = descricao



class Espada(Upgrade):

    def __init__(self):

        super().__init__(
            "Espada",
            "Aumenta o dano em 10"
        )


    def efeito(self, jogador):

        jogador.dano += 10
        jogador.upgrades["espada"] += 10



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
        jogador.upgrades["vida_extra"] += 25
        

class BotaCeleridade(Upgrade):
    
    def __init__(self):
        
        super().__init__(
        "Bota de Celeridade",
        "Aumenta a velocidade de movimento em 1"
    )
        
    def efeito(self, jogador):
        jogador.velocidade_base += 0.75
        jogador.upgrades["bota_celeridade"] += 0.75
        
        
class PassoSombrio(Upgrade):

    def __init__(self):

        super().__init__(
            "Passo Sombrio",
            "Aumenta o tempo de invencibilidade do dash"
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

        jogador.upgrades["aura_espinhos"] += 20