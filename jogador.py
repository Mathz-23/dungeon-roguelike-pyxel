import pyxel
import math


class Jogo:
    def __init__(self):
        self.bola = Personagem(5, 250, 6, 3)
       
        
    def update(self):
        self.bola.update()
        
    def draw(self):
        pyxel.cls(0)
        self.bola.draw()
        

        
class Personagem:
    def __init__(self, x, y, raio, cor):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.velocidade_base = 1.75
        self.velocidade_dash = 6

        self.vida_max = 100
        self.vida = self.vida_max
        self.dano = 10
        self.defesa = 0
        
        self.upgrades = {
            "espada": 0,
            "armadura": 0,
            "vida_extra": 0,
            "bota_celeridade": 0,
            "passo_sombrio": False,
            "aura_espinhos": 0
        }
        
        self.cooldown_dano = 0
        
        self.inventario = []

        self.dash = Dash()
        
    
    def receber_dano(self, dano, inimigo=None):
        # dash
        if self.dash.invencivel:
            return

        if self.dash.reducao_dano:
            dano *= 0.15
            dano = int(dano)
        
        self.vida -= dano
        
        self.cooldown_dano = 10


        # aura de espinhos
        if self.upgrades["aura_espinhos"] and inimigo:

            dano_refletido = int(dano * 0.2)

            inimigo.receber_dano(dano_refletido)
    
    
    def pegar_upgrade(self, upgrade):

        self.inventario.append(upgrade)

        upgrade.efeito(self)
                

    def update(self):
        #dano
        if self.cooldown_dano > 0:
            self.cooldown_dano -= 1
        
        
        # morte
        if self.vida <= 0:
            pyxel.quit()
        self.dx = 0
        self.dy = 0

        if pyxel.btn(pyxel.KEY_RIGHT):
            self.dx += 1

        if pyxel.btn(pyxel.KEY_LEFT):
            self.dx -= 1

        if pyxel.btn(pyxel.KEY_DOWN):
            self.dy += 1

        if pyxel.btn(pyxel.KEY_UP):
            self.dy -= 1


        if pyxel.btn(pyxel.KEY_SHIFT) and (self.dx != 0 or self.dy != 0):
            
            self.dash.usar(
                self.upgrades["passo_sombrio"]
            )


        self.dash.update()


        velocidade = self.velocidade_base

        if self.dash.ativo:
            velocidade = self.velocidade_dash
            
          
        # Hipotenusa  
        distancia = math.sqrt(self.dx**2 + self.dy**2)

        if distancia != 0:
            self.dx /= distancia
            self.dy /= distancia   
      
            
        self.x += self.dx * velocidade
        self.y += self.dy * velocidade
            
       
        # Colisão Tekla
        if self.x - self.raio < 0:
            self.x = self.raio
        if self.x + self.raio > 255:
            self.x = 255 - self.raio
        if self.y - self.raio < 0:
            self.y = self.raio
        if self.y + self.raio > 255:
            self.y = 255 - self.raio
                
    def draw(self):
        # bola
        cor_atual = self.cor

        # passo sombrio
        if self.upgrades["passo_sombrio"] and self.dash.ativo:
            cor_atual = 0


        if self.cooldown_dano > 0 and not self.upgrades["passo_sombrio"]:
            cor_atual = 13

        if self.dash.reducao_dano and not self.upgrades["passo_sombrio"]:
            cor_atual = 10
                


        pyxel.circ(
            self.x,
            self.y,
            self.raio,
            cor_atual
        )


        # espada
        if self.upgrades["espada"]:

            pyxel.rect(
                self.x + 7,
                self.y - 15,
                3,
                20,
                2
            )


        # armadura
        if self.upgrades["armadura"]:

            pyxel.circb(
                self.x,
                self.y,
                self.raio + 2,
                10
            )
            
            
        # aura de espinhos
        if self.upgrades["aura_espinhos"]:

            pyxel.circb(
                self.x,
                self.y,
                self.raio + 4,
                8
            )
        
        
        
        # barra de vida
        pyxel.rect(
            self.x - 15,
            self.y + 8,
            30,
            5,
            8
        )


        progresso = self.vida / self.vida_max


        pyxel.rect(
            self.x - 15,
            self.y + 8,
            30 * progresso,
            5,
            11
)
        
        pyxel.text(
            self.x - 12,
            self.y + 8,
            str(self.vida) + "/" + str(self.vida_max),
            7
        )
        # dash
        self.dash.draw_barra(self.x, self.y)
        
        

class Dash:
    def __init__(self):

        self.ativo = False
        
        self.timer = 0
        self.duracao = 10
        
        self.cooldown = 0
        self.cooldown_max = 40
        
        self.reducao_dano = False
        self.invencivel = False


    def usar(self, passo_sombrio=False):

        if self.cooldown <= 0:

            self.ativo = True
            self.timer = self.duracao

            self.reducao_dano = True

            if passo_sombrio:
                self.invencivel = True

            self.cooldown = self.cooldown_max


    def update(self):

        if self.cooldown > 0:
            self.cooldown -= 1

        if self.ativo:
            self.timer -= 1

            if self.timer <= 0:
                self.ativo = False
                self.reducao_dano = False
                self.invencivel = False                    
 

    def draw_barra(self, x, y):
        if self.cooldown > 0:
         
            largura = 6
            altura = 5

            progresso = 1 - (self.cooldown / self.cooldown_max)

            pyxel.rect(x - largura//2 -10,y + 15,largura, altura,1)

            pyxel.rect(x - largura//2 -10, y + 15, largura * progresso, altura, 10)
        return