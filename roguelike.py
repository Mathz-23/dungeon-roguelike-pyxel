import pyxel
from jogador import Personagem
from inventario import sortear_upgrades
from inimigos import Inimigo

class Roguelike:

    def __init__(self):

        self.jogador = Personagem(50,50,5,7)

        
        self.inimigos = [
            Inimigo(200,90),
            Inimigo(200,100),
            Inimigo(200,110),
            Inimigo(200,120),
            Inimigo(200,130)
        ]
        

        self.opcoes = sortear_upgrades()

        self.mensagem = []

        self.escolhendo_upgrade = True

        for upgrade in self.opcoes:
            self.mensagem.append(upgrade.nome)


    def update(self):

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

                pyxel.text(
                    x + 5,
                    y + 22,
                    str(i + 1) + " - " + nome,
                    7
                )

        else:
            self.jogador.draw()
            for inimigo in self.inimigos:
                inimigo.draw()
            
    
        
pyxel.init(256,256)

jogo = Roguelike()

pyxel.run(jogo.update, jogo.draw)