#####################################
# Programmer: Kenneth Sinder
# Date: Sunday, June 15, 2014
# Filename: run_game.py
# Description: Launching point for the Supremacy game
#####################################
import modules.game, modules.constants

if __name__ == '__main__':
    game = modules.game.Game(modules.constants.SMOOTH_FPS)
    game.run()
