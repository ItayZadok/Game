from settings import *
import os
import pygame
from polygon import Polygon


class Cache:
    def __init__(self):
        self.stacked_sprite_cache = {}

    def generate_cache(self, name, layers):

        if name not in self.stacked_sprite_cache.keys():
            self.stacked_sprite_cache[name] = {}

        for i in range(NUM_ANGLES + 1):
            rotation = i * ANGLE_VALUE

            rotated_arr = [pygame.transform.rotate(img, rotation) for img in layers]
            polygon = Polygon(rotated_arr[0], (0, 0))

            self.stacked_sprite_cache[name][rotation] = (rotated_arr, polygon)

        return self.stacked_sprite_cache[name]
