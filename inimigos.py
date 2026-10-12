import pyxel
from entidades import Entidade
from colisao import distancia, colidiu


class Inimigo(Entidade):
    def __init__(self, x, y, tipo="comum", variante=1):
        self.tipo = tipo
        self.variante = variante

        if tipo == "boss":
            largura, altura = 15, 16
        elif tipo == "elite" and variante == 1:
            largura, altura = 15, 13
        elif tipo == "elite":
            largura, altura = 10, 14
        elif variante == 1:
            largura, altura = 8, 11
        else:
            largura, altura = 8, 12

        super().__init__(x, y, largura, altura, 10, 10)
        self.velocidade = 1
        self.defesa = 0
        self.direcao_sprite = 1
        self.quadro_animacao = 0
        self.tempo_animacao = 0
        self.movendo = False
        
        
    def atacar(self, jogador):
        if self.cooldown_ataque > 0:
            return

        if colidiu(self, jogador, 2):

            dano_real = max(0, self.dano - jogador.defesa)

            jogador.receber_dano(dano_real, self)

            self.cooldown_ataque = 50
            
      
        
    def seguir(self, jogador):

        dx = jogador.x - self.x
        dy = jogador.y - self.y

        distancia_atual = distancia(self, jogador)

        if not colidiu(self, jogador, 2):

            if abs(dx) >= abs(dy):
                self.direcao_sprite = 3 if dx > 0 else 2
            else:
                self.direcao_sprite = 1 if dy > 0 else 0

            dx /= distancia_atual
            dy /= distancia_atual

            self.x += dx * self.velocidade
            self.y += dy * self.velocidade
            self.movendo = True
        else:
            self.movendo = False

    def atualizar_animacao(self):
        if not self.movendo:
            self.quadro_animacao = 0
            self.tempo_animacao = 0
            return

        self.tempo_animacao += 1
        if self.tempo_animacao >= 8:
            self.tempo_animacao = 0
            quantidade_quadros = 2
            self.quadro_animacao = (
                self.quadro_animacao + 1
            ) % quantidade_quadros
        
    def separar(self, inimigos):

        for outro in inimigos:

            if outro == self:
                continue

            if colidiu(self, outro, 2):

                dx = self.x - outro.x
                dy = self.y - outro.y

                distancia_atual = distancia(self, outro)

                if distancia_atual == 0:
                    self.x += 1
                else:

                    dx /= distancia_atual
                    dy /= distancia_atual

                    self.x += dx
                    self.y += dy
        

    def update(self, jogador, inimigos):
        self.atualizar_temporizadores()
        
        self.atacar(jogador)
        self.seguir(jogador)
        self.separar(inimigos)
        self.atualizar_animacao()

        # Os inimigos ficam dentro das paredes da sala.
        self.x = max(8, min(248 - self.largura, self.x))
        self.y = max(8, min(248 - self.altura, self.y))

    def draw(self):
        origem_x, origem_y, largura_sprite, altura_sprite = self.origem_sprite()
        desenho_x = self.x + (self.largura - largura_sprite) / 2
        desenho_y = self.y + (self.altura - altura_sprite) / 2
        pyxel.blt(
            desenho_x,
            desenho_y,
            0,
            origem_x,
            origem_y,
            largura_sprite,
            altura_sprite,
            7,
        )

        pyxel.text(
            self.x - 10,
            self.y - 10,
            f"HP: {int(self.vida)}",
            10
        )

        if self.tempo_exibir_dano > 0:

            pyxel.text(
                self.x - 10,
                self.y - 20,
                f"-{int(self.ultimo_dano)}",
                7
            )

    def origem_sprite(self):
        quadro = self.quadro_animacao
        direcao = self.direcao_sprite

        if self.tipo == "boss":
            x = 1 + direcao * 17
            if self.movendo:
                y = 67 + quadro * 18
            else:
                y = 49
            return x, y, 15, 16
        elif self.tipo == "elite" and self.variante == 1:
            origens_x = (1, 18, 35, 49)
            larguras = (15, 15, 12, 12)
            y = 161 if not self.movendo else 176 + quadro * 15
            return origens_x[direcao], y, larguras[direcao], 13
        elif self.tipo == "elite":
            origens_x = (121, 133, 145, 156)
            larguras = (10, 10, 9, 9)
            y = 161 if not self.movendo else 177 + quadro * 16
            return origens_x[direcao], y, larguras[direcao], 14
        elif self.variante == 1:
            origens_x = (1, 11, 21, 31)
            y = 113 if not self.movendo else 126 + quadro * 13
            return origens_x[direcao], y, 8, 11
        else:
            origens_x = (97, 106, 115, 125)
            larguras = (7, 7, 8, 8)
            y = 113 if not self.movendo else 127 + quadro * 14
            return origens_x[direcao], y, larguras[direcao], 12


