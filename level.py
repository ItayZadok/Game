from settings import *
from stackedSprite import StackedSprite
from player import Player
from sprite import Sprite


class Level:
    def __init__(self, main):
        self.main = main
        self.create_map()

    def create_map(self):
        for row_index, row in enumerate(WORLD_MAP):
            for col_index, tile in enumerate(row):
                x = col_index * TILE_SIZE + TILE_SIZE // 2
                y = row_index * TILE_SIZE + TILE_SIZE // 2
                if tile == 'b':
                    Sprite([x, y], self.main.obstacle_sprites)
                if tile == 'p':
                    self.main.player = Player('car2', [x, y], 0, self.main, (self.main.obstacle_sprites, self.main.visible_sprites))
