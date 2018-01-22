#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: level.py
# Description: Level class
#####################################

from random import randint, choice
from constants import *
from data_loader import *
from bullet import Bullet
from character import Player, Enemy, Splatter
from ending import Lock, Key
from item import Item
from spritesheet import Spritesheet


class Level(object):
    """ Level class that keeps track of all level objects and visuals. """

    def __init__(self, path_img, wall_img):
        """ (str, str) -> Level
        Instantiate a blank level.
        """

        # ----- Parameter-based properties -----
        self.path_image = load_image(path_img)
        self.wall_image = load_image(wall_img)

        # ----- Intersections, rooms, paths -----
        self.directions = []        # List of integers for intersection directions
        self.paths = []             # List of path Rect objects
        self.rooms = []             # List of room Rect objects
        self.path_width = 260       # Width of each path
        self.wall_width = 35        # Thickness of each wall
        self.wall_surfaces = []     # List of wall (outer) Surfaces for rooms and paths
        self.floor_surfaces = []    # List of floor (inner) Surfaces

        # ----- Level objects -----
        self.items = []
        self.ammo = 15
        self.key = None
        self.blood = []

        # ----- Characters -----
        self.player = None
        self.enemies = []

        # ----- I/O -----
        self.keys = None
        self.mouse_buttons = [0] * 3

        # ----- Other -----
        self.bullets = []           # List of active bullets
        self.endpoint = []          # [x, y] co-ordinates of the end of the level
        self.screen_w = None        # Screen width and height
        self.screen_h = None        # This data will be obtained later
        self.level_num = 1          # Current level number

    @staticmethod
    def get_opposite_dir(direction):
        """ (int) -> int
        Returns an integer index representing the opposite direction.
        """
        return (2 + direction) % 4

    def populate_directions(self, numdirections):
        """ (int) -> None
        Determine path directions (directions are integers from 0 to 3).
        """
        self.directions = []
        while len(self.directions) < numdirections:
            try:
                possible_dirs = []
                for i in range(4):
                    prev_dir = self.directions[-1]
                    if prev_dir != i and prev_dir != self.get_opposite_dir(i):
                        possible_dirs.append(i)
                self.directions.append(choice(possible_dirs))
                self.populate_paths()
                collision = self.paths[-1].collidelist(self.rooms) != -1 or\
                    self.paths[-1].collidelist(self.paths[:-1]) != -1
                while collision and len(possible_dirs) > 1:
                    possible_dirs.remove(self.directions[-1])
                    del self.directions[-1]
                    self.directions.append(choice(possible_dirs))
                    self.populate_paths()
                    collision = self.paths[-1].collidelist(self.rooms) != -1 or \
                        self.paths[-1].collidelist(self.paths[:-1]) != -1
                if collision:
                    return
            except IndexError:
                self.directions.append(randint(0, 3))

    def increment(self):
        """ (None) -> None
        Resets all relevant level objects and increments the level number by 1.
        """
        self.level_num += 1
        self.generate()

    def populate_paths(self):
        """ (None) -> None
        Using the generated directions, create physical path Rects.
        """
        self.paths = []
        x = self.rooms[0].centerx
        y = self.rooms[0].centery
        if self.directions[0] == 0:
            x += self.rooms[0].width // 2
        elif self.directions[0] == 2:
            x -= self.rooms[0].width // 2
        elif self.directions[0] == 1:
            y -= self.rooms[0].height // 2
        else:
            y += self.rooms[0].height // 2
        for direction in self.directions:
            path_length = randint(3 * self.path_width, 7 * self.path_width)
            if direction == 0:
                self.paths.append(pygame.Rect(x, y, path_length, self.path_width))
                x += (path_length - self.path_width)
            elif direction == 2:
                self.paths.append(pygame.Rect(x - path_length, y, path_length, self.path_width))
                x -= path_length
            elif direction == 1:
                self.paths.append(pygame.Rect(x, y - path_length, self.path_width, path_length))
                y -= path_length
            else:
                self.paths.append(pygame.Rect(x, y, self.path_width, path_length))
                y += (path_length - self.path_width)

        # Determine the level endpoint
        sample_lock = Lock(x, y, 'lock_blue.png')
        lock_rect = sample_lock.rect.inflate(10, 10).clamp(self.paths[-1])
        self.endpoint = list(lock_rect.topleft)

    def populate_output_surfaces(self):
        """ (None) -> None
        Caches each level object as a list of Surfaces to accelerate and facilitate blitting.
        """
        self.wall_surfaces = []
        self.floor_surfaces = []
        for rect in self.paths + self.rooms:
            # Create a blank surface to use for the "floor" of each room and hallway.
            floor_surface = pygame.Surface(rect.size).convert()

            # Tile the floor tiles all over the newly created Surface, starting from the origin (0, 0).
            self.tile(self.path_image, floor_surface, pygame.Rect((0, 0), rect.size))

            # Add the floor surface to the internal list of all floor surfaces.
            self.floor_surfaces.append(floor_surface)

            # Calculate an enlarged Rect to use for the outer wall.
            wall_rect = rect.inflate(2 * self.wall_width, 2 * self.wall_width)

            # Perform the same steps as above, except for the wall tiles instead of the floor tiles.
            wall_surface = pygame.Surface(wall_rect.size).convert()
            self.tile(self.wall_image, wall_surface, pygame.Rect((0, 0), wall_rect.size))
            self.wall_surfaces.append(wall_surface)

    def add_pass_through_rooms(self, x=5):
        """ (None, [int]) -> None
        Attempt to add 'x' number of rooms such that the paths go through the rooms.
        """
        if len(self.rooms) > 1:
            self.rooms = [self.rooms[0]]
        descending_paths = self.paths[:]
        descending_paths.sort(key=lambda r: max(r.width, r.height))
        descending_paths.reverse()
        for i in range(x):
            try:
                height = width = max(descending_paths[i].width, descending_paths[i].height) // 5
                top = descending_paths[i].centery - height // 2
                left = descending_paths[i].centerx - width // 2
                if width - self.path_width > 40:
                    self.rooms.append(pygame.Rect(left, top, width, height))
            except IndexError:
                print('WARNING: Attempted to add pass-through room to nonexistent path!')

    def add_item(self, image, type='food'):
        room = choice(self.rooms + self.paths)
        x = randint(room.left, room.right - image.get_width())
        y = randint(room.top, room.bottom - image.get_height())
        self.items.append(Item(image, x, y, type))

    def generate(self, game=None):
        """ (None, Game) -> None
        Generate a pseudorandom world with the given Game instance.
        """
        # Generate the central room.
        self.rooms = []
        if game is not None:
            self.screen_w = w = game.screen_w
            self.screen_h = h = game.screen_h
        else:
            w = self.screen_w
            h = self.screen_h
        room_size = 3 * self.path_width // 2
        self.rooms.append(pygame.Rect(w // 2 - room_size, h // 2 - room_size, 2 * room_size, 2 * room_size))

        # Determine path directions (Directions are integers from 0-3).
        self.populate_directions(2 * self.level_num + 3)

        # Convert the directions to paths.
        self.populate_paths()

        # Add pass-through room areas.
        self.add_pass_through_rooms(abs(len(self.paths) - 2))

        # Cache level object Surfaces
        self.populate_output_surfaces()

        # Prepare game objects.
        self.initialize_player()
        enemy_sheet = Spritesheet('zombiebasic.png', 4, 3)
        regular_zombie_images = list(enemy_sheet[0:3]) + list(enemy_sheet[4:7])
        weak_zombie_images = [load_image('zombie.png')]
        num_enemies = len(self.rooms) * 2
        self.enemies = []
        for x, y in self.get_multiple_enemy_locations(num_enemies):
            if randint(0, 1):
                self.enemies.append(Enemy(x, y, 4, *regular_zombie_images))
                self.enemies[-1].health = randint(2, 3) * 50
            else:
                self.enemies.append(Enemy(x, y, 5, *weak_zombie_images))
                self.enemies[-1].health = 50
        self.lock = Lock(self.endpoint[0], self.endpoint[1], 'lock_blue.png')

        # Add food and pickups
        self.items = []
        num_foods, num_health_packs, num_ammo_packs = 3 * len(self.rooms) // 2, \
                                                      len(self.rooms) // 2, len(self.rooms) // 3 + 1
        food_images = Spritesheet('food.png', 14, 8)    # Spritesheet object for food items
        food_images *= 1.4                              # Enlarge the spritesheet
        icon_images = Spritesheet('icons.png', 3, 2)    # Spritesheet object for icons
        icon_images *= 1.5
        health_pack_image = icon_images[0]              # Extract the health pack image
        ammo_pack_image = load_image('ammo.png')
        for i in range(num_foods):
            image = choice(food_images[:])
            self.add_item(image)
        for i in range(num_health_packs):
            self.add_item(health_pack_image, 'health')
        for i in range(num_ammo_packs):
            self.add_item(ammo_pack_image, 'ammo')
        self.blood = []
        self.blood_images = enemy_sheet[10], enemy_sheet[9]     # Large and small blood splatter

        # Add a key
        image = load_image('keyblue.png')
        room = choice(self.rooms)
        x = randint(room.left, room.right - image.get_width())
        y = randint(room.top, room.bottom - image.get_height())
        self.key = Key(x, y, image)

    def shift(self, dx, dy):
        """ (int, int) -> None
        Shift the entire level by the given increments (+x, +y is right and down).
        """
        for rect in self.paths + self.rooms:
            rect.move_ip(dx, dy)
        for thing in self.blood + self.enemies + self.items + self.bullets + [self.lock] + [self.key]:
            thing.shift(dx, dy)


    def get_multiple_enemy_locations(self, x):
        """ (int) -> list
        Return a list with size "x" of [x, y] position lists that represent
        appropriate enemy spawn locations.
        """
        enemy_locations = []
        rooms = self.rooms[1:] + self.paths[1:]
        for i in range(x):
            rect = rooms[i % len(rooms)]
            offset_x = randint(-rect.width // 4, rect.width // 4)
            offset_y = randint(-rect.height // 4, rect.height // 4)
            enemy_locations.append([rect.centerx + offset_x, rect.centery + offset_y])
        return enemy_locations

    def is_collision(self, point):
        """ (Rect) -> bool
        Return True if the given point collides with any wall, False otherwise.
        """
        for rect in self.paths + self.rooms:
            if rect.collidepoint(point):
                return False
        return True

    def initialize_player(self):
        """ (None) -> None
        Initialize the player character for use in the game loop.
        """
        if not self.player:
            player_spritesheet = Spritesheet('player.png', 2, 4)
            self.player = Player(self.screen_w // 2, self.screen_h // 2, 7, *player_spritesheet[0:6])
            self.player.set_aiming_image(player_spritesheet[6])

    def update_player(self):
        """ (None) -> None
        Update the player object based on user inputs.
        """
        # Gather info
        should_shoot = pygame.mouse.get_pressed()[0] and not self.mouse_buttons[0]
        self.keys = pygame.key.get_pressed()
        self.mouse_buttons = pygame.mouse.get_pressed()
        up, down, left, right = self.keys[K_w], self.keys[K_s], self.keys[K_a], self.keys[K_d]
        self.player.aiming = pygame.mouse.get_pressed()[-1]

        # Set the player's direction
        if left: self.player.set_direction(LEFT)
        elif up: self.player.set_direction(UP)
        elif right: self.player.set_direction(RIGHT)
        elif down: self.player.set_direction(DOWN)
        else: self.player.set_direction()

        # Override the player's direction if they're aiming
        if self.player.aiming:
            self.player.rotate(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            self.player.set_speed()
        # Shoot a bullet if the player presses the left mouse button - decrease ammo and food as well
        if self.player.aiming and should_shoot and self.ammo > 0:
            self.bullets.append(Bullet(BLACK, self.player.x, self.player.y, 16, self.player.angle))
            self.player.hunger += 0.05
            self.ammo = max(0, self.ammo - 1)

        # Update the player and obtain the new speed to shift the level
        self.player.update()
        vx, vy = self.player.get_speed()
        vx, vy = -vx, -vy
        self.shift(vx, vy)

        # Start reducing health when hunger gets high
        if self.player.hunger >= HUNGER_LIMIT and randint(0, 75) == 0:
            self.player.health -= 5

    def rebound_character(self, character, stopdir=LEFT):
        """ (Character, [int]) -> None
        Handle wall collisions that require the character to no longer go in the given
        stop direction.
        """
        if stopdir == LEFT:
            vx = character.top_speed
            vy = 0
        elif stopdir == RIGHT:
            vx = -character.top_speed
            vy = 0
        elif stopdir == DOWN:
            vx = 0
            vy = -character.top_speed
        else:
            vx = 0
            vy = character.top_speed
        character.image_counter = 0
        if not isinstance(character, Player):
            character.shift(vx, vy)
        else:
            self.shift(-vx, -vy)

    def handle_wall_collision(self, character):
        """ (Character) -> None
        Check and react to collisions between the given Character and all walls.
        """
        character.possible_directions = [i for i in xrange(4)]
        e = self.is_collision(character.get_east())
        ne = self.is_collision(character.get_north_east())
        n = self.is_collision(character.get_north())
        nw = self.is_collision(character.get_north_west())
        w = self.is_collision(character.get_west())
        sw = self.is_collision(character.get_south_west())
        s = self.is_collision(character.get_south())
        se = self.is_collision(character.get_south_east())
        if w or sw or nw:
            self.rebound_character(character, LEFT)
        if n or ne or nw:
            self.rebound_character(character, UP)
        if ne or e or se:
            self.rebound_character(character, RIGHT)
        if s or sw or se:
            self.rebound_character(character, DOWN)

    def handle_pickups(self):
        """ (None) -> None
        Check for and react to collisions with items
        """
        for item in self.items:
            if not item.is_alive() or not self.player.collides_with(item):
                continue
            item.destroy()
            if item.type == 'food':
                self.player.hunger -= 3
                self.player.hunger = max(self.player.hunger, 0)
            elif item.type == 'health':
                self.player.health += 10
            elif item.type == 'ammo':
                self.ammo += randint(4, 16)

    def collide_with_player(self, character):
        """ (Character) -> None
        Check for and handle collisions between the given Character and the player.
        """
        if character.collides_with(self.player):
            self.player.health -= character.damage
            self.shift(self.player.vx, self.player.vy)
            character.shift(-2 * character.vx, -2 * character.vy)
            self.blood.append(Splatter(self.player.x, self.player.y, self.blood_images[1]))
        if len(self.blood) > 25:
            self.blood.pop(0)

    def update(self):
        """ (None) -> None
        Update the state of the Level.
        """
        self.update_player()
        self.handle_wall_collision(self.player)
        if self.player.get_speed() != (0, 0):
            self.player.hunger += 0.005

        new_enemies = []
        for enemy in self.enemies:
            enemy.update()
            everything = self.paths + self.rooms
            if self.player.rect.collidelist(everything) == enemy.rect.collidelist(everything):
                enemy.move_to_target(self.player.x, self.player.y)
            self.handle_wall_collision(enemy)
            self.collide_with_player(enemy)
            if enemy.health > 0:
                new_enemies.append(enemy)
            else:
                self.blood.append(Splatter(enemy.x, enemy.y, self.blood_images[0]))
        self.enemies = new_enemies

        self.handle_pickups()

        for item in self.items + [self.key]:
            item.update()
        if self.key and self.player.collides_with(self.key):
            self.key.visible = False
            self.lock.unlock()
        if not self.lock.locked and self.player.collides_with(self.lock):
            pygame.time.delay(1000)
            self.increment()

        enemy_rects = [enemy.rect for enemy in self.enemies]
        bullets = []
        for bullet in self.bullets:
            index = bullet.rect.collidelist(enemy_rects)
            if index > -1:
                self.enemies[index].health -= bullet.damage
                continue
            if not (0 <= bullet.x <= self.screen_w and 0 <= bullet.y <= self.screen_h) or \
                    self.is_collision((bullet.x, bullet.y)):
                continue
            bullet.update()
            bullets.append(bullet)
        self.bullets = bullets

    @staticmethod
    def tile(source, dest, rect):
        """ (Surface, Surface, Rect) -> None
        Completely tile the given destination surface with tiles of the source surface, within the bounds
        specified by the rect argument.
        """
        for x in xrange(rect.left, rect.right, source.get_width()):
            for y in xrange(rect.top, rect.bottom, source.get_height()):
                dest.blit(source, (x, y), (0, 0, rect.right - x, rect.bottom - y))

    def draw(self, surface):
        """ (Surface) -> None
        Draw all level objects onto the given Surface.
        """
        # Get a list of every Rect that represents a room or hallway.
        rects = self.paths + self.rooms

        # Iterate through all of the cached wall surfaces and blit them.
        for i in range(len(rects)):
            surface.blit(self.wall_surfaces[i], rects[i].inflate([2 * self.wall_width] * 2))

        # Iterate through all of the cached floor surfaces and blit them - smaller than the wall surfaces
        # due to the lack of a border.
        for i in range(len(rects)):
            surface.blit(self.floor_surfaces[i], rects[i])

        # Draw enemies, items, and bullets
        for item in self.blood + [self.lock] + self.items + [self.key] + self.enemies + self.bullets:
            item.draw(surface)

        # Draw player
        self.player.draw(surface)