import pyxel
from jogador import Personagem
from inventario import sortear_upgrades
from inimigos import Inimigo
from menu import Menu

class Roguelike:

    def __init__(self):

        self.menu = Menu()
        
        self.jogador = Personagem(50,50,5,7)

        self.state = "menu"
        
        self.inimigos = [
            Inimigo(200,90),
            Inimigo(200,100)
        ]
        

        self.opcoes = sortear_upgrades()

        self.mensagem = []

        self.escolhendo_upgrade = True

        for upgrade in self.opcoes:
            self.mensagem.append(upgrade.nome)

    def reiniciar_jogo(self):

        self.jogador = Personagem(50,50,5,7)

        self.inimigos = [
            Inimigo(200,90),
            Inimigo(200,100)
        ]

        self.opcoes = sortear_upgrades()

        self.mensagem = []

        for upgrade in self.opcoes:
            self.mensagem.append(upgrade.nome)

        self.escolhendo_upgrade = True


    def update(self):
        
        if self.state == "menu":

            self.menu.update()

            if self.menu.state == "game":
                self.reiniciar_jogo()
                self.state = "game"
                        
                

        elif self.state == "game": 
        
            if self.jogador.vida <= 0:
                self.state = "game_over"
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

                for inimigo in self.inimigos:
                    inimigo.update(
                        self.jogador,
                        self.inimigos
                    )


        elif self.state == "game_over":
            self.menu.update_gameover()
                    
            if self.menu.state == "menu":
                self.state = "menu"
                
    def draw(self):
        pyxel.cls(0)
        if self.state == "menu":

            self.menu.draw()
            
        elif self.state == "game_over":
        
            self.menu.draw_gameover()

        elif self.state == "game":


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
            

        
pyxel.init(256,256)

jogo = Roguelike()

pyxel.run(jogo.update, jogo.draw)
