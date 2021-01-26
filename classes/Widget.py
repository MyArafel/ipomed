import pygame
from utils import load_font

class Widget(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, text, font_filename, allsprites, game_state, stage):
        pygame.sprite.Sprite.__init__(self, allsprites)
        self.game_state = game_state
        self.allsprites = allsprites
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color_text = (255,255,255)
        self.dark_bg_rgb = (140,140,140)
        self.font = load_font(font_filename, 30)
        self.stage = stage

        self.text = self.font.render(text, True, self.color_text)

        dark_widget = pygame.Surface((self.width, self.height))
        dark_widget.fill(self.dark_bg_rgb)
        dark_widget.blit(self.text, (8, 8))

        self.dark_widget = dark_widget
        self.image = self.dark_widget
        self.pos = (self.x, self.y)
        self.rect = (self.pos, (self.width, self.height))

    def update(self):
        if self.game_state.state == self.stage:
            self.rect = (self.pos, (self.width, self.height))
        else:
            self.rect = ((-500, -500), (self.width, self.height))
    
    def setText(self, text):
        self.text = self.font.render(text, True, self.color_text)
        dark_widget = pygame.Surface((self.width, self.height))
        dark_widget.fill(self.dark_bg_rgb)
        dark_widget.blit(self.text, (8, 8))
        self.dark_widget = dark_widget
        self.image = self.dark_widget



