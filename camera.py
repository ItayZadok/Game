import math

import pygame
from settings import *


class Camera:
    def __init__(self, main):
        self.main = main

        self.screen = main.screen
        self.pixel_display = main.display
        self.visible_sprites = self.main.visible_sprites

        self.half_width = P_WIDTH // 2
        self.half_height = P_HEIGHT // 2
        self.offset = pygame.math.Vector2()

        self.camera_borders = {'left': 40, 'right': 40, 'top': 40, 'bottom': 40}
        l = self.camera_borders['left']
        t = self.camera_borders['top']
        w = self.pixel_display.get_size()[0] - (self.camera_borders['left'] + self.camera_borders['right'])
        h = self.pixel_display.get_size()[1] - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(l, t, w, h)

    def box_target_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    # individually draw a sprite
    def draw(self, sprite):
        offset_pos = sprite.rect.center - self.offset
        sprite.drawOn(self.pixel_display, offset_pos)

    # draw all the group
    def custom_draw(self, target):

        self.box_target_camera(target)

        for sprite in sorted(self.visible_sprites.sprites(), key=lambda s: s.rect.centery):
            if math.sqrt((sprite.rect.centerx - target.rect.centerx) ** 2 + (
                    sprite.rect.centery - target.rect.centery) ** 2) < P_WIDTH // TILE_SIZE:
                offset_pos = sprite.rect.center - self.offset
                sprite.drawOn(self.pixel_display, offset_pos)

        rect = self.camera_rect.__copy__()
        rect.center -= self.offset

        pygame.draw.rect(self.pixel_display, 'yellow', rect, 5)

        for line in self.main.player.borders:
            line = [line[0]-self.offset, line[1]-self.offset]
            pygame.draw.line(self.main.display, 'cyan', line[0], line[1], 1)

        rect = self.main.player.rect.__copy__()
        rect.center -= self.offset

        pygame.draw.rect(self.main.display, 'blue', rect, 1)

        self.screen.blit(pygame.transform.scale(self.pixel_display, RES), (0, 0))

