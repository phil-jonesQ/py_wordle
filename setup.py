"""
Setup module to initialize pygame and game constants
"""
import pygame


class Setup:
    """
    Setup class to initialize pygame and game constants
    """
    def __init__(self):
        # Set up game constants
        self.app_name = "Wordle"

        # Set up display constants
        self.window_width, self.window_height = 600, 500
        self.bg_colour = (255, 255, 255)  # White color for 
        self.white = (255, 255, 255) 
        self.black = (0, 0, 0) # Black color for text
        self.yellow = (255, 255, 0) # Yellow color for partially correct letters
        self.red = (255, 0, 0) # Red color for incorrect letters
        self.green = (0, 255, 0) # Green color for fully correct letters
        self.grey = (222, 222, 222)
        self.cyan = (0, 100, 100)
        self.grid_size = (6, 5) # Rows, Cols
        self.cell_size = 80
        self.pad = 5

        # Create the window
        self.surface = pygame.display.set_mode(
            (self.window_width, self.window_height))

    def __str__(self):
        return self.__class__.__name__

    def get_name(self):
        """
        Return the app name
        """
        return self.app_name
