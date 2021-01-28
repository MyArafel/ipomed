import pygame
from utils import load_image

class QuickSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, game_state, file, sprites, stage):
        pygame.sprite.Sprite.__init__(self, sprites)
        self.image, self.rect = load_image(file, 1)
        self.game_state = game_state
        self.stage = stage
        self.pos = (x, y)
        self.w = w
        self.h = h
        self.allsprites = sprites

    def update(self):
        if self.game_state.state == self.stage:
            self.rect = (self.pos, (self.w, self.h))
        else:
            self.rect = ((-500, -500), (self.w, self.h))

