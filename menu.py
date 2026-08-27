import pyxel

class Player:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color

class Wall:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        
class Game:
    def __init__(self):
        pyxel.init(256, 256)
        
        pyxel.mouse(True)
        
        self.state = "menu"

        self.player = Player(20, 20, 6, 3)
        self.wall = Wall(100, 102, 4, 200, 5)

        pyxel.run(self.update, self.draw)


    def update(self):
        if self.state == "menu":
            self.update_menu()

        elif self.state == "game":
            self.update_game()
            
        elif self.state == "rules":
            self.update_rules()
            
        elif self.state == "options":
            self.update_options()


    def draw(self):
        if self.state == "menu":
            self.draw_menu()

        elif self.state == "game":
            self.draw_game()
            
        elif self.state == "rules":
            self.draw_rules()
            
        elif self.state == "options":
            self.draw_options()
    def draw_menu_button(self, x, y, width, height, rect_color, text, text_color):

        pyxel.rect(x, y, width, height, rect_color)
        pyxel.rectb(x, y, width, height, 3)

        text_width = len(text) * 4

        text_x = x + (width - text_width) / 2
        text_y = y + (height - 6) / 2

        pyxel.text(text_x, text_y, text, text_color)
        
    def update_menu(self):
        if pyxel.mouse_x >= 78 and pyxel.mouse_x <= 178:
            if pyxel.mouse_y >= 130 and pyxel.mouse_y <= 150:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.state = "game"
                    
        if pyxel.mouse_x >= 78 and pyxel.mouse_x <= 178:
            if pyxel.mouse_y >= 160 and pyxel.mouse_y <= 180:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.state = "rules"
                    
        if pyxel.mouse_x >= 78 and pyxel.mouse_x <= 178:
            if pyxel.mouse_y >= 190 and pyxel.mouse_y <= 210:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.state = "options"
                    
        if pyxel.mouse_x >= 78 and pyxel.mouse_x <= 178:
            if pyxel.mouse_y >= 220 and pyxel.mouse_y <= 240:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    pyxel.quit()
    def draw_menu(self):
        pyxel.cls(0)
        pyxel.mouse(True)
        self.draw_menu_button(78, 130, 100, 20, 5, "PLAY GAME", 7)
        self.draw_menu_button(78, 160, 100, 20, 5, "RULES", 7)
        self.draw_menu_button(78, 190, 100, 20, 5, "OPTIONS", 7)
        self.draw_menu_button(78, 220, 100, 20, 5, "EXIT GAME", 7)
    
    def update_rules(self):
        pyxel.mouse(True)
        if pyxel.mouse_x >= 12 and pyxel.mouse_x <= 31:
            if pyxel.mouse_y >= 234 and pyxel.mouse_y <= 243:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.state = "menu"
        
    def update_options(self):
        pyxel.mouse(True)
        if pyxel.mouse_x >= 12 and pyxel.mouse_x <= 50:
            if pyxel.mouse_y >= 234 and pyxel.mouse_y <= 244:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.state = "menu"
        
    def draw_rules(self):
        pyxel.cls(0)
        pyxel.rect(8, 8, 240, 240, 3)
        pyxel.rect(10, 10, 236, 236, 5)
        pyxel.rectb(116, 12, 23, 9, 3)
        pyxel.text(118, 14, "RULES", 7)
        pyxel.rect(12, 234, 20, 10, 1)
        pyxel.text(14,236,"menu",7)
        
    def draw_options(self):
        pyxel.cls(0)
        pyxel.rectb(9, 9, 238, 238, 3)
        pyxel.rect(10, 10, 236, 236, 5)
        pyxel.rectb(112, 12, 31, 9, 3)
        pyxel.text(114, 14, "OPTIONS", 7)
        pyxel.rect(12, 234, 39, 10, 1)
        pyxel.text(14,236,"main menu",7)
    def update_game(self):
        pyxel.mouse(False)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player.x += 1
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player.x -= 1
        if pyxel.btn(pyxel.KEY_UP):
            self.player.y -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player.y += 1
        if pyxel.btn(pyxel.KEY_BACKSPACE):
            self.state = "menu"
            
    def draw_game(self):
        pyxel.cls(0)
        pyxel.rect(
            self.wall.x,
            self.wall.y,
            self.wall.width,
            self.wall.height,
            self.wall.color
        )

        pyxel.circ(
            self.player.x,
            self.player.y,
            self.player.radius,
            self.player.color
        )
Game()
