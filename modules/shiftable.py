#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: shiftable.py
# Description: Base class for moveable objects that can be shifted
#####################################

class ShiftableObject(object):

    def __init__(self, x=0, y=0):
        """ ([int], [int]) -> ShiftableObject
        Instantiate a shiftable level object with the given co-ordinates.
        Subclasses must define self.rect as a pygame Rect object.
        """
        self.x = x
        self.y = y
        self.rect = None

    def shift(self, dx=1, dy=1):
        """ ([int], [int]) -> None
        Increment the on-screen position dx pixels right and dy pixels down.
        """
        self.x += dx
        self.y += dy
        self.rect.move_ip(dx, dy)

    def collides_with(self, other):
        """ (Rect-or-tuple-or-list) -> bool
        Return True if the given object collides with self, False otherwise.
        """
        if isinstance(other, tuple):
            return self.rect.collidepoint(other)
        elif isinstance(other, list):
            return self.rect.collidelist(other) != -1
        else:
            try:
                return self.rect.colliderect(other.rect)
            except TypeError:
                return self.rect.colliderect(other)

    def get_rect(self):
        """ (None) -> Rect
        Return a pygame Rect object representing the boundaries of the shiftable object.
        """
        return self.rect

    def update(self):
        """ (None) -> None
        Update the state of the shiftable object.
        """
        pass