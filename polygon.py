import math

import pygame
from settings import *
import numpy as np


def get_borders(image):
    surface = pygame.Surface(image.get_size(), pygame.SRCALPHA)
    surface.blit(image, (0, 0))

    width, height = surface.get_size()

    # Get the coordinates of opaque pixels
    opaque_pixels = [(x, y) for x in range(width) for y in range(height) if surface.get_at((x, y))[3] != 0]

    if len(opaque_pixels) == 0:
        return []

    # Sort the opaque pixels by their x-coordinate (and then by their y-coordinate for tie-breaking)
    sorted_pixels = sorted(opaque_pixels, key=lambda point: (point[0], point[1]))

    # Compute the convex hull using Graham's scan algorithm
    def convex_hull(points):
        def cross_product(p1, p2, p3):
            return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

        # Build lower hull
        lower_hull = []
        for point in points:
            while len(lower_hull) >= 2 and cross_product(lower_hull[-2], lower_hull[-1], point) <= 0:
                lower_hull.pop()
            lower_hull.append(point)

        # Build upper hull
        upper_hull = []
        for point in reversed(points):
            while len(upper_hull) >= 2 and cross_product(upper_hull[-2], upper_hull[-1], point) <= 0:
                upper_hull.pop()
            upper_hull.append(point)

        return lower_hull[:-1] + upper_hull[:-1]

    convex_hull_points = convex_hull(sorted_pixels)

    return convex_hull_points


class Polygon:
    def __init__(self, image=None, pos=None, points=None, rotation=None):

        if image is None:
            self.points = points
            self.pos = pos
        elif image is not None:
            self.set_from_image(image, pos)

        if rotation is not None:
            self.rotation = rotation
            self.set_rotation(rotation)
        else:
            self.rotation = 0

    def draw(self, surface, color, pos=None, border_size=1):
        if pos is None:
            pygame.draw.polygon(surface, color, self.points, 1)
        else:
            offset = (pos[0] - self.get_center()[0], pos[1] - self.get_center()[1])
            points = [(point[0] + offset[0], point[1] + offset[1]) for point in self.points]
            pygame.draw.polygon(surface, color, points, border_size)

    def set_rotation(self, rotation):

        angle_radians = math.radians(self.rotation-rotation)  # because the method rotates it and not sets it
        pivot = self.get_center()

        points = []

        for point in self.points:

            # Translate pivot to origin
            translated_point = (point[0] - pivot[0], point[1] - pivot[1])

            # Perform rotation
            rotated_x = translated_point[0] * math.cos(angle_radians) - translated_point[1] * math.sin(angle_radians)
            rotated_y = translated_point[0] * math.sin(angle_radians) + translated_point[1] * math.cos(angle_radians)

            # Translate back to original position
            points.append((rotated_x + pivot[0], rotated_y + pivot[1]))

        self.points = points
        self.rotation = rotation

    def set_from_image(self, image, pos):
        self.points = get_borders(image)
        self.set_position(pos)

    def set_position(self, pos):
        self.pos = pos

        offset = (self.pos[0] - self.get_center()[0], self.pos[1] - self.get_center()[1])
        self.points = [(point[0] + offset[0], point[1] + offset[1]) for point in self.points]

    def get_center(self):
        # Calculate the centroid of the polygon
        total_x = sum(point[0] for point in self.points)
        total_y = sum(point[1] for point in self.points)
        centroid_x = total_x / len(self.points)
        centroid_y = total_y / len(self.points)
        return centroid_x, centroid_y
