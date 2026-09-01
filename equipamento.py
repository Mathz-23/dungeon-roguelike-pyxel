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

        self.dano = 10


class Armadura(Upgrade):

    def __init__(self):
        super().__init__(
            "Armadura",
            "Aumenta a defesa em 5"
        )

        self.defesa = 5


class VidaExtra(Upgrade):

    def __init__(self):
        super().__init__(
            "Vida Extra",
            "Aumenta a vida em 20"
        )

        self.vida = 20