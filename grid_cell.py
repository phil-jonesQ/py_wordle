"""
GridCell module
"""
import pygame
from config import GameConstants as gc


class GridCell:
    """
    GridCell class
    """
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def draw_cell(self, colour):
        """
        Draw cell to the surface
        """
        pygame.draw.rect(gc.SURFACE.value,
                         gc.COLOURS.value[f"{colour}"],
                         (self.col * gc.CELL_SIZE.value,
                          self.row * gc.CELL_SIZE.value,
                          gc.CELL_SIZE.value - gc.PAD.value,
                          gc.CELL_SIZE.value - gc.PAD.value), 2)

    def fill_cell(self, colour):
        """
        Draw a filled cell to the surface
        """
        pygame.draw.rect(gc.SURFACE.value,
                         gc.COLOURS.value[f"{colour}"],
                         (self.col * gc.CELL_SIZE.value + gc.PAD.value // 2,
                          self.row * gc.CELL_SIZE.value + gc.PAD.value // 2,
                          gc.CELL_SIZE.value - gc.PAD.value * 2,
                          gc.CELL_SIZE.value - gc.PAD.value * 2))
