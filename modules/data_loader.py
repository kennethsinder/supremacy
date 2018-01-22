#####################################
# Programmer: Kenneth Sinder
# Date:
# Filename: data_loader.py
# Description: Basic image, font, and sound loader module
#####################################

import pygame, os

def _get_filepath(folder, filename):
    """ (str, str) -> str
    Return the exact path of the given filename in the given data folder.
    """
    root = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root, folder, filename)

def load_image(filename, transparency=True):
    """ (str, [bool]) -> Surface
    Return a pygame Surface object representing an image with the given filename.
    """
    if isinstance(filename, str):
        result = pygame.image.load(_get_filepath('images', filename))
    else:
        result = filename
    if transparency:
        return result.convert_alpha()
    return result.convert()

def load_sound(filename):
    """ (str) -> Sound
    Return a new Sound object based on the given filename.
    """
    return pygame.mixer.Sound(_get_filepath('sounds', filename))

def load_font(filename, size):
    """ (str) -> Font
    Return a new Font object based on the given size and filename.
    """
    return pygame.font.Font(_get_filepath('fonts', filename), size)

def get_music_path(filename):
    """ (str) -> str
    Return the exact path of music with the given filename. Does not play music.
    """
    return _get_filepath('sounds', filename)
