import pygame
from utils import load_font

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, function, font_filename, allsprites, game_state, stage):
        pygame.sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state
        self.allsprites = allsprites
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclick_function = function
        self.color_text = (255,255,255)
        self.dark_bg_rgb = (140,140,140)
        self.light_bg_rgb = (170,170,170)
        self.font = load_font(font_filename, 30)
        self.stage = stage

        self.text = self.font.render(text , True , self.color_text)

        self._blit_buttons()
        
        self.image = self.dark_button
        self.pos = (self.x, self.y)
        self.rect = (self.pos, (self.width, self.height))
    
    stage = ""

    def update(self):
        if self.game_state.state == self.stage:
            self.rect = (self.pos, (self.width, self.height))
            if self._mouse_hover():
                self.image = self.light_button
            else:
                self.image = self.dark_button
        else:
            self.rect = ((-500, -500), (self.width, self.height))
    
    def setBg(self, color):
        self.dark_bg_rgb = color
        self._blit_buttons()
    
    def setLbg(self, color):
        self.light_bg_rgb = color
        self._blit_buttons()

    def set_text(self, t):
        print(f"new text: {t}")
        self.text = self.font.render(t , True , self.color_text)
        self._blit_buttons()

    def _blit_buttons(self, ):
        dark_button = pygame.Surface((self.width, self.height))
        dark_button.fill(self.dark_bg_rgb)
        dark_button.blit(self.text, (8, 8))
        self.dark_button = dark_button

        light_button = pygame.Surface((self.width, self.height))
        light_button.fill(self.light_bg_rgb)
        light_button.blit(self.text, (8, 8))
        self.light_button = light_button

    def _mouse_hover(self):
        mouse = pygame.mouse.get_pos()
        return (mouse[0] >= self.x and mouse[0] <= self.x + self.width and mouse[1] >= self.y and mouse[1] <= self.y + self.height)
        

    def check_click(self):
        if self._mouse_hover():
            self.onclick_function()
