#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: ending.py
# Description: Lock and key classes (which lead to level endings)
#####################################

from data_loader import *
from constants import *
from modules.shiftable import ShiftableObject

class Lock(ShiftableObject):

    def __init__(self, x, y, image):
        """ (int, int, Surface) -> Lock
        Instantiate a new Lock object.
        """
        ShiftableObject.__init__(self, x, y)
        self.image = load_image(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.locked = True

    def lock(self):
        """ (None) -> None
        Ensure that the lock is in a locked (unusable) state.
        """
        self.locked = True

    def unlock(self):
        """ (None) -> None
        Ensure that the lock is in an unlocked (usable) state.
        """
        self.locked = False

    def draw(self, surface):
        """ (Surface) -> None
        Draw the lock onto the given display Surface.
        """
        surface.blit(self.image, self.rect)


class Key(ShiftableObject):

    def __init__(self, x, y, image):
        """ (int, int, Surface) -> Lock
        Instantiate a new Key object.
        """
        ShiftableObject.__init__(self, x, y)
        self.image = load_image(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.visible = True

    def draw(self, surface):
        """ (Surface) -> None
        Draw the key onto the given display Surface.
        """
        if self.visible:
            surface.blit(self.image, self.rect)