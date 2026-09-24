import pyxel
import math
from entidades import Entidade
from colisao import ataque_colidiu, limitar_tela

        
class Personagem(Entidade):
    def __init__(self, x, y, largura, altura, cor):
        super().__init__(x, y, largura, altura, 50, 1)
        self.cor = cor
        self.velocidade_base = 1.5
        self.velocidade_dash = 6
        
        self.direcao_x = 1
        self.direcao_y = 0
        self.mira_teclado = False
        self.ultima_posicao_mouse = (pyxel.mouse_x, pyxel.mouse_y)

        self.defesa = 0
        self.durabilidade_armadura = 0
        self.durabilidade_armadura_max = 0
        self.ultima_cura = 0
        self.tempo_exibir_cura = 0
        self.timer_cura = 0
        self.cooldown_ataque_max = 30
        self.tempo_visual_ataque = 0
        self.area_ultimo_ataque = None
        self.direcao_ultimo_ataque = (1, 0)
        self.proxima_mao = 1  # 1: direita; -1: esquerda
        self.mao_ultimo_soco = 1
        self.arma_equipada = "soco"
        
        self.upgrades = {
            "espada": 0,
            "espadao_dano": 0,
            "espadao_cooldown": 0,
            "manopla_dano": 0,
            "manopla_cooldown": 0,
            "armadura": 0,
            "armadura_durabilidade": 0,
            "vida_extra": 0,
            "bota_celeridade": 0,
            "passo_sombrio": False,
            "aura_espinhos": 0,
            "cura_continua": 0
        }
        
        self.inventario = []

        self.dash = Dash()

    def equipar_arma(self, tipo):
        if tipo == "soco":
            if self.upgrades["manopla_dano"] > 0:
                self.arma_equipada = "manopla"
                self.dano = self.upgrades["manopla_dano"]
                self.cooldown_ataque_max = self.upgrades["manopla_cooldown"]
            else:
                self.arma_equipada = "soco"
                self.dano = 1
                self.cooldown_ataque_max = 30
        elif tipo == "espada" and self.upgrades["espada"] > 0:
            self.arma_equipada = "espada"
            self.dano = self.upgrades["espada"]
            self.cooldown_ataque_max = 52.5
        elif tipo == "espadao" and self.upgrades["espadao_dano"] > 0:
            self.arma_equipada = "espadao"
            self.dano = self.upgrades["espadao_dano"]
            self.cooldown_ataque_max = self.upgrades["espadao_cooldown"]
        else:
            self.equipar_arma("soco")
    
    def hitbox_ataque(self):
        alcance = 15
        espessura = 10

        if self.arma_equipada == "espadao":
            alcance = 24
            espessura = 30
        
        centro_x = self.x + self.largura / 2
        centro_y = self.y + self.altura / 2
        
        
        #direita
        if self.direcao_x == 1:
            return (
                self.x + self.largura,
                centro_y - espessura / 2,
                alcance,
                espessura
            )
            
        #esquerda
        if self.direcao_x == -1:
            return (
                self.x - alcance,
                centro_y - espessura / 2,
                alcance,
                espessura
            )
        
        #baixo
        if self.direcao_y == 1:
            return (
                centro_x - espessura / 2,
                self.y + self.altura,
                espessura,
                alcance
            )
        #cima
        return (
            centro_x - espessura / 2,
            self.y - alcance,
            espessura,
            alcance
        )

    def atacar(self, inimigos):
        if self.cooldown_ataque > 0:
            return

        quer_atacar = (
            pyxel.btn(pyxel.MOUSE_BUTTON_LEFT)
            or pyxel.btn(pyxel.KEY_SPACE)
        )
        if not quer_atacar:
            return

        area = self.hitbox_ataque()
        self.area_ultimo_ataque = area
        self.direcao_ultimo_ataque = (self.direcao_x, self.direcao_y)
        self.tempo_visual_ataque = 10 if self.arma_equipada == "espadao" else 6
        self.cooldown_ataque = self.cooldown_ataque_max

        if self.arma_equipada in ("soco", "manopla"):
            self.mao_ultimo_soco = self.proxima_mao
            self.proxima_mao *= -1

        for inimigo in inimigos:
            if not inimigo.esta_vivo():
                continue

            if ataque_colidiu(area, inimigo):
                dano_real = max(0, self.dano - inimigo.defesa)
                acertou = inimigo.receber_dano(dano_real)
                if acertou and self.arma_equipada != "espadao":
                    break
                
    def draw_barra_ataque(self):
        if self.cooldown_ataque > 0:
         
            largura = 6
            altura = 5

            centro_x = self.x + self.largura / 2
            x = centro_x - largura // 2 + 10
            y = self.y + self.altura + 10

            progresso = 1 - (self.cooldown_ataque / self.cooldown_ataque_max)
            progresso = max(0, min(1, progresso))

            pyxel.rect(x, y, largura, altura, 1)

            pyxel.rect(x, y, largura * progresso, altura, 14)
        return
    
    def atualizar_cura(self):
        if not self.upgrades["cura_continua"]:
            return

        if not self.esta_vivo():
            return

        self.timer_cura += 1

        if self.timer_cura >= 90:
            self.timer_cura = 0

            vida_anterior = self.vida
            self.vida = min(
                self.vida + self.upgrades["cura_continua"],
                self.vida_max
            )
            cura_real = self.vida - vida_anterior

            if cura_real > 0:
                self.ultima_cura = cura_real
                self.tempo_exibir_cura = 20
    
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

        if self.durabilidade_armadura > 0:
            self.durabilidade_armadura -= 1

            if self.durabilidade_armadura == 0:
                self.defesa = 0

        # aura de espinhos
        if self.upgrades["aura_espinhos"] and inimigo:

            porcentagem = self.upgrades["aura_espinhos"] / 100
            dano_refletido = max(1, int(dano * porcentagem))

            inimigo.receber_dano(dano_refletido)

        return True
    
    
    def pegar_upgrade(self, upgrade):

        self.inventario.append(upgrade)

        upgrade.efeito(self)
                

    def atualizar_mira(self):
        posicao_mouse = (pyxel.mouse_x, pyxel.mouse_y)
        mouse_moveu = posicao_mouse != self.ultima_posicao_mouse
        self.ultima_posicao_mouse = posicao_mouse

        # Setas seguradas tem prioridade sobre o mouse.
        direcoes = (
            (pyxel.KEY_RIGHT, 1, 0),
            (pyxel.KEY_LEFT, -1, 0),
            (pyxel.KEY_DOWN, 0, 1),
            (pyxel.KEY_UP, 0, -1),
        )
        for tecla, direcao_x, direcao_y in direcoes:
            if pyxel.btn(tecla):
                self.direcao_x = direcao_x
                self.direcao_y = direcao_y
                self.mira_teclado = True
                return

        if mouse_moveu:
            self.mira_teclado = False

        if self.mira_teclado:
            return

        centro_x = self.x + self.largura / 2
        centro_y = self.y + self.altura / 2

        dx = pyxel.mouse_x - centro_x
        dy = pyxel.mouse_y - centro_y

        # Mantem a direcao quando o cursor esta no centro.
        if dx == 0 and dy == 0:
            return

        if abs(dx) >= abs(dy):
            self.direcao_x = 1 if dx > 0 else -1
            self.direcao_y = 0
        else:
            self.direcao_x = 0
            self.direcao_y = 1 if dy > 0 else -1

    def update(self):
        #dano
        self.atualizar_temporizadores()

        if self.tempo_visual_ataque > 0:
            self.tempo_visual_ataque -= 1
        
        if self.tempo_exibir_cura > 0:
            self.tempo_exibir_cura -= 1
            
        self.atualizar_cura()

        if pyxel.btnp(pyxel.KEY_1):
            self.equipar_arma("soco")
        elif pyxel.btnp(pyxel.KEY_2):
            self.equipar_arma("espada")
        elif pyxel.btnp(pyxel.KEY_3):
            self.equipar_arma("espadao")
        
        
        # morte
        if self.vida <= 0:
            pyxel.quit()
        self.dx = 0
        self.dy = 0

        if pyxel.btn(pyxel.KEY_D):
            self.dx += 1

        if pyxel.btn(pyxel.KEY_A):
            self.dx -= 1

        if pyxel.btn(pyxel.KEY_S):
            self.dy += 1

        if pyxel.btn(pyxel.KEY_W):
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
            
        limitar_tela(self)
        self.atualizar_mira()
                
    def draw(self):
        centro_x = self.x + self.largura / 2
        centro_y = self.y + self.altura / 2
        base_y = self.y + self.altura

        cor_atual = self.cor

        if self.upgrades["passo_sombrio"] and self.dash.ativo:
            cor_atual = 0

        if (
            self.cooldown_receber_dano > 0
            and not self.upgrades["passo_sombrio"]
        ):
            cor_atual = 13

        if (
            self.dash.reducao_dano
            and not self.upgrades["passo_sombrio"]
        ):
            cor_atual = 10

        # cura
        if self.tempo_exibir_cura > 0:
            pyxel.text(
                centro_x - 10,
                self.y - 23,
                f"+{int(self.ultima_cura)}",
                11
            )

        # dano
        if self.tempo_exibir_dano > 0:
            pyxel.text(
                centro_x - 10,
                self.y - 15,
                f"-{int(self.ultimo_dano)}",
                8
            )

        # corpo
        pyxel.rect(
            self.x,
            self.y,
            self.largura,
            self.altura,
            cor_atual
        )

        # Visual do golpe: espada ou pequeno punho.
        if self.tempo_visual_ataque > 0:
            x, y, largura, altura = self.area_ultimo_ataque

            if self.arma_equipada == "espadao":
                pyxel.rectb(x, y, largura, altura, 10)
                progresso = (10 - self.tempo_visual_ataque) / 9

                if self.direcao_ultimo_ataque[0] != 0:
                    corte_y = y + progresso * (altura - 4)
                    pyxel.rect(x, corte_y, largura, 4, 7)
                else:
                    corte_x = x + progresso * (largura - 4)
                    pyxel.rect(corte_x, y, 4, altura, 7)

            elif self.arma_equipada == "espada":
                pyxel.rectb(x, y, largura, altura, 7)
                if largura > altura:
                    pyxel.rect(x, y + (altura - 3) / 2, largura, 3, 2)
                else:
                    pyxel.rect(x + (largura - 3) / 2, y, 3, altura, 2)
            else:
                tamanho = 6 if self.arma_equipada == "manopla" else 4
                cor_punho = 10 if self.arma_equipada == "manopla" else cor_atual
                direcao_x, direcao_y = self.direcao_ultimo_ataque
                punho_x = centro_x - tamanho / 2
                punho_y = centro_y - tamanho / 2

                if direcao_x == 1:
                    punho_x = self.x + self.largura
                elif direcao_x == -1:
                    punho_x = self.x - tamanho
                elif direcao_y == 1:
                    punho_y = self.y + self.altura
                else:
                    punho_y = self.y - tamanho

                # Mantem a mao escolhida durante toda a animacao do soco.
                deslocamento_braco = 4 * self.mao_ultimo_soco
                punho_x -= direcao_y * deslocamento_braco
                punho_y += direcao_x * deslocamento_braco

                pyxel.rect(punho_x, punho_y, tamanho, tamanho, cor_punho)

        # Espada em repouso acompanha a direcao do jogador.
        elif self.arma_equipada in ("espada", "espadao"):
            comprimento = 14 if self.arma_equipada == "espadao" else 8
            espessura = 5 if self.arma_equipada == "espadao" else 3

            if self.direcao_x == 1:
                pyxel.rect(self.x + self.largura, centro_y - espessura / 2,
                           comprimento, espessura, 2)
            elif self.direcao_x == -1:
                pyxel.rect(self.x - comprimento, centro_y - espessura / 2,
                           comprimento, espessura, 2)
            elif self.direcao_y == 1:
                pyxel.rect(centro_x - espessura / 2, self.y + self.altura,
                           espessura, comprimento, 2)
            else:
                pyxel.rect(centro_x - espessura / 2, self.y - comprimento,
                           espessura, comprimento, 2)

        # armadura
        if self.durabilidade_armadura > 0:
            pyxel.rectb(
                self.x - 2,
                self.y - 2,
                self.largura + 4,
                self.altura + 4,
                10
            )

            pyxel.text(
                self.x - 4,
                self.y - 10,
                str(self.durabilidade_armadura)
                + "/"
                + str(self.durabilidade_armadura_max),
                10,
            )

        # aura de espinhos
        if self.upgrades["aura_espinhos"]:
            pyxel.rectb(
                self.x - 4,
                self.y - 4,
                self.largura + 8,
                self.altura + 8,
                8
            )

        # barra de vida
        barra_x = centro_x - 15
        barra_y = base_y + 3

        progresso = max(0, min(1, self.vida / self.vida_max))

        pyxel.rect(barra_x, barra_y, 30, 5, 8)
        pyxel.rect(barra_x, barra_y, 30 * progresso, 5, 11)

        pyxel.text(
            barra_x + 3,
            barra_y,
            f"{self.vida}/{self.vida_max}",
            7
        )

        self.dash.draw_barra_dash(centro_x, base_y + 10)
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
         
            largura = 10
            altura = 5

            progresso = 1 - (self.cooldown / self.cooldown_max)

            barra_x = x - largura - 5
            pyxel.rect(barra_x, y, largura, altura, 1)

            pyxel.rect(barra_x, y, largura * progresso, altura, 10)
        return
