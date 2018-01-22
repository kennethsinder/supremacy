#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: character.py
# Description: Character classes for the Supremacy game
#####################################

import math
from constants import *
from data_loader import *
from modules.shiftable import ShiftableObject


class Character(ShiftableObject):
    """ Generic, rotatable game character. """

    def __init__(self, x, y, speed, *images):
        """ (str, int, int, [int], [int], [int]) -> Character
        Instantiate a Pygame-based generic character with the given properties.
        Expects all images to be facing-up by default.
        """
        ShiftableObject.__init__(self, x, y)
        self.top_speed = speed
        self.images_l, self.images_r, self.images_d, self.images_u = [], [], [], []
        self.rotate_images(images)

        self.health = 100
        self.damage = 1             # Damage to other characters
        self.hunger = 0
        self.vx = 0
        self.vy = 0
        self.image_counter = 0
        self.angle = 0
        self.aiming = False
        self.current_images = self.images_d
        self.possible_directions = []
        self.rect = self.get_rect()
        self.original_rect = self.rect.copy()

        self.text_font = load_font(SLEEK, 28)

    def normalize(self):
        """ (None) -> None
        Ensure that the velocity vector has the magnitude top_speed.
        """
        magnitude = math.sqrt(self.vx ** 2 + self.vy ** 2)
        if magnitude == 0: return
        self.vx /= magnitude / float(self.top_speed)
        self.vy /= magnitude / float(self.top_speed)
        self.vx = int(self.vx)
        self.vy = int(self.vy)

    def rotate(self, x=0, y=0):
        """ ([int], [int]) -> None
        Determine the angle based on the direction of the position vector and
        the given co-ordinate.
        """
        dx = x - self.x
        dy = y - self.y
        radians = math.atan2(-dy, dx)
        radians %= 2 * math.pi
        self.angle = math.degrees(radians)

    def rotate_images(self, images):
        """ (None) -> None
        Correct missing rotated images by rotating them automatically.
        """
        self.images_u = images[:]
        num = len(self.images_u)
        self.images_d = [pygame.transform.rotate(self.images_u[i], 180) for i in range(num)]
        self.images_l = [pygame.transform.rotate(self.images_u[i], 90) for i in range(num)]
        self.images_r = [pygame.transform.rotate(self.images_u[i], -90) for i in range(num)]

    def move_to_target(self, x, y):
        """ (int, int) -> None
        Move the Character toward the given x and y co-ordinates.
        """
        self.rotate(x, y)
        self.vx = self.top_speed * math.cos(math.radians(self.angle))
        self.vy = -self.top_speed * math.sin(math.radians(self.angle))

    def update(self):
        """ (None) -> None
        Update the Character object. Call on every iteration of the game loop.
        """
        if not DOWN in self.possible_directions and self.vy > 0:
            self.vy = 0
        elif not UP in self.possible_directions and self.vy < 0:
            self.vy = 0
        if not LEFT in self.possible_directions and self.vx < 0:
            self.vx = 0
        elif not RIGHT in self.possible_directions and self.vx > 0:
            self.vx = 0
        if self.vx < 0:
            self.current_images = self.images_l
        elif self.vx > 0:
            self.current_images = self.images_r
        elif self.vy > 0:
            self.current_images = self.images_d
        elif self.vy < 0:
            self.current_images = self.images_u
        self.x += self.vx
        self.y += self.vy
        if self.vx != 0 or self.vy != 0:
            self.image_counter += 0.2
        self.rect = self.get_rect()
        
    def draw(self, surface):
        """ (Surface) -> None
        Draw the character onto the given Surface object.
        """
        surface.blit(self.current_images[int(self.image_counter) % len(self.images_l)], self.rect)

    def set_rect(self, rect):
        """ (Rect) -> None
        Set the Character rect to the given pygame Rect object.
        """
        self.x, self.y = rect.x, rect.y

    def get_rect(self):
        """ (None) -> Rect
        Return a Rect object representing the character co-ordinates.
        """
        result = self.current_images[int(self.image_counter) % len(self.images_l)].get_rect()
        result.center = self.x, self.y
        return result

    def get_west(self):
        return self.rect.inflate(10, 10).midleft

    def get_east(self):
        return self.rect.inflate(10, 10).midright

    def get_north(self):
        return self.rect.inflate(10, 10).midtop

    def get_south(self):
        return self.rect.inflate(10, 10).midbottom

    def get_north_east(self):
        return self.rect.topright

    def get_north_west(self):
        return self.rect.topleft

    def get_south_west(self):
        return self.rect.bottomleft

    def get_south_east(self):
        return self.rect.bottomright

    def set_speed(self, vx=0, vy=0):
        """ ([int], [int]) -> None
        Set the player's x and y velocity to the given values.
        Adjust the angle accordingly.
        """
        self.vx = int(vx)
        self.vy = int(vy)
        self.normalize()
        if self.vx == 0 and self.vy == 0:
            self.image_counter = 0

    def set_direction(self, direction=STOP):
        """ ([int]) -> None
        Set the player's direction.
        """
        direction = int(direction)
        if direction == RIGHT: self.set_speed(1000, 0)
        elif direction == UP: self.set_speed(0, -1000)
        elif direction == LEFT: self.set_speed(-1000, 0)
        elif direction == DOWN: self.set_speed(0, 1000)
        else: self.set_speed()

    def get_speed(self):
        """ (None) -> tuple
        Return the player character x and y velocity as a 2-tuple.
        """
        return self.vx, self.vy


class Player(Character):

    def update(self):
        """ (None) -> None
        Update the Player object. Call on every game loop iteration.
        Overrides Character.update().
        """
        Character.update(self)
        self.x -= self.vx
        self.y -= self.vy

    def set_aiming_image(self, image, facing_up=True):
        """ (Surface, [bool]) -> None
        Specify which image to use as the rotating aiming picture.
        MUST be called once before any draw() calls.
        """
        self.aiming_image = load_image(image)
        if facing_up:
            self.aiming_image = pygame.transform.rotate(self.aiming_image, -90)

    def get_rect(self):
        """ (None) -> Rect
        Return a Rect that represents the bounding box of the player character.
        Overrides Character.get_rect().
        """
        if self.aiming:
            result = pygame.transform.rotate(self.aiming_image, self.angle).get_rect().inflate(-10, -10)
        else:
            result = self.current_images[int(self.image_counter) % len(self.images_l)].get_bounding_rect()
        result.center = self.x, self.y
        return result

    def draw(self, surface):
        """ (Surface) -> None
        Draw the player character onto the given display Surface.
        """
        if not self.aiming:
            Character.draw(self, surface)
        else:
            surface.blit(pygame.transform.rotate(self.aiming_image, self.angle), self.rect)


class Enemy(Character):

    def get_rect(self):
        """ (None) -> Rect
        Return a Rect that represents the bounding box of the player character.
        Overrides Character.get_rect().
        """
        image = pygame.transform.rotate(self.images_r[int(self.image_counter) % len(self.images_l)], self.angle)
        result = image.get_bounding_rect()
        result.center = self.x, self.y
        return result

    def draw(self, surface):
        """ (Surface) -> None
        Draw the enemy onto the given Surface, rotated based on the current angle.
        Overrides Character.draw()
        """
        image = pygame.transform.rotate(self.images_r[int(self.image_counter) % len(self.images_l)], self.angle)
        surface.blit(image, self.rect)
        if self.collides_with(pygame.mouse.get_pos()):
            font_surface = self.text_font.render('Health: ' + str(self.health), 1, WHITE)
            font_rect = font_surface.get_rect()
            font_rect.center = self.rect.centerx, self.rect.top - 20
            surface.blit(font_surface, font_rect)


class Splatter(ShiftableObject):

    def __init__(self, x, y, image):
        """ (int, int, [Surface]) -> Splatter
        Instantiate a blood splatter object.
        """
        ShiftableObject.__init__(self, x, y)
        self.image = load_image(image)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def draw(self, surface):
        surface.blit(self.image, self.rect)