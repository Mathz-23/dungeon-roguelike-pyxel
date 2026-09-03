import pyxel
import math


class Inimigo:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.raio = 5
        self.cor = 4

        self.vida = 7
        self.velocidade = 1
        self.dano = 20
        self.cooldown_atq =  0
        
        self.ultimo_dano = 0
        self.tempo_dano = 0
        
        
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

            if not jogador.dash.invencivel:

                jogador.receber_dano(dano_real, self)

                self.cooldown_atq = 60  
            
     
     
    def receber_dano(self, dano):

        self.vida -= dano 
      
        self.ultimo_dano = dano
        self.tempo_dano = 20
        
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
            7
        )

        if self.tempo_dano > 0:

            pyxel.text(
                self.x - 10,
                self.y - 20,
                f"-{int(self.ultimo_dano)}",
                8
            )


