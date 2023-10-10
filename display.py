"""
Module to display the game UI
"""
import pygame
from config import GameConstants as gc

class Display:
    """
    Class to display the game data to the screen
    """
    def __init__(self, x, y, colour, size, text, bound):
        self.coord = (x, y)
        self.colour = colour
        self.size = size
        self.text = text
        self.bound = bound

    def draw(self):
        """
        Draw the text on the screen
        """
        message = gc.font_small.value.render(self.text, True, self.colour)
        gc.SURFACE.value.blit(message, (self.coord[0], self.coord[1] // 4 + message.get_height()))

    def bound_box(self):
        """
        Draw a box around text length
        """
        pass