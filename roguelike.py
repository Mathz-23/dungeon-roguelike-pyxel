import pyxel
import textwrap
from jogador import Personagem
from inventario import sortear_upgrades
from menu import Menu
from mapa import Mapa
from modo_infinito import ModoInfinito

class Roguelike:

    def __init__(self):
        pyxel.images[0].load(0, 0, "assets/jogador.png")
        pyxel.images[1].load(0, 0, "assets/jogador_armadura.png")
        pyxel.images[2].load(0, 0, "assets/aura_espinhos.png")
        pyxel.images[2].load(32, 0, "assets/passo_sombrio.png")
        pyxel.images[2].load(96, 0, "assets/jogador_dano.png")
        pyxel.images[2].load(160, 0, "assets/botas.png")
        pyxel.images[1].load(64, 64, "assets/itens.png")
        pyxel.images[1].load(160, 64, "assets/interface_armas.png")
        pyxel.images[1].load(200, 64, "assets/marcador_arma_bloqueada.png")
        pyxel.images[1].load(216, 64, "assets/marcador_arma_selecionada.png")
        pyxel.images[0].load(0, 48, "assets/boss.png")
        pyxel.images[0].load(0, 112, "assets/inimigo_comum_1.png")
        pyxel.images[0].load(96, 112, "assets/inimigo_comum_2.png")
        pyxel.images[0].load(0, 160, "assets/inimigo_elite_1.png")
        pyxel.images[0].load(120, 160, "assets/inimigo_elite_2.png")
        self.menu = Menu()
        self.reiniciar_jogo()

    def reiniciar_jogo(self):

        self.jogador = Personagem(50, 50, 11, 13, 7)
        self.mapa = Mapa()
        self.inimigos = self.mapa.sala_atual.inimigos
        self.opcoes = []
        self.mensagem = []
        self.escolhendo_upgrade = False
        self.modo_infinito = None

    def preparar_upgrade(self):
        self.opcoes = sortear_upgrades(self.jogador)
        self.mensagem = []
        self.escolhendo_upgrade = True

        for upgrade in self.opcoes:
            self.mensagem.append(upgrade.nome)

    def desenhar_interface_armas(self):
        pyxel.blt(8, 8, 1, 160, 64, 37, 13)

        armas = (
            ("espada", self.jogador.upgrades["espada"] > 0),
            ("espadao", self.jogador.upgrades["espadao_dano"] > 0),
            ("manopla", self.jogador.upgrades["manopla_dano"] > 0),
        )

        for posicao, (arma, possui) in enumerate(armas):
            marcador_x = None

            if self.jogador.arma_equipada == arma:
                marcador_x = 216
            elif not possui:
                marcador_x = 200

            if marcador_x is None:
                continue

            pyxel.blt(
                8 + posicao * 12,
                8,
                1,
                marcador_x,
                64,
                13,
                13,
                0,
            )


    def update(self):
        estado_anterior = self.menu.state
        self.menu.update()
        pyxel.mouse(True)

        if estado_anterior == "menu" and self.menu.state == "game":
            self.reiniciar_jogo()

        if estado_anterior == "victory" and self.menu.state == "infinite":
            self.mapa.preparar_acesso_infinito()
            self.inimigos = []
            self.menu.state = "game"
            return

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
                if self.modo_infinito is not None:
                    self.modo_infinito.criar_proxima_wave(self.jogador)
                    self.inimigos = self.modo_infinito.inimigos


            if len(self.opcoes) > 1 and pyxel.btnp(pyxel.KEY_2):

                self.jogador.pegar_upgrade(
                    self.opcoes[1]
                )

                self.escolhendo_upgrade = False
                if self.modo_infinito is not None:
                    self.modo_infinito.criar_proxima_wave(self.jogador)
                    self.inimigos = self.modo_infinito.inimigos


        elif self.modo_infinito is not None:
            self.update_modo_infinito()

        else:
            self.jogador.update()
            if self.mapa.tentar_mudar_sala(self.jogador):
                self.inimigos = self.mapa.sala_atual.inimigos

            self.mapa.coletar_chave(self.jogador)
            self.mapa.abrir_bau(self.jogador)

            if self.mapa.tentar_entrar_infinito(self.jogador):
                self.iniciar_modo_infinito()
                return

            if self.mapa.tentar_proximo_andar(self.jogador):
                self.inimigos = self.mapa.sala_atual.inimigos

            if self.mapa.jogo_concluido:
                self.menu.state = "victory"
                return

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
                venceu_boss_final = (
                    self.mapa.numero_andar == 5
                    and self.mapa.sala_atual.tipo == "boss"
                )
                if not venceu_boss_final:
                    self.preparar_upgrade()

    def iniciar_modo_infinito(self):
        # Um novo personagem remove todos os itens e upgrades antigos.
        self.jogador = Personagem(123, 180, 11, 13, 7)
        self.jogador.modo_infinito = True
        self.modo_infinito = ModoInfinito()
        self.inimigos = self.modo_infinito.inimigos
        self.escolhendo_upgrade = False

    def update_modo_infinito(self):
        self.jogador.update()
        self.jogador.x = max(8, min(248 - self.jogador.largura, self.jogador.x))
        self.jogador.y = max(8, min(248 - self.jogador.altura, self.jogador.y))

        self.modo_infinito.abrir_bau(self.jogador)
        self.inimigos = self.modo_infinito.inimigos
        self.jogador.atacar(self.inimigos)

        for inimigo in self.inimigos:
            if inimigo.esta_vivo() and self.jogador.esta_vivo():
                inimigo.update(self.jogador, self.inimigos)

        self.inimigos = [
            inimigo for inimigo in self.inimigos if inimigo.esta_vivo()
        ]
        self.modo_infinito.inimigos = self.inimigos

        if self.modo_infinito.wave_em_andamento and not self.inimigos:
            self.modo_infinito.wave_em_andamento = False
            if self.modo_infinito.wave % 2 == 0:
                self.preparar_upgrade()
            else:
                self.modo_infinito.criar_proxima_wave(self.jogador)
                self.inimigos = self.modo_infinito.inimigos

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
                (8, 78),
                (138, 78)
            ]

            for i, nome in enumerate(self.mensagem):

                x, y = posicoes[i]

                pyxel.rect(
                    x,
                    y,
                    110,
                    84,
                    1
                )

                pyxel.rectb(
                    x,
                    y,
                    110,
                    84,
                    7
                )

                nivel = getattr(self.opcoes[i], "nivel", 1)
                titulo = str(i + 1) + " - " + nome
                descricao = getattr(self.opcoes[i], "descricao", "")

                linhas_titulo = textwrap.wrap(titulo, width=25)
                for linha, texto in enumerate(linhas_titulo[:2]):
                    pyxel.text(x + 5, y + 7 + linha * 8, texto, 7)

                linhas_descricao = textwrap.wrap(descricao, width=25)
                for linha, texto in enumerate(linhas_descricao[:3]):
                    pyxel.text(x + 5, y + 29 + linha * 8, texto, 6)

                if nivel > 1:
                    pyxel.text(
                        x + 5,
                        y + 61,
                        "Nivel " + str(nivel - 1) + " -> " + str(nivel),
                        7,
                    )

                indicador = getattr(
                    self.opcoes[i], "indicador_melhoria", ""
                )
                pyxel.text(x + 5, y + 72, indicador, 10)

        else:
            if self.modo_infinito is not None:
                self.modo_infinito.draw()
            else:
                self.mapa.draw()
            self.jogador.draw()
            for inimigo in self.inimigos:
                inimigo.draw()
            if self.modo_infinito is None:
                self.mapa.draw_minimapa()
            self.desenhar_interface_armas()
            
    
        
if __name__ == "__main__":
    pyxel.init(256,256,fps=30)
    jogo = Roguelike()
    pyxel.run(jogo.update, jogo.draw)
