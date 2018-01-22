#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: gui.py
# Description: Classes for the Rogueline GUI
#####################################

from data_loader import *
from constants import *
from random import randint


class Button(object):
    """ Sleek, Pygame-based button control. """

    on_colour = YELLOW
    off_colour = WHITE

    def __init__(self, text='', x=0, y=0, size=48):
        """ ([str], [int], [int], [int], [tuple]) -> Button
        Instantiate a Button object with the given size, text and center co-ordinates.
        """
        # ----- caption and co-ordinates -----
        self.x = x
        self.y = y
        self.text = str(text)

        # ----- other properties -----
        self.font = load_font(SLEEK, size)
        self.text_surface_on = self.font.render(self.text, 1, self.on_colour)
        self.text_surface_off = self.font.render(self.text, 1, self.off_colour)
        self.text_rect = self.text_surface_on.get_rect()
        self.text_rect.center = x, y
        self.hovering = False

    def pressed(self):
        """ (None) -> bool
        Return True if the mouse clicked the button, False otherwise. """
        return pygame.mouse.get_pressed()[0] and self.hovering

    def update(self):
        """ (None) -> None
        Update the state of the Button. Call on every iteration of the game loop.
        """
        if self.x > 2000 or self.y > 2000: return
        self.hovering = self.text_rect.collidepoint(pygame.mouse.get_pos())

    def draw(self, surface):
        """ (Surface) -> None
        Draw the Button onto the given Surface object.
        """
        if self.hovering:
            surface.blit(self.text_surface_on, self.text_rect)
        else:
            surface.blit(self.text_surface_off, self.text_rect)


class Stripe(object):
    """ Vertical or horizontal stripe. """

    def __init__(self, x, y, thickness=50, vertical=True):
        """ (int, int, [int], [bool]) -> Stripe
        Instantiate a Stripe object with the given co-ordinates and thickness.
        """
        # ----- parameter-based properties -----
        self.x = x
        self.y = y
        self.thickness = thickness
        self.vertical = vertical
        
        # ----- get random colour and length -----
        self.colour = [randint(70, 255), randint(70, 255), randint(70, 255)]
        self.length = randint(50, 100)

    def update(self):
        """ (None) -> None
        Lengthen the Stripe as necessary to provide a growing effect. Call on every game update.
        """
        if self.x < 2000 and self.y < 2000:
            self.length += 2

    def draw(self, surface):
        """ (None) -> None
        Draw the Stripe onto the given Surface object.
        """
        if self.vertical:
            pygame.draw.line(surface, self.colour, (self.x, self.y),
                             (self.x, self.y + self.length), self.thickness)
        else:
            pygame.draw.line(surface, self.colour, (self.x, self.y),
                             (self.x + self.length, self.y), self.thickness)