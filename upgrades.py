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
        jogador.tem_espada = True



class Armadura(Upgrade):

    def __init__(self):

        super().__init__(
            "Armadura",
            "Aumenta defesa em 7"
        )


    def efeito(self, jogador):

        jogador.defesa += 6
        jogador.tem_armadura = True



class VidaExtra(Upgrade):

    def __init__(self):

        super().__init__(
            "Vida Extra",
            "Aumenta vida em 25"
        )


    def efeito(self, jogador):

        jogador.vida += 25
        

class BotaCeleridade(Upgrade):
    
    def __init__(self):
        
        super().__init__(
        "Bota de Celeridade",
        "Aumenta a velocidade de movimento em 1"
    )
        
    def efeito(self, jogador):
        jogador.velocidade_base += 1.25
