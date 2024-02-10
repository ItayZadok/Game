import pygame
import math
from stackedSprite import StackedSprite
from settings import *


def distance(pos1, pos2):
    """calculates the distance between two points"""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def line_line_collision(line1, line2):
    """Check if two lines represented by their start and end points intersect."""

    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0: return 0  # Collinear
        return 1 if val > 0 else 2  # Clockwise or counterclockwise

    def on_segment(p, q, r):
        return max(p[0], r[0]) >= q[0] >= min(p[0], r[0]) and \
               max(p[1], r[1]) >= q[1] >= min(p[1], r[1])

    p1, q1 = line1
    p2, q2 = line2

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    if o1 != o2 and o3 != o4:
        # Lines are intersecting, calculate the intersection point
        denominator = ((q1[1] - p1[1]) * (q2[0] - p2[0])) - ((q1[0] - p1[0]) * (q2[1] - p2[1]))
        if denominator == 0:
            # Lines are parallel or coincident, return None
            return None
        else:
            numerator1 = ((p1[0] - p2[0]) * (q2[1] - p2[1])) - ((p1[1] - p2[1]) * (q2[0] - p2[0]))
            t = numerator1 / denominator
            intersection_point = [p1[0] + (t * (q1[0] - p1[0])), p1[1] + (t * (q1[1] - p1[1]))]
            return intersection_point

    return None  # No intersection


def rect_line_collision(rect, line_pos):
    """calculate if a collision occurs between a rect and a line"""

    lines = [
        (rect.topleft, rect.topright),
        (rect.bottomleft, rect.bottomright),
        (rect.topright, rect.bottomright),
        (rect.topleft, rect.bottomleft),
    ]

    # instead of working with shitty built-in rect, we'll use our own!

    min_distance = 100000
    min_intersection = None

    for line in lines:
        intersection = line_line_collision(line_pos, line)

        if intersection is not None:
            d = distance(intersection, rect.center)
            if d < min_distance:
                min_distance = d
                min_intersection = intersection

    if min_intersection is not None:
        add = (rect.centerx - min_intersection[0], rect.centery - min_intersection[1])
        return rect.centerx + add[0], rect.centery + add[1]

    return None


class Player(StackedSprite):
    def __init__(self, name, pos, rotation, main, groups):
        super().__init__(name, pos, rotation, main, groups)
        self.borders = [[(100, 5), (50, 150)]]
        self.delta_time = main.delta_time
        self.main = main

        self.move_velocity = 0
        self.rotate_velocity = 0

        self.move_acceleration = 0.1
        self.rotate_acceleration = 0.1

        self.move_deceleration = 0.9
        self.rotate_deceleration = 0.9

        self.move_max_speed = 0.5
        self.rotate_max_speed = 0.5

        self.dire = pygame.math.Vector2(0, 0)

    def detection(self):
        keys = pygame.key.get_pressed()

        # reset
        self.dire.x = 0
        self.dire.y = 0

        if keys[pygame.K_RIGHT]:
            self.dire.x = -1
        if keys[pygame.K_LEFT]:
            self.dire.x = 1
        if keys[pygame.K_UP]:
            self.dire.y = -1
        if keys[pygame.K_DOWN]:
            self.dire.y = 1

    def collisions(self):
        rect_1 = self.rect.__copy__()
        rect_2 = self.rect.__copy__()
        rect_3 = self.rect.__copy__()
        rect_4 = self.rect.__copy__()

        d1 = 0
        d2 = 0
        d3 = 0
        d4 = 0

        for sprite in self.main.obstacle_sprites:
            if sprite is not self and sprite.rect.colliderect(self.rect):
                rect_1.right = sprite.rect.left
                d1 = distance(rect_1, self.rect)

                rect_2.left = sprite.rect.right
                d2 = distance(rect_2, self.rect)

                rect_3.bottom = sprite.rect.top
                d3 = distance(rect_3, self.rect)

                rect_4.top = sprite.rect.bottom
                d4 = distance(rect_4, self.rect)

                break

        d = min(d1, d2, d3, d4)

        if d == 0:
            return 0

        if d == d1:
            self.rect = rect_1
        elif d == d2:
            self.rect = rect_2
        elif d == d3:
            self.rect = rect_3
        else:
            self.rect = rect_4

        #  to see the rects
        '''
        surf = pygame.Surface((self.rect.width, self.rect.height))
        surf.fill('blue')
        self.main.display.blit(surf, rect_1)
        surf.fill('yellow')
        self.main.display.blit(surf, rect_2)
        surf.fill('green')
        self.main.display.blit(surf, rect_3)
        surf.fill('purple')
        self.main.display.blit(surf, rect_4)
        '''

        self.pos[0] = self.rect.centerx
        self.pos[1] = self.rect.centery

    def new_collision(self):
        for line in self.borders:
            pos = rect_line_collision(self.rect, line)
            if pos is not None:
                self.pos[0] = pos[0]
                self.pos[1] = pos[1]

    def update_movement_and_rotation(self, linear_input, rotational_input):

        # Update velocity based on acceleration
        self.move_velocity += linear_input * self.move_acceleration * PLAYER_MOVEMENT_SPEED
        self.rotate_velocity += rotational_input * self.rotate_acceleration * PLAYER_ROTATE_SPEED

        # Cap the velocity to the maximum speed
        self.move_velocity = min(self.move_velocity, self.move_max_speed)
        self.rotate_velocity = min(self.rotate_velocity, self.rotate_max_speed)

        self.rotation += self.rotate_velocity * self.delta_time

        radians = math.radians(self.rotation)
        dist = self.move_velocity * self.delta_time

        self.pos[0] += dist * math.sin(radians)
        self.pos[1] += dist * math.cos(radians)

        # self.collisions()  # very inefficient

        self.new_collision()
        self.rect.center = self.pos

        # Apply friction
        self.move_velocity *= self.move_deceleration
        self.rotate_velocity *= self.rotate_deceleration

    def update(self):
        self.delta_time = self.main.delta_time
        self.detection()
        self.update_movement_and_rotation(self.dire.y, self.dire.x)
