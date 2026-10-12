import random

import pyxel

from inimigos import Inimigo
from itens import Espada, Espadao, Manopla


class ModoInfinito:
    def __init__(self):
        self.wave = 0
        self.bau_aberto = False
        self.arma_do_bau = random.choice((Espada, Espadao, Manopla))()
        self.inimigos = []
        self.wave_em_andamento = False
        self.imagem_sala = pyxel.Image(256, 256)
        self.imagem_sala.load(0, 0, "assets/sala_infinita.png")

    def abrir_bau(self, jogador):
        if self.bau_aberto:
            return False
        perto = (
            jogador.x < 140
            and jogador.x + jogador.largura > 116
            and jogador.y < 140
            and jogador.y + jogador.altura > 116
        )
        if perto and pyxel.btnp(pyxel.KEY_E):
            self.bau_aberto = True
            self.arma_do_bau.pegar(jogador)
            self.criar_proxima_wave(jogador)
            return True
        return False

    def criar_inimigo(self, tipo, jogador):
        while True:
            x = random.randint(24, 220)
            y = random.randint(24, 220)
            distancia_jogador = ((x - jogador.x) ** 2 + (y - jogador.y) ** 2) ** 0.5
            longe_do_centro = not (85 < x < 171 and 85 < y < 171)
            longe_dos_outros = all(
                abs(x - outro.x) > 18 or abs(y - outro.y) > 18
                for outro in self.inimigos
            )

            if longe_do_centro and distancia_jogador >= 60 and longe_dos_outros:
                break

        variante = random.randint(1, 2)
        inimigo = Inimigo(x, y, tipo, variante)
        aumento = self.wave - 1
        if tipo == "elite":
            inimigo.vida = 25 + aumento * 3
            inimigo.dano = 12 + aumento // 2
        elif tipo == "boss":
            inimigo.vida = 65 + aumento * 5
            inimigo.dano = 18 + aumento // 2
            inimigo.velocidade = 0.7
        else:
            inimigo.vida = 10 + aumento * 2
            inimigo.dano = 10 + aumento // 2
        inimigo.vida_max = inimigo.vida
        return inimigo

    def criar_proxima_wave(self, jogador):
        self.wave += 1
        self.inimigos = []
        if self.wave % 10 == 0:
            self.inimigos.append(self.criar_inimigo("boss", jogador))
        else:
            quantidade = min(2 + (self.wave - 1) // 3, 10)
            for _ in range(quantidade):
                self.inimigos.append(self.criar_inimigo("comum", jogador))
            if self.wave % 3 == 0:
                self.inimigos.append(self.criar_inimigo("elite", jogador))
        self.wave_em_andamento = True

    def draw(self):
        pyxel.blt(0, 0, self.imagem_sala, 0, 0, 256, 256)
        if not self.bau_aberto:
            pyxel.blt(120, 124, 1, 69, 112, 16, 12, 7)
            pyxel.text(106, 142, "Pressione E", 7)
        else:
            pyxel.blt(120, 120, 1, 88, 108, 16, 16, 7)
            pyxel.text(106, 8, "WAVE " + str(self.wave), 7)

            if self.wave % 10 == 0:
                tipo_wave = "BOSS"
            elif self.wave % 3 == 0:
                tipo_wave = "ELITE"
            else:
                tipo_wave = "COMUM"

            waves_ate_upgrade = 2 - self.wave % 2
            pyxel.text(8, 8, "TIPO: " + tipo_wave, 7)
            pyxel.text(8, 16, "UPGRADE EM: " + str(waves_ate_upgrade), 7)
            pyxel.text(8, 24, "FORCA: " + str(self.wave), 7)
