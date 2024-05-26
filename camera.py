import math
import pygame
from player import distance
from polygon import Polygon
from settings import *

class Camera:
    def __init__(self, main):
        self.main = main

        self.screen = main.screen
        self.pixel_display = main.display
        self.visible_sprites = self.main.visible_sprites

        self.offset = pygame.math.Vector2()
        self.player = self.main.player
        self.background = self.main.level

    def center_target_camera(self):
        self.offset.x = self.player.pos[0] - P_WIDTH//2
        self.offset.y = self.player.pos[1] - P_HEIGHT//2

    # individually draw a sprite
    def draw(self, sprite):
        sprite.drawOn(self.pixel_display, self.offset)

    def custom_draw(self):

        self.center_target_camera()

        self.background.drawOn(self.pixel_display, self.offset)
        self.player.drawOn(self.pixel_display, self.player.pos-self.offset, 0.5)

        '''
        for line in LEVEL_BORDERS:
            new_line = [line[0] - self.offset, line[1] - self.offset]
            pygame.draw.line(self.main.display, 'cyan', new_line[0], new_line[1], 1)
        '''

        scaled = pygame.transform.scale(self.pixel_display, (WIDTH*1.4, HEIGHT*1.4))
        rotated = pygame.transform.rotate(scaled, 360-self.player.rotation)


        r = rotated.get_rect(center=(WIDTH//2, HEIGHT//2))

        self.screen.blit(rotated, r)
