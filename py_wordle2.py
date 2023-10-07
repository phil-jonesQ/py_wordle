"""
Simple Wordle Clone
phil.jones.24.4@gmail.com
"""

import random
import sys
import pygame
from config import GameConstants as gc
from grid_cell import GridCell


def load_random_word():
    """
    Function to load the word_list
    Returns a random word string
    """
    # Load word list from a file
    try:
        with open("wordlist.txt", "r", encoding="utf8") as file:
            words = [line.strip().upper() for line in file.readlines()]
    except FileNotFoundError as file_error:
        print("File not found", file_error)
        sys.exit(1)
    # Select a random word for the player to guess
    word_to_guess = random.choice(words)
    return word_to_guess, words


class Wordle:
    """
    Wordle main game class
    """
    def __init__(self):
        self.reset()
        self.surface = gc.SURFACE.value

    def reset(self):
        """
        reset game state
        """
        self.grid_state = {}
        self.game_state = {
            'current_row': 0,
            'current_col': 0,
            'check_flag': False,
            'not_a_word_flag': False
        }
        self.game_data = {
            'score': gc.START_SCORE.value,
            'win': False,
            'loose': False,
            'game_over': False
        }

        # Load the random word and words in
        self.the_word, self.words = load_random_word()

        # Initialise the letter
        # Need to make a spare end column for backspace
        self.letter_store = [['_' for _ in range(gc.GRID_SIZE.value[1] + 1)]
                             for _ in range(gc.GRID_SIZE.value[0])]
        self.grid_state = {(row, col): 'DEFAULT'
                           for row in range(gc.GRID_SIZE.value[0])
                           for col in range(gc.GRID_SIZE.value[1])}

        # Initialise the guessed word
        print("Debug here is the word " + self.the_word)

    def draw_grid(self):
        """
        Draw the grid on the surface
        """
        # Draw the grid
        # print(f"Debug grid state is {self.grid_state}")
        for row in range(gc.GRID_SIZE.value[0]):
            for col in range(gc.GRID_SIZE.value[1]):
                # Create a cell object
                cell = GridCell(row, col)
                cell.draw_cell("CYAN")
                if self.grid_state.get((row, col)) == "GREY":
                    cell.fill_cell("GREY")

    def fill_grid_cell(self, row, col, colour):
        """
        Fills the cell to desired colour
        """
        cell = GridCell(row, col)
        cell.fill_cell(colour)

    def draw_grid_char(self, row, col, letter_store):
        """
        Draws the chars to the screen
        """
        cell_update = GridCell(row, col)
        cell_update.print_char(letter_store[row][col])

    def populate_row(self):
        pass

    def check_row(self):
        pass


def main():
    """
    Main game loop function
    """
    # Create a Game Instance
    wordle = Wordle()
    current_col = wordle.game_state.get('current_col')
    current_row = wordle.game_state.get('current_row')
    letter_store = wordle.letter_store

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            # Handle Game Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Handle key input
            if event.type == pygame.KEYDOWN and event.key >= 97 and event.key <= 122:
                not_a_word_flag = False
                check_flag = False
                key_char = chr(event.key).upper()
                letter_store[current_row][current_col] = key_char

                # Increment the col
                current_col += 1
                if current_col >= gc.GRID_SIZE.value[1]:
                    current_col = gc.GRID_SIZE.value[1]#
            # Handle back space
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                        letter_store[current_row][current_col - 1] = '_'
                        current_col = current_col - 1
                        if current_col <= 0:
                            current_col = 0

        # Clear the screen with background color
        gc.SURFACE.value.fill(gc.COLOURS.value["BG_COLOUR"])
        
        # Draw the grid
        wordle.draw_grid()

        # Fill a grid square
        wordle.fill_grid_cell(0, 4, "GREEN")

        # Fill a grid square
        wordle.fill_grid_cell(0, 2, "YELLOW")

        # Fill a grid square
        wordle.fill_grid_cell(0,3, "GREY")

        # Draw char to Grid
        # Populate the letters in the grid
        for row in range(gc.GRID_SIZE.value[0]):
             for col in range(gc.GRID_SIZE.value[1]):
                 wordle.draw_grid_char(row, col, letter_store)


        # Update the display
        pygame.display.flip()

        # Limit frames per second (FPS)
        pygame.time.Clock().tick(gc.FPS.value)  # Limit to 60 frames per second



if __name__ == "__main__":
    main()