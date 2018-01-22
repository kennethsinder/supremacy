#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: constants.py
# Description: Module that contains useful constants
#               to import into the local namespace
#####################################

import pygame, math
from pygame.locals import *

# ----- Game -----
TITLE = 'supremacy'
PROGRAMMER = 'Kenneth Sinder'
SHORT_DESCR = 'WASD movement controls. Mouse buttons to aim and shoot. Keep hunger below 10. Survive.'

# ----- Directions -----
RIGHT = 0
UP = 1
LEFT = 2
DOWN = 3
STOP = 4

# ----- Colours -----
BLACK = 0, 0, 0
WHITE = 255, 255, 255
RED = 255, 0, 0
GREEN = 0, 255, 0
BLUE = 0, 0, 255
YELLOW = 255, 255, 0

# ----- FPS -----
SLOW_FPS = 30
SMOOTH_FPS = 60
UNL_FPS = 1000

# ---- Fonts -----
SLEEK = 'weblysleekuil.ttf'
DIGITAL = 'DigitalDream.ttf'

# ----- Other -----
LAST_LEVEL = 4
HUNGER_LIMIT = 10
