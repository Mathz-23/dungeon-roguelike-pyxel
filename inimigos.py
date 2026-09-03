import pyxel
import math
from entidades import Entidade
from colisao import distancia, colidiu


class Inimigo(Entidade):
    def __init__(self, x, y):
        super().__init__(x, y, 5, 7)
        self.cor = 4

        self.velocidade = 1
        self.dano = 20
        self.cooldown_atq =  0
        
        
    def atacar(self, jogador):

        if self.cooldown_atq > 0:
            self.cooldown_atq -= 1
            return

        if colidiu(self, jogador, 3):

            dano_real = max(0, self.dano - jogador.defesa)

            if not jogador.dash.invencivel:

                jogador.receber_dano(dano_real, self)

                self.cooldown_atq = 60
            
      
        
    def seguir(self, jogador):

        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia_atual = distancia(self, jogador)

        if not colidiu(self, jogador, 3):

            dx /= distancia_atual
            dy /= distancia_atual

            self.x += dx * self.velocidade
            self.y += dy * self.velocidade
        
    def separar(self, inimigos):

        for outro in inimigos:

            if outro == self:
                continue

            if colidiu(self, outro, 2):

                dx = self.x - outro.x
                dy = self.y - outro.y

                distancia_atual = distancia(self, outro)

                if distancia_atual != 0:

                    dx /= distancia_atual
                    dy /= distancia_atual

                    self.x += dx
                    self.y += dy
        

    def update(self, jogador, inimigos):
        
        if self.tempo_dano > 0:
            self.tempo_dano -= 1
        
        self.atacar(jogador)

        self.seguir(jogador)

        self.separar(inimigos)

    def draw(self):
        pyxel.circ(self.x, self.y, self.raio, self.cor)

        pyxel.text(
            self.x - 10,
            self.y - 10,
            f"HP: {int(self.vida)}",
            10
        )

        if self.tempo_dano > 0:

            pyxel.text(
                self.x - 10,
                self.y - 20,
                f"-{int(self.ultimo_dano)}",
                7
            )


