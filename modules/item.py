#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: item.py
# Description: Classes for level items
#####################################

from constants import *
from data_loader import *
from modules.shiftable import ShiftableObject


class Item(ShiftableObject):

    def __init__(self, image, x=0, y=0, itemtype='food'):
        """ (str, [int], [int], [str]) -> Item
        Instantiate an Item object with the given picture path and co-ordinates.
        """
        ShiftableObject.__init__(self, x, y)
        self.type = str(itemtype)
        self.image = load_image(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.visible = True
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def destroy(self):
        """ (None) -> None
        Render the item invisible and unusable.
        """
        self.visible = False

    def is_alive(self):
        """ (None) -> bool
        Return True if the item is visible, False otherwise.
        """
        return self.visible

    def update(self):
        """ (None) -> None
        Update the state of the Item.
        """
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface):
        """ (Surface) -> None
        Draw the Item onto the given Surface.
        """
        if self.visible:
            surface.blit(self.image, (self.x, self.y))