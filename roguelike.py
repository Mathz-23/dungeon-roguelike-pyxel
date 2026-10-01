import pyxel
import textwrap
from jogador import Personagem
from inventario import sortear_upgrades
from menu import Menu
from mapa import Mapa

class Roguelike:

    def __init__(self):
        pyxel.images[0].load(0, 0, "assets/jogador.png")
        pyxel.images[1].load(0, 0, "assets/jogador_armadura.png")
        pyxel.images[2].load(0, 0, "assets/aura_espinhos.png")
        pyxel.images[2].load(32, 0, "assets/passo_sombrio.png")
        pyxel.images[2].load(96, 0, "assets/jogador_dano.png")
        pyxel.images[2].load(160, 0, "assets/botas.png")
        pyxel.images[1].load(64, 64, "assets/itens.png")
        self.menu = Menu()
        self.reiniciar_jogo()

    def reiniciar_jogo(self):

        self.jogador = Personagem(50, 50, 11, 13, 7)
        self.mapa = Mapa()
        self.inimigos = self.mapa.sala_atual.inimigos
        self.opcoes = []
        self.mensagem = []
        self.escolhendo_upgrade = False
        self.tempo_vitoria = 90

    def preparar_upgrade(self):
        self.opcoes = sortear_upgrades(self.jogador)
        self.mensagem = []
        self.escolhendo_upgrade = True

        for upgrade in self.opcoes:
            self.mensagem.append(upgrade.nome)


    def update(self):
        estado_anterior = self.menu.state
        self.menu.update()
        pyxel.mouse(True)

        if estado_anterior == "menu" and self.menu.state == "game":
            self.reiniciar_jogo()

        if self.menu.state != "game" or estado_anterior != "game":
            return

        if self.jogador.vida <= 0:
            self.menu.state = "game_over"
            pyxel.mouse(True)
            return

        self.update_game()

        if self.jogador.vida <= 0:
            self.menu.state = "game_over"
            pyxel.mouse(True)

    def update_game(self):

        if self.mapa.jogo_concluido:
            self.tempo_vitoria -= 1

            if self.tempo_vitoria <= 0:
                self.menu.state = "menu"

            return

        if self.escolhendo_upgrade:

            if pyxel.btnp(pyxel.KEY_1):

                self.jogador.pegar_upgrade(
                    self.opcoes[0]
                )

                self.escolhendo_upgrade = False


            if pyxel.btnp(pyxel.KEY_2):

                self.jogador.pegar_upgrade(
                    self.opcoes[1]
                )

                self.escolhendo_upgrade = False


        else:
            self.jogador.update()
            if self.mapa.tentar_mudar_sala(self.jogador):
                self.inimigos = self.mapa.sala_atual.inimigos

            self.mapa.coletar_chave(self.jogador)
            self.mapa.abrir_bau(self.jogador)

            if self.mapa.tentar_proximo_andar(self.jogador):
                self.inimigos = self.mapa.sala_atual.inimigos

            self.jogador.atacar(self.inimigos)

            for inimigo in self.inimigos:
                if inimigo.esta_vivo() and self.jogador.esta_vivo():
                    inimigo.update(self.jogador, self.inimigos)

            self.inimigos = [
                inimigo
                for inimigo in self.inimigos
                if inimigo.esta_vivo()
            ]
            self.mapa.sala_atual.inimigos = self.inimigos

            if self.mapa.concluir_sala():
                self.preparar_upgrade()

    def draw(self):
        if self.menu.state != "game":
            self.menu.draw()
            return

        pyxel.cls(0)


        if self.escolhendo_upgrade:
            pyxel.text(
                90,
                30,
                "Escolha um upgrade:",
                7
            )

            posicoes = [
                (20, 90),
                (140, 90)
            ]

            for i, nome in enumerate(self.mensagem):

                x, y = posicoes[i]

                pyxel.rect(
                    x,
                    y,
                    95,
                    50,
                    1
                )

                pyxel.rectb(
                    x,
                    y,
                    95,
                    50,
                    7
                )

                nivel = getattr(self.opcoes[i], "nivel", 1)
                titulo = str(i + 1) + " - " + nome

                if nivel > 1:
                    linhas = textwrap.wrap(titulo, width=21)
                    for linha, texto in enumerate(linhas):
                        pyxel.text(x + 5, y + 6 + linha * 8, texto, 7)

                    pyxel.text(
                        x + 5,
                        y + 28,
                        "Nivel " + str(nivel - 1) + " -> " + str(nivel),
                        7,
                    )
                    bonus = getattr(
                        self.opcoes[i], "bonus_melhoria", "Melhoria"
                    )
                    pyxel.text(x + 5, y + 38, bonus, 10)
                else:
                    pyxel.text(x + 5, y + 22, titulo, 7)

        else:
            self.mapa.draw()
            self.jogador.draw()
            for inimigo in self.inimigos:
                inimigo.draw()
            self.mapa.draw_minimapa()
            pyxel.text(8, 8, "Arma: " + self.jogador.arma_equipada, 7)

            if self.mapa.jogo_concluido:
                pyxel.rect(48, 100, 160, 50, 0)
                pyxel.rectb(48, 100, 160, 50, 7)
                pyxel.text(73, 120, "Voce venceu os 5 andares!", 10)
            
    
        
if __name__ == "__main__":
    pyxel.init(256,256,fps=30)
    jogo = Roguelike()
    pyxel.run(jogo.update, jogo.draw)
