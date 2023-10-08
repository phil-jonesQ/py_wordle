"""
Setup module to initialize pygame and game constants
"""
from enum import Enum
import pygame


class GameConstants(Enum):
    """
    Define constants
    """
    # Set up game constants
    APP_NAME = "Wordle"

    # Set up display constants
    WINDOW_WIDTH, WINDOW_HEIGHT = 600, 500
    COLOURS = {
        'BG_COLOUR': (255, 255, 255),
        'WHITE': (255, 255, 255),
        'DEFAULT': (245, 245, 245),
        'BLACK': (0, 0, 0,),
        'YELLOW': (255, 255, 0),
        'RED': (255, 0, 0),
        'GREEN': (0, 255, 0),
        'GREY': (111, 111, 111),
        'CYAN': (0, 100, 100)
        }
    GRID_SIZE = (6, 5)  # ROWS, COLS
    CELL_SIZE = 80
    PAD = 5
    START_SCORE = 90
    FPS = 60

    # Create the window
    SURFACE = pygame.display.set_mode(
        (WINDOW_WIDTH, WINDOW_HEIGHT))
    
    # Initialise Pygame
    pygame.init()
    pygame.display.set_caption(APP_NAME)
    # Initialise the font
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 22)
