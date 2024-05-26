import pygame
import math

from polygon import Polygon
from stackedSprite import StackedSprite
from settings import *


def distance(pos1, pos2):
    """calculates the distance between two points"""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


class Player(StackedSprite):
    def __init__(self, name, pos, rotation, main, groups):
        super().__init__(name, pos, rotation, main, groups)
        self.delta_time = main.delta_time
        self.main = main

        self.borders = LEVEL_BORDERS

        self.move_velocity = 0
        self.rotate_velocity = 0

        self.move_acceleration = 0.1
        self.rotate_acceleration = 0.1

        self.move_deceleration = 0.9
        self.rotate_deceleration = 0.9

        self.move_max_speed = 0.5
        self.rotate_max_speed = 0.5

        self.dire = pygame.math.Vector2(0, 0)
        self.rotation_offset = 0
    def detection(self):
        keys = pygame.key.get_pressed()

        # reset
        self.dire.x = 0
        self.dire.y = 0

        if keys[pygame.K_RIGHT]:
            self.dire.x = 1
        if keys[pygame.K_LEFT]:
            self.dire.x = -1
        if keys[pygame.K_UP]:
            self.dire.y = -1
        if keys[pygame.K_DOWN]:
            self.dire.y = 1

    def collision(self):

        for line in self.borders:

            line_start = line[0]
            line_end = line[1]
            player_position = self.pos

            line_vector = (line_end[0] - line_start[0], line_end[1] - line_start[1])

            # Calculate vector from line start to player
            player_to_start_vector = (player_position[0] - line_start[0], player_position[1] - line_start[1])

            # Calculate dot product of the line vector and player-to-start vector
            dot_product = line_vector[0] * player_to_start_vector[0] + line_vector[1] * player_to_start_vector[1]

            # Calculate squared length of the line vector
            line_length_squared = line_vector[0] ** 2 + line_vector[1] ** 2

            # Calculate the parameter t for the projection of player_to_start_vector onto line_vector
            t = max(0, min(1, dot_product / line_length_squared))

            # Calculate the closest point on the line to the player
            closest_point_on_line = (line_start[0] + t * line_vector[0], line_start[1] + t * line_vector[1])

            # Calculate the vector from the closest point on the line to the player
            closest_point_to_player_vector = (player_position[0] - closest_point_on_line[0],
                                              player_position[1] - closest_point_on_line[1])

            # Calculate the distance from the player to the closest point on the line
            distance_to_line = (closest_point_to_player_vector[0] ** 2 + closest_point_to_player_vector[1] ** 2) ** 0.5

            # If player is colliding with the line, move the player away from the line
            if distance_to_line < 9:  # Adjust this threshold as needed
                # Calculate the direction vector from the line to the player
                move_direction = (player_position[0] - closest_point_on_line[0],
                                  player_position[1] - closest_point_on_line[1])

                # Normalize the move direction vector
                move_direction_length = (move_direction[0] ** 2 + move_direction[1] ** 2) ** 0.5
                move_direction = (move_direction[0] / move_direction_length,
                                  move_direction[1] / move_direction_length)

                # Move the player along the move direction to avoid collision
                player_position = (
                closest_point_on_line[0] + move_direction[0] * 9,  # Adjust this movement distance as needed
                closest_point_on_line[1] + move_direction[1] * 9)

            self.pos[0] = player_position[0]
            self.pos[1] = player_position[1]

    def update_movement_and_rotation(self, linear_input, rotational_input):

        # Update velocity based on acceleration
        self.move_velocity += linear_input * self.move_acceleration * PLAYER_MOVEMENT_SPEED
        self.rotate_velocity += rotational_input * self.rotate_acceleration * PLAYER_ROTATE_SPEED

        # Cap the velocity to the maximum speed
        self.move_velocity = min(self.move_velocity, self.move_max_speed)
        self.rotate_velocity = min(self.rotate_velocity, self.rotate_max_speed)

        self.rotation += 360-self.rotate_velocity * self.delta_time
        self.rotation %= 360

        fixed_rotation = (self.rotation // ANGLE_VALUE) * ANGLE_VALUE

        radians = math.radians(fixed_rotation)
        dist = self.move_velocity * self.delta_time

        self.pos[0] += dist * math.sin(radians)
        self.pos[1] += dist * math.cos(radians)

        self.collision() # very not perfect
        self.rect.set_position(self.pos)

        # Apply friction
        self.move_velocity *= self.move_deceleration
        self.rotate_velocity *= self.rotate_deceleration

    def update(self):
        self.delta_time = self.main.delta_time
        self.detection()
        self.update_movement_and_rotation(self.dire.y, self.dire.x)
