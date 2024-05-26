import os
import sys

import pygame.image

from camera import Camera
from player import Player
from settings import *
from cache import Cache
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

        self.obstacle_sprites = pygame.sprite.Group()
        self.visible_sprites = pygame.sprite.Group()
        self.clock = pygame.time.Clock()

        img = pygame.image.load('graphics/levels/level3.png')
        pos = [img.get_size()[0]//2, img.get_size()[1]//2]

        self.level = Sprite(pos, img)
        self.player = Player('car2', [pos[0], pos[1]], 0, self, self.obstacle_sprites) # why is it all by reference?!

        self.camera = Camera(self)

    def draw(self):
        self.player.update()
        self.camera.custom_draw()

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
