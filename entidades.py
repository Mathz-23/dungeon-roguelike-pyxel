class Entidade:
    def __init__(self, x, y, raio, vida, dano):
        self.x = x
        self.y = y
        self.raio = raio

        self.vida = vida
        self.vida_max = vida

        # dano causado
        self.dano = dano
        self.cooldown_ataque = 0

        # dano recebido
        self.cooldown_receber_dano = 0

        # visual do dano
        self.ultimo_dano = 0
        self.tempo_exibir_dano = 0


    def receber_dano(self, dano):

        # ainda está invulnerável após o último golpe
        if self.cooldown_receber_dano > 0:
            return False

        self.vida -= dano

        self.ultimo_dano = dano
        self.tempo_exibir_dano = 20

        # frames de invulnerabilidade
        self.cooldown_receber_dano = 10

        return True


    def atualizar_temporizadores(self):

        if self.cooldown_ataque > 0:
            self.cooldown_ataque -= 1

        if self.cooldown_receber_dano > 0:
            self.cooldown_receber_dano -= 1

        if self.tempo_exibir_dano > 0:
            self.tempo_exibir_dano -= 1


    def esta_vivo(self):
        return self.vida > 0