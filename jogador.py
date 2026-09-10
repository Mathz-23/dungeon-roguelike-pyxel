import pyxel
import math
from entidades import Entidade
from colisao import colidiu, limitar_tela

        
class Personagem(Entidade):
    def __init__(self, x, y, raio, cor):
        super().__init__(x, y, raio, 50, 3)
        self.cor = cor
        self.velocidade_base = 1.5
        self.velocidade_dash = 6
        
        self.direcao_x = 1
        self.direcao_y = 0

        self.defesa = 0
        self.cooldown_ataque_max = 25
        
        self.upgrades = {
            "espada": 0,
            "armadura": 0,
            "vida_extra": 0,
            "bota_celeridade": 0,
            "passo_sombrio": False,
            "aura_espinhos": False
        }
        
        self.inventario = []

        self.dash = Dash()
    
    def hitbox_ataque(self):
        alcance = 15
        largura = 10
        
        #direita
        if self.direcao_x == 1:
            return (
                self.x + self.raio,
                self.y - largura / 2,
                alcance,
                largura
            )
            
        #esquerda
        if self.direcao_x == -1:
            return (
                self.x - self.raio - alcance,
                self.y - largura / 2,
                alcance,
                largura
            )
        
        #baixo
        if self.direcao_y == 1:
            return (
                self.x - largura / 2,
                self.y + self.raio,
                largura,
                alcance
            )
        #cima
        if self.direcao_y == -1:
            return (
                self.x - largura / 2,
                self.y - self.raio - alcance,
                largura,
                alcance
            )

    def atacar(self, inimigos):

        if self.cooldown_ataque > 0:
            return

        if pyxel.btn(pyxel.KEY_SPACE):

            for inimigo in inimigos:

                if colidiu(self, inimigo, 10):

                    dano_real = max(0, self.dano - inimigo.defesa)

                    acertou = inimigo.receber_dano(dano_real)

                    if acertou:
                        self.cooldown_ataque = self.cooldown_ataque_max

                    return
                
    def draw_barra_ataque(self):
        if self.cooldown_ataque > 0:
         
            largura = 6
            altura = 5

            progresso = 1 - (self.cooldown_ataque / self.cooldown_ataque_max)

            pyxel.rect(self.x - largura//2 +10, self.y + 15,largura, altura,1)

            pyxel.rect(self.x - largura//2 +10, self.y + 15, largura * progresso, altura, 14)
        return
    
    
    def receber_dano(self, dano, inimigo=None):
        # Passo Sombrio
        if self.dash.invencivel:
            return False

        # redução do dash
        if self.dash.reducao_dano:
            dano *= 0.3
            dano = int(dano)

        recebeu = super().receber_dano(dano)

        if not recebeu:
            return False

        # aura de espinhos
        if self.upgrades["aura_espinhos"] and inimigo:

            dano_refletido = int(dano * 0.2)

            inimigo.receber_dano(dano_refletido)

        return True
    
    
    def pegar_upgrade(self, upgrade):

        self.inventario.append(upgrade)

        upgrade.efeito(self)
                

    def update(self):
        #dano
        self.atualizar_temporizadores()
        
        
        # morte
        if self.vida <= 0:
            pyxel.quit()
        self.dx = 0
        self.dy = 0

        if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_D):
            self.dx += 1
            self.direcao_x = 1
            self.direcao_y = 0

        if pyxel.btn(pyxel.KEY_LEFT) or pyxel.btn(pyxel.KEY_A):
            self.dx -= 1
            self.direcao_x = -1
            self.direcao_y = 0

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.btn(pyxel.KEY_S):
            self.dy += 1
            self.direcao_x = 0
            self.direcao_y = 1

        if pyxel.btn(pyxel.KEY_UP) or pyxel.btn(pyxel.KEY_W):
            self.dy -= 1
            self.direcao_x = 0
            self.direcao_y = -1


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
            
        limitar_tela(self)
                
    def draw(self):
        # bola
        cor_atual = self.cor
        
        # passo sombrio
        if self.upgrades["passo_sombrio"] and self.dash.ativo:
            cor_atual = 0


        if self.cooldown_receber_dano > 0 and not self.upgrades["passo_sombrio"]:
            cor_atual = 13

        if self.dash.reducao_dano and not self.upgrades["passo_sombrio"]:
            cor_atual = 10
                
        #dano
        if self.tempo_exibir_dano > 0:
        
            pyxel.text(
                self.x - 10,
                self.y - 20,
                f"-{int(self.ultimo_dano)}",
                8
            )


        pyxel.circ(
            self.x,
            self.y,
            self.raio,
            cor_atual
        )


        # espada
        if self.upgrades["espada"]:

            if self.cooldown_ataque > 0:
                # atacando
                pyxel.rect(
                    self.x + 7,
                    self.y + 1,
                    20,
                    3,
                    2
                )

            else:
                # normal
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
        self.dash.draw_barra_dash(self.x, self.y)
        self.draw_barra_ataque()
        
        

class Dash:
    def __init__(self):

        self.ativo = False
        
        self.timer = 0
        self.duracao = 10
        
        self.cooldown = 0
        self.cooldown_max = 70
        
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
 

    def draw_barra_dash(self, x, y):
        if self.cooldown > 0:
         
            largura = 6
            altura = 5

            progresso = 1 - (self.cooldown / self.cooldown_max)

            pyxel.rect(x - largura//2 -10,y + 15,largura, altura,1)

            pyxel.rect(x - largura//2 -10, y + 15, largura * progresso, altura, 10)
        return