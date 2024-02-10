import pygame


class Polygon:
    def __init__(self, points, pos):
        self.points = points
        self.position = pos

    def set_points_by_rect(self, rect):
        top_left = rect.topleft
        top_right = rect.topright
        bottom_left = rect.bottomleft
        bottom_right = rect.bottomright

        self.points = [top_left, top_right, bottom_right, bottom_left]

    def draw(self, surface):
        pygame.draw.polygon(surface, self.points)

    def set_position(self, x, y):
        self.position = (x, y)

        offset = (self.position[0] - self.get_center()[0], self.position[1] - self.get_center()[1])
        self.points = [(point[0] + offset[0], point[1] + offset[1]) for point in self.points]

    def get_center(self):
        # Calculate the centroid of the polygon
        total_x = sum(point[0] for point in self.points)
        total_y = sum(point[1] for point in self.points)
        centroid_x = total_x / len(self.points)
        centroid_y = total_y / len(self.points)
        return centroid_x, centroid_y
