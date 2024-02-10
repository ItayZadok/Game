from settings import *
import os
import pygame


def get_rotation_arr(images, rotation):
    return [pygame.transform.rotate(img, rotation) for img in images]


class Cache:
    def __init__(self):
        self.stacked_sprite_cache = {}

    def generate_cache(self, name, layers):

        if name not in self.stacked_sprite_cache.keys():
            self.stacked_sprite_cache[name] = {}

        for i in range(NUM_ANGLES + 1):
            rotation = i * ANGLE_VALUE
            self.stacked_sprite_cache[name][rotation] = get_rotation_arr(layers, rotation)

        return self.stacked_sprite_cache[name]
