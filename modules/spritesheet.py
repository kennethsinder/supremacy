#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: spritesheet.py
# Description: Spritesheet class
#####################################
from math import ceil, floor
from data_loader import *


class Spritesheet(object):

    def __init__(self, filename, num_in_row, num_in_col):
        """ (str, int, int) -> Spritesheet
        Instantiate a spritesheet object with the given filename, width, height,
        number of images per row, and number of images per column.
        """
        self.image = load_image(filename)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.num_in_row = num_in_row
        self.num_in_column = num_in_col
        self.frames = [self.get_frame(i) for i in range(self.num_in_row * self.num_in_column)]
        self.optimize_images()

    def __imul__(self, other):
        self.scale(float(other))
        return self

    def __getitem__(self, index):
        return self.frames[index]

    def add(self, image):
        """ (Surface) -> None
        Add the given image Surface to the list of loaded Spritesheet frames.
        Does not save image to disk.
        """
        self.frames.append(image)

    def add_mirrors(self, index):
        """ (int) -> list
        Add the horizontally and vertical versions of the given
        image index to the list of loaded Spritesheet frames.
        Return the indices of the new images as a list.
        """
        result = []
        for angle in range(0, 360, 90):
            self.add(pygame.transform.rotate(self.frames[index], angle))
            result.append(len(self.frames) - 1)
        return result

    def optimize_images(self):
        """ (None) -> None
        Remove transparent edges at each side of each frame in order to optimize them for blitting.
        """
        new_frames = []
        for image in self.frames:
            new_frames.append(image.subsurface(image.get_bounding_rect()))
        self.frames = new_frames

    def get_frame(self, i):
        """ (int) -> Surface
        Return a Surface object representing the ith index of images in the Spritesheet.
        """
        w = float(self.width) / self.num_in_row
        h = float(self.height) / self.num_in_column
        x = (i % self.num_in_row) * w
        y = (i // self.num_in_row) * h
        return self.image.subsurface(pygame.Rect(int(x), int(y), int(w), int(h)))

    def scale(self, factor):
        """ (float) -> None
        Resize the entire spritesheet image by the given factor (factor > 0.0).
        """
        w = float(self.width) / self.num_in_row
        h = float(self.height) / self.num_in_column
        for i in range(len(self.frames)):
            self.frames[i] = pygame.transform.scale(self.frames[i], (int(w * factor), int(h * factor)))