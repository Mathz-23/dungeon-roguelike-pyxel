import pyxel
import math


class Inimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.raio = 5
        self.cor = 4

        self.vida = 30
        self.velocidade = 1
        self.dano = 15
        self.cooldown_atq =  0
        
        
    def atacar(self, jogador):

        if self.cooldown_atq > 0:
            self.cooldown_atq -= 1
            return


        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia = math.sqrt(dx**2 + dy**2)

        distancia_minima = self.raio + jogador.raio + 3


        if distancia < distancia_minima:

            dano_real = max(0, self.dano - jogador.defesa)

            if not jogador.dash.iframe:

                jogador.receber_dano(dano_real)

                self.cooldown_atq = 60  
            
        
    def seguir(self, jogador):

        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia = math.sqrt(dx**2 + dy**2)

        distancia_minima = self.raio + jogador.raio + 3


        if distancia > distancia_minima:

            dx /= distancia
            dy /= distancia

            self.x += dx * self.velocidade
            self.y += dy * self.velocidade
        
    def separar(self, inimigos):

        for outro in inimigos:

            if outro == self:
                continue

            dx = self.x - outro.x
            dy = self.y - outro.y

            distancia = math.sqrt(dx**2 + dy**2)

            distancia_minima = self.raio * 2 + 2


            if distancia < distancia_minima and distancia != 0:

                dx /= distancia
                dy /= distancia

                self.x += dx
                self.y += dy
        

    def update(self, jogador, inimigos):
        
        self.atacar(jogador)

        self.seguir(jogador)

        self.separar(inimigos)

    def draw(self):
        pyxel.circ(self.x, self.y, self.raio, self.cor)
        pyxel.text(self.x - 10, self.y - 10, f"HP: {self.vida}", 7)  
