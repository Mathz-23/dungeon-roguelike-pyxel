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
        self.dx = 0
        self.dy = 0
        
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

        # Imagem do jogador: cima, baixo, esquerda e direita.
        self.direcao_sprite = 1
        self.quadro_animacao = 0
        self.tempo_animacao = 0
        
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
        if self.arma_equipada == "soco":
            alcance = 4
            espessura = 8
        elif self.arma_equipada == "manopla":
            alcance = 10
            espessura = 10
        elif self.arma_equipada == "espada":
            alcance = 16
            espessura = 10
        else:
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

        if dano <= 0:
            if self.durabilidade_armadura > 0:
                self.durabilidade_armadura -= 1

                if self.durabilidade_armadura == 0:
                    self.defesa = 0

            return False

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

            inimigo.receber_dano(
                dano_refletido,
                ignorar_invencibilidade=True
            )

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

    def atualizar_animacao(self):
        if self.dx == 0 and self.dy == 0:
            self.quadro_animacao = 0
            self.tempo_animacao = 0
            return

        self.tempo_animacao += 1

        if self.tempo_animacao >= 8:
            self.tempo_animacao = 0
            self.quadro_animacao = 1 - self.quadro_animacao

    def desenhar_arma(self):
        if self.arma_equipada not in ("espada", "espadao"):
            return

        deslocamento_cor = 0

        if self.arma_equipada == "espada":
            nivel = 1 + (self.upgrades["espada"] - 5) // 2
            if nivel >= 6:
                deslocamento_cor = 55
            elif nivel >= 3:
                deslocamento_cor = 28

            comprimento = 10
            origem_cima = (70 + deslocamento_cor, 67, 3, 10)
            origem_baixo = (75 + deslocamento_cor, 67, 3, 10)
            origem_esquerda = (80 + deslocamento_cor, 69, 10, 3)
            origem_direita = (80 + deslocamento_cor, 74, 10, 3)
        else:
            melhorias = 0
            if self.upgrades["espadao_dano"] >= 14:
                melhorias += 1
            if self.upgrades["espadao_dano"] >= 18:
                melhorias += 1
            if self.upgrades["espadao_cooldown"] <= 82.5:
                melhorias += 1
            if self.upgrades["espadao_cooldown"] <= 75:
                melhorias += 1

            if melhorias >= 4:
                deslocamento_cor = 55
            elif melhorias >= 2:
                deslocamento_cor = 28

            comprimento = 14
            origem_cima = (70 + deslocamento_cor, 81, 3, 14)
            origem_baixo = (75 + deslocamento_cor, 81, 3, 14)
            origem_esquerda = (80 + deslocamento_cor, 91, -14, 3)
            origem_direita = (80 + deslocamento_cor, 84, 14, 3)

        centro_x = self.x + self.largura / 2
        centro_y = self.y + self.altura / 2

        direcao_x = self.direcao_x
        direcao_y = self.direcao_y

        if self.tempo_visual_ataque > 0:
            direcao_x, direcao_y = self.direcao_ultimo_ataque

        if direcao_x == 1:
            x = self.x + self.largura
            y = centro_y - 1
            origem = origem_direita
        elif direcao_x == -1:
            x = self.x - comprimento
            y = centro_y - 1
            origem = origem_esquerda
        elif direcao_y == 1:
            x = centro_x - 1
            y = self.y + self.altura
            origem = origem_baixo
        else:
            x = centro_x - 1
            y = self.y - comprimento
            origem = origem_cima

        if self.arma_equipada == "espada" and self.tempo_visual_ataque > 0:
            progresso = (6 - self.tempo_visual_ataque) / 5

            if progresso > 0.5:
                progresso = 1 - progresso

            distancia_estocada = progresso * 12
            x += direcao_x * distancia_estocada
            y += direcao_y * distancia_estocada

        origem_x, origem_y, largura, altura = origem
        pyxel.blt(x, y, 1, origem_x, origem_y, largura, altura, 7)

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
            self.direcao_sprite = 3

        if pyxel.btn(pyxel.KEY_A):
            self.dx -= 1
            self.direcao_sprite = 2

        if pyxel.btn(pyxel.KEY_S):
            self.dy += 1
            self.direcao_sprite = 1

        if pyxel.btn(pyxel.KEY_W):
            self.dy -= 1
            self.direcao_sprite = 0

        self.atualizar_animacao()

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

        # Imagem do jogador. A cor 7 (branco) fica transparente.
        sprite_x = 1 + self.direcao_sprite * 13
        sprite_y = 1

        if self.dx != 0 or self.dy != 0:
            sprite_y = 16 + self.quadro_animacao * 15

        banco_imagem = 0
        if self.durabilidade_armadura > 0:
            banco_imagem = 1

        if self.cooldown_receber_dano > 0:
            banco_imagem = 2
            sprite_x = 97 + self.direcao_sprite * 13

        if self.dash.invencivel:
            banco_imagem = 2
            sprite_x = 32 + self.direcao_sprite * 13
            sprite_y = self.quadro_animacao * 15

        pyxel.blt(
            self.x,
            self.y,
            banco_imagem,
            sprite_x,
            sprite_y,
            11,
            13,
            7
        )

        if self.upgrades["bota_celeridade"] > 0:
            botas_x = 161 + self.direcao_sprite * 13
            botas_y = 1

            if self.dx != 0 or self.dy != 0:
                botas_y = 16 + self.quadro_animacao * 15

            pyxel.blt(
                self.x,
                self.y,
                2,
                botas_x,
                botas_y,
                11,
                13,
                7
            )

        self.desenhar_arma()

        # Mostra a area atingida pela espada e pelo espadao.
        if (
            self.tempo_visual_ataque > 0
            and self.arma_equipada in ("espada", "espadao")
        ):
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
            else:
                pyxel.rectb(x, y, largura, altura, 7)

        # Visual do golpe dos punhos e da manopla.
        if (
            self.tempo_visual_ataque > 0
            and self.arma_equipada in ("soco", "manopla")
        ):
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

            deslocamento_braco = 4 * self.mao_ultimo_soco
            punho_x -= direcao_y * deslocamento_braco
            punho_y += direcao_x * deslocamento_braco

            pyxel.rect(punho_x, punho_y, tamanho, tamanho, cor_punho)

        # armadura
        if self.durabilidade_armadura > 0:
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
            aura_x = self.x + (self.largura - 23) / 2
            aura_y = self.y + (self.altura - 23) / 2

            pyxel.blt(
                aura_x,
                aura_y,
                2,
                0,
                0,
                23,
                23,
                7
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
