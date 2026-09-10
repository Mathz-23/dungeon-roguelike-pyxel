import pyxel
from jogador import Personagem
from inventario import sortear_upgrades
from inimigos import Inimigo
from menu import Menu

class Roguelike:

    def __init__(self):
        self.menu = Menu()
        self.reiniciar_jogo()

    def reiniciar_jogo(self):

        self.jogador = Personagem(50,50,5,7)

        
        self.inimigos = [
            Inimigo(200,90),
            Inimigo(200,100)
        ]
        

        self.opcoes = sortear_upgrades()

        self.mensagem = []

        self.escolhendo_upgrade = True

        for upgrade in self.opcoes:
            self.mensagem.append(upgrade.nome)


    def update(self):
        estado_anterior = self.menu.state
        self.menu.update()
        pyxel.mouse(self.menu.state != "game")

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

            for inimigo in self.inimigos:
                inimigo.update(
                    self.jogador,
                    self.inimigos
                )

                self.inimigos = [
                    inimigo for inimigo in self.inimigos
                    if inimigo.vida > 0
                ]
                self.jogador.atacar(self.inimigos)

    def draw(self):
        if self.menu.state != "game":
            self.menu.draw()
            return

        pyxel.cls(0)


        if self.escolhendo_upgrade:

            pyxel.text(
                20,
                20,
                "Escolha um upgrade:",
                7
            )


            for i, nome in enumerate(self.mensagem):

                pyxel.text(
                    20,
                    40 + i * 10,
                    str(i+1) + " - " + nome,
                    7
                )

        else:

            self.jogador.draw()

            for inimigo in self.inimigos:
                inimigo.draw()
            
    
        
if __name__ == "__main__":
    pyxel.init(256,256)
    jogo = Roguelike()
    pyxel.run(jogo.update, jogo.draw)
