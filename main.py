import os
import sys

from camera import Camera
from settings import *
from cache import Cache
from level import Level
from sprite import Sprite


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(RES, 0, 32)
        self.display = pygame.Surface(P_RES)
        self.delta_time = 0.01

        self.player = None  # for auto-completion
        self.cache = Cache()
        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.camera = Camera(self)
        self.clock = pygame.time.Clock()
        self.level = Level(self)

        self.cur_level = Sprite((0, 0), None, 'levels/level' + '3')

    def draw(self):

        self.player.update()

        self.camera.draw(self.cur_level)
        self.camera.custom_draw(self.player)

        self.display.fill(BG_COLOR)

    def update(self):

        pygame.display.update()
        self.delta_time = self.clock.tick()
        pygame.display.set_caption(f'{self.clock.get_fps(): .1f}')

    def run(self):
        while True:
            handle_events()
            self.draw()
            self.update()


if __name__ == '__main__':
    game = Game()
    game.run()
