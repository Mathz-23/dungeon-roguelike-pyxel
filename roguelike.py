import pyxel
import textwrap
import random
from jogador import Personagem
from inventario import sortear_upgrades
from inimigos import Inimigo
from menu import Menu

class Roguelike:

    def __init__(self):
        self.menu = Menu()
        self.reiniciar_jogo()

    def reiniciar_jogo(self):

        self.jogador = Personagem(50, 50, 10, 10, 7)
        self.fase = 0
        self.inimigos = []
        self.preparar_upgrade()

    def iniciar_fase(self):
        self.fase += 1
        # Reposiciona o mesmo jogador, preservando vida e upgrades.
        self.jogador.x = 50
        self.jogador.y = 50
        self.jogador.tempo_visual_ataque = 0
        self.jogador.area_ultimo_ataque = None
        maximo_inimigos = self.fase * 2
        quantidade = (
            2 if self.fase == 1
            else random.randint(maximo_inimigos - 1, maximo_inimigos)
        )
        self.inimigos = [
            Inimigo(random.randint(140, 236), random.randint(30, 236))
            for _ in range(quantidade)
        ]
        

        self.escolhendo_upgrade = False

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

        if self.escolhendo_upgrade:
            escolha = None
            if pyxel.btnp(pyxel.KEY_1):
                escolha = 0
            elif pyxel.btnp(pyxel.KEY_2):
                escolha = 1

            if escolha is not None:
                self.jogador.pegar_upgrade(self.opcoes[escolha])
                self.iniciar_fase()


        else:
            self.jogador.update()
            self.jogador.atacar(self.inimigos)

            for inimigo in self.inimigos:
                if inimigo.esta_vivo() and self.jogador.esta_vivo():
                    inimigo.update(self.jogador, self.inimigos)

            self.inimigos = [
                inimigo
                for inimigo in self.inimigos
                if inimigo.esta_vivo()
            ]

            if not self.inimigos and self.jogador.esta_vivo():
                self.preparar_upgrade()

    def draw(self):
        if self.menu.state != "game":
            self.menu.draw()
            return

        pyxel.cls(0)


        if self.escolhendo_upgrade:
            titulo = (
                f"Fase {self.fase} concluida!"
                if self.fase > 0
                else "Prepare-se para a fase 1"
            )
            pyxel.text((256 - len(titulo) * 4) // 2, 16, titulo, 10)
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
                    for linha, texto in enumerate(textwrap.wrap(titulo, width=21)):
                        pyxel.text(x + 5, y + 6 + linha * 8, texto, 7)
                    pyxel.text(x + 5, y + 28, f"Nivel {nivel - 1} -> {nivel}", 7)
                    bonus = getattr(self.opcoes[i], "bonus_melhoria", "+2 de dano")
                    pyxel.text(x + 5, y + 38, bonus, 10)
                else:
                    pyxel.text(x + 5, y + 22, titulo, 7)

            instrucao = "Pressione 1 ou 2 para escolher"
            pyxel.text((256 - len(instrucao) * 4) // 2, 154, instrucao, 7)
            proxima_fase = f"Proxima fase: {self.fase + 1}"
            pyxel.text((256 - len(proxima_fase) * 4) // 2, 166, proxima_fase, 7)

        else:
            self.jogador.draw()
            for inimigo in self.inimigos:
                inimigo.draw()
            pyxel.text(8, 8, f"Fase: {self.fase}", 7)
            pyxel.text(8, 16, f"Inimigos: {len(self.inimigos)}", 7)
            
    
        
if __name__ == "__main__":
    pyxel.init(256,256,fps=30)
    jogo = Roguelike()
    pyxel.run(jogo.update, jogo.draw)
