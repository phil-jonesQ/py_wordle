"""
Simple Wordle Clone
phil.jones.24.4@gmail.com
"""

import random
import sys
import pygame
from config import GameConstants as gc
from grid_cell import GridCell
from display import Display


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
    # word_to_guess = "ALLOW" # Input "LOLLY" to test
    # Result should be Y Y G _ _ _
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

    def fill_grid_cell(self, row, col, colour):
        """
        Fills the cell to desired colour
        """
        cell = GridCell(row, col)
        cell.fill_cell(colour)

    def draw_grid_char(self, row, col):
        """
        Draws the chars to the screen
        """
        cell_update = GridCell(row, col)
        cell_update.print_char(self.letter_store[row][col])

    def process_results(self, current_row):
        """
        Compare the guessed word against
        the_word and determine grid state
        """
        current_guess = self.decode_guess(current_row)
        translate_guess = self.translate_guess(current_guess)
        print(translate_guess)

        # Handle yellow and grey cells firs
        for index in range(gc.GRID_SIZE.value[1]):
            if translate_guess[index] == "Y":
                self.grid_state[(current_row, index)] = "YELLOW"
            elif translate_guess[index] == "G":
                self.grid_state[(current_row, index)] = "GREEN"
            else:
                self.grid_state[(current_row, index)] = "GREY"

    def translate_guess(self, guess):
        """
        Evaluates the guess and translates the guess
        to:
        'G' - char. is correctly placed
        'Y' - char. is misplaced
        '_' - char. is not in the secret word
        '0' - char. char has been checked
        based on code by Iulian Intorsureanu
        """
        # Initialise result
        result = [' '] * 5

        # Make a copy of the word and guess as lists
        the_word_copy = list(self.the_word)
        the_guess_copy = list(guess)

        # Iterate through the guess and mark the correct letters
        for index, char in enumerate(guess):
            if char == self.the_word[index]:
                result[index] = 'G'
                the_guess_copy[index] = '0' # Marked as checked
                the_word_copy.remove(char)
        
        # Iterate through the word and mark the misplaced letters
        for index, char in enumerate(the_guess_copy):
            if char != '0':
                if char in the_word_copy:
                    result[index] = 'Y'
                    the_guess_copy[index] = '0' # Marked as checked
                    the_word_copy.remove(char)
                else:
                    result[index] = '_'
        return result

    def decode_guess(self, current_row):
        """
        Examines the current row and decodes the
        guessed word
        """
        guessed_word_extract = []
        # Scan current row and build the word
        for index in range(gc.GRID_SIZE.value[1]):
            guessed_word_extract.append(self.letter_store[current_row][index])

        # Convert to a string
        guessed_word = "".join(guessed_word_extract)
        return guessed_word

    def have_we_won(self, current_row):
        """
        Check if the word_store matches the_word
        Returns True if won, False otherwise
        """
        check_word = self.decode_guess(current_row)
        # Return the result
        if check_word == self.the_word:
            self.game_data['win'] = True
            self.game_data['game_over'] = True
            return True
        else:
            return

    def is_it_a_word(self, current_row):
        """
        Check if the word_store matches the_word
        Returns True if the word is "valid", False otherwise
        """
        current_guess = self.decode_guess(current_row)
        # Convert to a string
        guessed_word = "".join(current_guess)

        # Return the result
        if guessed_word in self.words:
            return True
        else:
            return False

    def draw_title(self):
        ui_area = GridCell(10, 10)
        ui_area.fill_ui_area("UI")
        for i, letter in enumerate(list(gc.APP_NAME.value)):
            if i % 2 == 0:
                colour = "GREEN"
            elif i == 3:
                colour = "YELLOW"
            else:
                colour = "GREY"
            display = Display((gc.CELL_SIZE.value * 1.6) + i * 25,
                            gc.WINDOW_HEIGHT.value // 1.43,
                            gc.COLOURS.value[f"{colour}"],
                            "large",
                            letter,
                            True)
            display.draw()

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

            # Handle Inputs
            if event.type == pygame.KEYDOWN:
                # Handle key input
                if event.key >= 97 and event.key <= 122\
                        and not wordle.game_data['game_over']:
                    key_char = chr(event.key).upper()
                    letter_store[current_row][current_col] = key_char
                    # Increment the col
                    current_col += 1
                    if current_col >= gc.GRID_SIZE.value[1]:
                        current_col = gc.GRID_SIZE.value[1]
                if event.key == pygame.K_BACKSPACE\
                        and not wordle.game_data['game_over']:
                    letter_store[current_row][current_col - 1] = '_'
                    current_col = current_col - 1
                    if current_col <= 0:
                        current_col = 0
                if event.key == pygame.K_RETURN\
                        and not wordle.game_data['game_over']:
                    if wordle.is_it_a_word(current_row):
                        if current_col == gc.GRID_SIZE.value[1]:
                            # Check the submission
                            wordle.process_results(current_row)
                            # Check if we have won
                            wordle.have_we_won(current_row)
                            # Increment the row and reset the col
                            current_row = current_row + 1
                            current_col = 0
                            # Check if we have lost
                            if current_row == gc.GRID_SIZE.value[0]:
                                wordle.game_data['loose'] = True
                                wordle.game_data['game_over'] = True
                if event.key == pygame.K_SPACE\
                        and wordle.game_data['game_over']:
                    wordle = Wordle()
                    current_col = wordle.game_state.get('current_col')
                    current_row = wordle.game_state.get('current_row')
                    letter_store = wordle.letter_store

        # Clear the screen with background color
        gc.SURFACE.value.fill(gc.COLOURS.value["BG_COLOUR"])

        # Draw the grid
        wordle.draw_grid()

        # Draw Title
        wordle.draw_title()

        # Populate the cells depending on grid state
        for row in range(gc.GRID_SIZE.value[0]):
            for col in range(gc.GRID_SIZE.value[1]):
                wordle.fill_grid_cell(row, col,
                                      wordle.grid_state.get((row, col)))

        # Draw char to Grid
        # Populate the letters in the grid
        for row in range(gc.GRID_SIZE.value[0]):
            for col in range(gc.GRID_SIZE.value[1]):
                wordle.draw_grid_char(row, col)

        # Update the display
        pygame.display.flip()

        # Limit frames per second (FPS)
        pygame.time.Clock().tick(gc.FPS.value)  # Limit to 60 frames per second


if __name__ == "__main__":
    main()
