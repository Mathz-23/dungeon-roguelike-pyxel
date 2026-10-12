import pyxel


class Menu:
    def __init__(self):
        pyxel.mouse(True)
        self.state = "menu"

        self.imagem_menu = pyxel.Image(256, 256)
        self.imagem_menu.load(0, 0, "assets/menu.png")
        self.imagem_regras = pyxel.Image(256, 256)
        self.imagem_regras.load(0, 0, "assets/regras.png")
        self.imagem_controles = pyxel.Image(256, 256)
        self.imagem_controles.load(0, 0, "assets/controles.png")
        self.imagem_game_over = pyxel.Image(256, 256)
        self.imagem_game_over.load(0, 0, "assets/game_over.png")
        self.imagem_vitoria = pyxel.Image(256, 256)
        self.imagem_vitoria.load(0, 0, "assets/vitoria.png")
        self.imagem_pause = pyxel.Image(256, 256)
        self.imagem_pause.load(0, 0, "assets/pause.png")

    def clicou(self, x1, y1, x2, y2):
        return (
            x1 <= pyxel.mouse_x <= x2
            and y1 <= pyxel.mouse_y <= y2
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        )

    def update(self):
        if self.state == "menu":
            if self.clicou(78, 129, 177, 148):
                self.state = "game"
            elif self.clicou(78, 159, 177, 178):
                self.state = "rules"
            elif self.clicou(78, 189, 177, 208):
                self.state = "options"
            elif self.clicou(78, 219, 177, 238):
                pyxel.quit()

        elif self.state in ("rules", "options"):
            if self.clicou(22, 222, 97, 232):
                self.state = "menu"

        elif self.state == "pause":
            if pyxel.btnp(pyxel.KEY_P):
                self.state = "game"

        elif self.state == "game_over":
            if self.clicou(11, 225, 93, 244):
                self.state = "menu"
            elif self.clicou(177, 225, 244, 244):
                pyxel.quit()

        elif self.state == "victory":
            if self.clicou(11, 225, 94, 244):
                self.state = "menu"
            elif self.clicou(154, 225, 246, 244):
                self.state = "infinite"

        elif self.state == "game":
            if pyxel.btnp(pyxel.KEY_P):
                self.state = "pause"

    def draw(self):
        if self.state == "menu":
            pyxel.blt(0, 0, self.imagem_menu, 0, 0, 256, 256)
        elif self.state == "rules":
            pyxel.blt(0, 0, self.imagem_regras, 0, 0, 256, 256)
            pyxel.text(24, 42, "DERROTE OS INIMIGOS DE CADA SALA.", 7)
            pyxel.text(24, 58, "ENCONTRE A CHAVE COM OS GUARDAS.", 7)
            pyxel.text(24, 74, "VENCA O BOSS PARA SUBIR DE ANDAR.", 7)
            pyxel.text(24, 90, "COMPLETE OS 5 ANDARES PARA VENCER.", 7)
            pyxel.text(24, 106, "ABRA BAUS PARA ENCONTRAR ITENS.", 7)
        elif self.state == "options":
            pyxel.blt(0, 0, self.imagem_controles, 0, 0, 256, 256)
            pyxel.text(24, 42, "WASD: MOVER", 7)
            pyxel.text(24, 58, "MOUSE / SETAS: MIRAR", 7)
            pyxel.text(24, 74, "SHIFT: DASH", 7)
            pyxel.text(24, 90, "CLIQUE / ESPACO: ATACAR", 7)
            pyxel.text(24, 106, "1: ESPADA  2: ESPADAO", 7)
            pyxel.text(24, 122, "3: MANOPLA / SOCO", 7)
            pyxel.text(24, 138, "E: INTERAGIR", 7)
            pyxel.text(24, 154, "P: PAUSAR", 7)
        elif self.state == "game_over":
            pyxel.blt(0, 0, self.imagem_game_over, 0, 0, 256, 256)
        elif self.state == "victory":
            pyxel.blt(0, 0, self.imagem_vitoria, 0, 0, 256, 256)
        elif self.state == "pause":
            pyxel.blt(0, 0, self.imagem_pause, 0, 0, 256, 256)
