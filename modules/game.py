#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: game.py
# Description: Main Game class for Supremacy
#####################################

import sys
from constants import *
from data_loader import *
from level import Level
from gui import Button, Stripe


class Game(object):

    def __init__(self, fps):
        """ (int) -> Game
        Instantiate a Game object with the given desired framerate.
        """

        # ----- Initialization -----
        pygame.init()                   # Initialize the Pygame package

        # ----- FPS + Clock -----
        self.desired_fps = fps                  # Target framerate in frames per second
        self.fps_clock = pygame.time.Clock()    # Clock object to enforce framerate
        self.measured_fps = 0                   # Actual FPS

        # ----- Display -----
        self.screen_w = pygame.display.list_modes()[0][0]        # Screen width is the user's screen's width
        self.screen_h = pygame.display.list_modes()[0][1]        # Screen height is the user's screen's height
        self.flags = HWACCEL | RLEACCEL | ASYNCBLIT | FULLSCREEN # Accelerated fullscreen flags
        self.display_surf = pygame.display.set_mode((self.screen_w, self.screen_h), self.flags)
        self.display_surf.set_alpha(None)                        # Disable display transparency to boost FPS
        pygame.display.set_caption(TITLE + ' by ' + PROGRAMMER)  # Set the screen caption (just for fun)

        # ----- Events -----
        self.events = []                                            # List of Pygame events
        pygame.event.set_allowed([QUIT, KEYDOWN, MOUSEBUTTONDOWN])  # Restrict the allowed events to boost FPS

        # ----- Preloaded Fonts -----
        self.hud_font = load_font(DIGITAL, 40)              # Font for sidebar
        self.reg_font = load_font('GeosansLight.ttf', 28)   # General font object

        # ----- Other -----
        self.level = None           # Level object that keeps track of game state

    def terminate(self):
        """ (None) -> None
        End the game as soon as possible.
        """
        print('Closing game...')
        pygame.quit()
        sys.exit()

    def clear_screen(self):
        """ (None) -> None
        Clear the game window by filling in with black.
        """
        self.display_surf.fill(BLACK)

    def check_for_quits(self):
        """ (None) -> None
        Check for and respond to QUIT events and the ESCAPE key press.
        """
        for event in self.events:
            if event.type == QUIT:
                self.terminate()

    def update(self):
        """ (None) -> None
        Update the game state.
        """
        self.clear_screen()
        self.events = pygame.event.get()
        self.check_for_quits()

        # Draw the Pause Menu if necessary
        for event in self.events:
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                self.draw_pause_menu()

        self.level.update()
        self.level.draw(self.display_surf)

        # Draw sidebar text, coloured red if the property is low
        self.draw_hud_text(0, 'Level ' + str(self.level.level_num))
        if self.level.player.health > 20:
            self.draw_hud_text(50, 'Health: ' + str(self.level.player.health))
        else:
            self.draw_hud_text(50, 'Health: ' + str(self.level.player.health), RED)
        if self.level.player.hunger > HUNGER_LIMIT:
            self.draw_hud_text(100, 'Hunger: ' + str(int(self.level.player.hunger)), RED)
        else:
            self.draw_hud_text(100, 'Hunger: ' + str(int(self.level.player.hunger)))
        if self.level.ammo > 5:
            self.draw_hud_text(150, 'Ammo: ' + str(self.level.ammo))
        else:
            self.draw_hud_text(150, 'Ammo: ' + str(self.level.ammo), RED)

        self.redraw_and_proceed_tick()

    def draw_text(self, font, text='', x=0, y=0, center=False, colour=WHITE, surface=None):
        """ (Font, [str], [int], [int], [tuple], [Surface]) -> None
        Draw the given text onto the given Surface (or game window if no Surface given).
        """
        if not surface:
            surface = self.display_surf
        font_surface = font.render(str(text), 1, colour)
        font_rect = font_surface.get_rect()
        if center:
            font_rect.center = x, y
        else:
            font_rect.topleft = x, y
        surface.blit(font_surface, font_rect)

    def draw_hud_text(self, y, text, colour=WHITE):
        """ (int, str) -> None
        Draw the given message on the right side of the screen using a sleek font
        at the specified height co-ordinate.
        """
        x = self.screen_w - self.hud_font.size(text)[0]
        self.draw_text(self.hud_font, text, x, y, colour=colour)

    def draw_pause_menu(self):
        """ (None) -> None
        Draw a pause menu and loop until the player presses ESCAPE.
        """
        buttons = {'play': Button('Return to Game', self.screen_w // 2, self.screen_h // 2 - 50),
                   'quit': Button('Quit', self.screen_w // 2, self.screen_h // 2 + 50)}
        pausing = True
        while pausing:
            self.clear_screen()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    pausing = False
            self.draw_hud_text(0, 'PAUSED...')
            for button_type in buttons:
                buttons[button_type].update()
                buttons[button_type].draw(self.display_surf)
            if buttons['play'].pressed(): pausing = False
            if buttons['quit'].pressed(): self.terminate()
            self.redraw_and_proceed_tick()

    def update_title_buttons(self, **buttons):
        """ (None) -> bool
        Update, draw, and respond to the buttons on the title screen.
        Return True if the game should begin, False otherwise.
        """
        for button_label in buttons:
            buttons[button_label].update()
            buttons[button_label].draw(self.display_surf)
        if buttons['quit'].pressed():
            self.terminate()
        if buttons['play'].pressed():
            return True
        return False

    def draw_title_screen(self):
        """ (None) -> None
        Draw a title screen and loop around to poll user actions on the menu.
        """
        buttons = {'play': Button('New Game', self.screen_w // 2, self.screen_h // 2 + 80),
                   'quit': Button('Quit', self.screen_w // 2, self.screen_h // 2 + 150)}
        stripes = [Stripe(100, 0), Stripe(self.screen_w - 100, 0)]
        while True:
            # Clear screen and check for events.
            self.clear_screen()
            self.events = pygame.event.get()
            self.check_for_quits()

            # Draw the game title and description.
            x, y = self.screen_w // 2, self.screen_h // 2 - 60
            self.draw_text(load_font(SLEEK, 72), TITLE, x, y, 1)
            x, y = self.screen_w // 2, self.screen_h // 2
            self.draw_text(load_font(SLEEK, 28), SHORT_DESCR, x, y, 1)

            # Update all of the title buttons and check for game start.
            if self.update_title_buttons(**buttons): break

            # Update all of the stripes.
            for stripe in stripes:
                stripe.update()
                stripe.draw(self.display_surf)

            # Update the game window and delay to enforce FPS.
            self.redraw_and_proceed_tick()

    def draw_game_over_screen(self, time=5):
        """ ([int]) -> None
        Draw a game over screen for the given number of seconds.
        """
        self.clear_screen()
        self.draw_hud_text(50, 'Game Over! Returning to main menu...')
        self.redraw_and_proceed_tick()
        pygame.time.delay(1000 * time)

    def display_story(self):
        """ (None) -> None
        Show the game's backstory.
        """
        done = False
        while not done:
            self.clear_screen()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_SPACE):
                    done = True

            self.display_surf.blit(self.level.wall_image, (0, 0))
            self.display_surf.blit(self.level.player.current_images[0], (85, 85))
            self.draw_text(self.reg_font, 'Howard Hulk woke up in a large, strange room in a cave.', 280, 150)
            self.draw_text(self.reg_font, 'The cave is filled with deadly but seemingly unintelligent zombies.',
                           280, 250)
            self.draw_text(self.reg_font, 'He has no choice but to keep running and search for an exit.',
                           280, 350)
            self.draw_text(self.reg_font, 'Help him begin his exit dash. Press SPACE to start.', 280, 450)

            self.redraw_and_proceed_tick()

    def display_win_screen(self):
        """ (None) -> None
        Display a screen to show the player that they beat the game.
        """
        image = pygame.transform.scale(load_image('hyperion.png'), [1920, 1080])
        done = False
        while not done:
            self.clear_screen()
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                    done = True

            self.display_surf.blit(image, (0, 0))
            self.draw_text(self.reg_font, 'Howard fell through what he thought was just another hatch.', 10, 50)
            self.draw_text(self.reg_font, 'It led to a vast, open, free world. Something that Howard calls home.',
                           10, 150)
            self.draw_text(self.reg_font, 'He found the exit. You win.',
                           10, 250)
            self.draw_text(self.reg_font, 'Programming by ' + PROGRAMMER + ' Press ESCAPE to exit.', 10, 350)

            self.redraw_and_proceed_tick()

    def redraw_and_proceed_tick(self):
        """ (None) -> None
        Update the screen and enforce the desired FPS.
        """
        pygame.display.flip()
        self.fps_clock.tick_busy_loop(self.desired_fps)
        self.measured_fps = self.fps_clock.get_fps()

    @staticmethod
    def start_music(filename):
        pygame.mixer.music.load(get_music_path(filename))
        pygame.mixer.music.play(-1)

    def run(self):
        """ (None) -> None
        Execute Rogueline.
        """
        while True:
            # Instantiate and prepare level
            self.level = Level('concrete.png', 'rockwall.png')
            self.level.generate(self)

            # Play title music and show title screen
            self.start_music('music2.mp3')
            self.draw_title_screen()

            # Show game backstory
            self.display_story()

            # Play game music and enter the game loop
            self.start_music('music1.mp3')
            while True:
                self.update()
                if self.level.player.health <= 0:
                    self.draw_game_over_screen()
                    break
                elif self.level.level_num > LAST_LEVEL:
                    break

            if self.level.player.health > 0:
                self.display_win_screen()

    def get_rect(self):
        """ (None) -> Rect
        Return a Rect object representing the boundaries of the display Surface.
        """
        return self.display_surf.get_rect()
