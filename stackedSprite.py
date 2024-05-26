import math

from settings import *
from polygon import Polygon
import os


class StackedSprite(pygame.sprite.Sprite):
    def __init__(self, name, pos, rotation, main, groups):
        super().__init__(groups)
        self.rotation = rotation
        self.main = main
        self.pos = pos
        self.name = name

        self.layers = [pygame.image.load('graphics/' + name + '/' + img) for img in os.listdir('graphics/' + name)]
        self.rect = Polygon(self.layers[2], self.pos)

    def drawOn(self, surf, pos, spread=1):

        fixed_rotation = (self.rotation // ANGLE_VALUE) * ANGLE_VALUE

        self.rect.set_rotation(fixed_rotation)

        # to see the rect
        #self.rect.draw(self.main.display, 'red', pos)

        if self.layers is not None:
            for i, img in enumerate(self.layers):
                rotated_img = pygame.transform.rotate(img, fixed_rotation)

                surf.blit(rotated_img,
                          (pos[0] - rotated_img.get_width() // 2,
                           pos[1] - rotated_img.get_height() // 2 - i * spread))
