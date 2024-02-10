from settings import *
import os


class StackedSprite(pygame.sprite.Sprite):
    def __init__(self, name, pos, rotation, main, groups):
        super().__init__(groups)
        self.rotation = rotation
        self.main = main
        self.pos = pos
        self.name = name

        self.layers = [pygame.image.load('graphics/' + name + '/' + img) for img in os.listdir('graphics/' + name)]
        self.cache = main.cache.generate_cache(name, self.layers)
        self.rect = self.layers[0].get_rect(center=self.pos)

    def drawOn(self, surf, offset_pos, spread=1):

        self.rotation %= 360

        fixed_rotation = (self.rotation // ANGLE_VALUE) * ANGLE_VALUE

        #  to see the rect
        '''
        surf2 = pygame.Surface((self.rect.width, self.rect.height))
        surf2.fill('red')
        self.main.display.blit(surf2, (self.rect.x, self.rect.y))
        '''

        # update rect size
        self.rect = self.cache[fixed_rotation][0].get_rect(center=self.pos)  # self.pos in purpose!!! cuz camera only changes look not actual physics

        if self.layers is not None:
            for i, rotated_img in enumerate(self.cache[fixed_rotation]):
                surf.blit(rotated_img,
                          (offset_pos[0] - rotated_img.get_width() // 2,
                           offset_pos[1] - rotated_img.get_height() // 2 - i * spread))
