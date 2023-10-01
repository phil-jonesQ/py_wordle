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
        self.window_width, self.window_height = 800, 600
        self.bg_colour = (255, 255, 255)  # White color for the background

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
