from settings import *


class Sprite(pygame.sprite.Sprite):
    def __init__(self, pos, groups=None, name=None):

        if groups is not None:
            super().__init__(groups)

        if name is None:
            self.rect = pygame.Rect(0, 0, TILE_SIZE, TILE_SIZE)
            self.rect.center = pos
        else:
            self.image = pygame.image.load('graphics/' + name + '.png')
            self.rect = self.image.get_rect(center=pos)

    def drawOn(self, surf, offset_pos):
        surf.blit(self.image, offset_pos)

