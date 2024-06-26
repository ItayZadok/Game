import pygame

RES = WIDTH, HEIGHT = (750, 750)
P_RES = P_WIDTH, P_HEIGHT = (250, 250)

BG_COLOR = 'azure3'#  'olivedrab'
FPS = 60

PLAYER_MOVEMENT_SPEED = 0.2
PLAYER_ROTATE_SPEED = 0.15
NUM_ANGLES = 45
ANGLE_VALUE = (360 // NUM_ANGLES)


LEVEL_BORDERS = [
    [[0, 0], [512, 0]],
    [[0, 0], [0, 512]],
    [[512, 0], [512, 512]],
    [[0, 512], [512, 512]],
    [[112, 399], [399, 399]],
    [[399, 112], [399, 399]],
    [[112, 399], [112, 112]],
    [[112, 112], [207, 112]],
    [[399, 112], [304, 112]],
    [[207, 112], [207, 143]],
    [[304, 112], [304, 143]],
    [[368, 143], [368, 368]],
    [[143, 368], [368, 368]],
    [[143, 368], [143, 143]],
    [[207, 143], [143, 143]],
    [[368, 143], [304, 143]],
]