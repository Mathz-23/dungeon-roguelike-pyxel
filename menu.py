import pyxel

class Menu:
    def __init__(self):
        pyxel.mouse(True)
        self.state = "menu"
        

    def update(self):
        if self.state == "menu":
            self.update_menu()

        elif self.state == "game":
            self.update_game()
            
        elif self.state == "rules":
            self.update_rules()
            
        elif self.state == "options":
            self.update_options()
            
        elif self.state == "pause":
            self.update_pause()
            
        elif self.state == "game_over":
            self.update_gameover()

    def draw(self):
        if self.state == "menu":
            self.draw_menu()

        elif self.state == "game":
            self.draw_game()
            
        elif self.state == "rules":
            self.draw_rules()
            
        elif self.state == "options":
            self.draw_options()
            
        elif self.state == "pause":
            self.draw_pause()
            
        elif self.state == "game_over":
            self.draw_gameover()
            
    def draw_button(self, x, y, width, height, rect_color, text, text_color):
    
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
        self.draw_button(78, 130, 100, 20, 5, "PLAY GAME", 7)
        self.draw_button(78, 160, 100, 20, 5, "RULES", 7)
        self.draw_button(78, 190, 100, 20, 5, "OPTIONS", 7)
        self.draw_button(78, 220, 100, 20, 5, "EXIT GAME", 7)
    
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
        
    def update_pause(self):
        if pyxel.btnp(pyxel.KEY_P):
            self.state = "game"
            
    def draw_pause(self):
        pyxel.cls(11)
        pyxel.rect(2, 2, 252, 252, 3)
        pyxel.text(110,10,"PAUSE",11)


    def update_gameover(self):
        pyxel.mouse(True)
        if pyxel.mouse_x >= 12 and pyxel.mouse_x <= 50:
            if pyxel.mouse_y >= 234 and pyxel.mouse_y <= 244:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    self.state = "menu"
                    
        if pyxel.mouse_x >= 204 and pyxel.mouse_x <= 242:
            if pyxel.mouse_y >= 234 and pyxel.mouse_y <= 244:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    pyxel.quit()
                    
    def draw_gameover(self):
        pyxel.cls(8)
        pyxel.rect(2, 2, 252, 252, 0)
        
        pyxel.text(110,10,"GAME OVER",8)
        pyxel.rect(12, 234, 39, 10, 8)
        pyxel.text(14,236,"main menu",0)

        pyxel.rect(204, 234, 39, 10, 8)
        pyxel.text(206,236,"quit game",0)
        
    def update_game(self):
        pyxel.mouse(False)
        
        if pyxel.btn(pyxel.KEY_BACKSPACE):
            self.state = "menu"
        if pyxel.btn(pyxel.KEY_Q):
            self.state = "game_over"
        if pyxel.btnp(pyxel.KEY_P):
            self.state = "pause"
            



