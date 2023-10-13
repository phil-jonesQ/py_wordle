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

    def print_char(self, key_char):
        """
        Draw a character onto the grid
        """
        key_char_text = gc.font.value.render(
            key_char, True, gc.COLOURS.value["BLACK"])
        gc.SURFACE.value.blit(key_char_text,
                              (self.col * gc.CELL_SIZE.value +
                               gc.CELL_SIZE.value // 2 -
                               key_char_text.get_width() // 2,
                               self.row * gc.CELL_SIZE.value +
                               gc.CELL_SIZE.value // 2 -
                               key_char_text.get_height() // 2))

    def fill_ui_area(self, colour):
        """
        Draw a filled cell to the surface
        """
        pygame.draw.rect(gc.SURFACE.value,
                         gc.COLOURS.value[f"{colour}"],
                         (0,
                          gc.WINDOW_HEIGHT.value // 1.47,
                          gc.WINDOW_WIDTH.value,
                          gc.WINDOW_HEIGHT.value // 2))
