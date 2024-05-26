import math

import pygame.math

from settings import *
from polygon import Polygon
import math


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, image, groups=None, rotation=0):
        if groups is not None:
            super().__init__(groups)

        self.rotation = rotation
        self.image = image
        self.rect = Polygon(self.image, pos, None, rotation)

        self.pos_change = pygame.math.Vector2(0, 0)

    def drawOn(self, surf, offset):

        offset_pos = self.rect.pos - offset

        surf.blit(self.image,
                  (offset_pos[0] - self.image.get_width() // 2,
                   offset_pos[1] - self.image.get_height() // 2))

