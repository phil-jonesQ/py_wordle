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
        self.message = gc.font_small.value.render(self.text, True, self.colour)

    def draw(self):
        """
        Draw the text on the screen
        """
        gc.SURFACE.value.blit(self.message, (self.coord[0], self.coord[1]))
        if self.bound:
            self.bound_box()


    def bound_box(self):
        """
        Draw a box around text length
        """
        pygame.draw.rect(gc.SURFACE.value,
                         self.colour,
                         (self.coord[0] - gc.PAD.value,
                          self.coord[1] - gc.PAD.value,
                          self.message.get_width() + gc.PAD.value * 2,
                          self.message.get_height() + gc.PAD.value * 2), 1)