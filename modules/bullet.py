#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: bullet.py
# Description: Level class for Supremacy
#####################################

import math
from constants import *
from modules.shiftable import ShiftableObject


class Bullet(ShiftableObject):

    def __init__(self, colour, x, y, top_speed, angle):
        """ (Surface, tuple, int, [int], [int]) -> None
        Instantiate a Bullet object with the given position, colour, and velocity components.
        """
        ShiftableObject.__init__(self, x, y)
        self.vx = int(top_speed * math.cos(math.radians(angle)))
        self.vy = int(top_speed * -math.sin(math.radians(angle)))
        self.colour = colour
        self.radius = 3
        self.rect = pygame.Rect(0, 0, self.radius, self.radius)
        self.damage = 50

    def update(self):
        """ (None) -> None
        Update the state of the Bullet object.
        """
        self.x += self.vx
        self.y += self.vy
        self.rect.center = self.x, self.y

    def draw(self, surface):
        """ (Surface) -> None
        Draw the bullet onto the given display Surface.
        """
        pygame.draw.circle(surface, self.colour, self.rect.center, self.radius)