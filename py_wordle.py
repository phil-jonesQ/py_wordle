"""
Simple Wordle Clone
phil.jones.24.4@gmail.com
"""

import argparse
import random
import sys
from pathlib import Path

import pygame
from config import GameConstants as gc
from grid_cell import GridCell
from display import Display
from audio import AudioFeedback


class Wordle:
    """
    Wordle main game class
    """
    def __init__(self, debug=False):
        self.debug = debug
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
            'lose': False,
            'game_over': False
        }
        self.status_message = ""

        # Load the random word and words in
        self.the_word, self.words = self.load_random_word()
        self.valid_guesses = set(self.load_word_list("guess_words.txt"))
        self.valid_guesses.update(self.words)

        # Initialise the letter grid
        self.letter_store = [['_' for _ in range(gc.GRID_SIZE.value[1])]
                             for _ in range(gc.GRID_SIZE.value[0])]
        self.grid_state = {(row, col): 'DEFAULT'
                           for row in range(gc.GRID_SIZE.value[0])
                           for col in range(gc.GRID_SIZE.value[1])}

        if self.debug:
            print(f"Debug: secret word is {self.the_word}")

    @staticmethod
    def load_word_list(filename):
        """Load and uppercase a newline-delimited word list."""
        wordlist_path = Path(__file__).with_name(filename)
        try:
            with wordlist_path.open("r", encoding="utf8") as file:
                words = [line.strip().upper() for line in file.readlines()]
        except FileNotFoundError as file_error:
            print("File not found", file_error)
            sys.exit(1)

        return words

    @staticmethod
    def load_random_word():
        """
        Function to load the word_list
        Returns a random word string
        """
        words = Wordle.load_word_list("wordlist.txt")
        # Select a random word for the player to guess
        word_to_guess = random.choice(words)
        # word_to_guess = "ALLOW" # Input "LOLLY" to test
        # Result should be Y Y G _ _ _
        return word_to_guess, words

    def update_score(self):
        """
        Decrement the score
        """
        if self.game_data['lose']:
            self.game_data['score'] = 0
        elif self.game_data['win']:
            return
        else:
            self.game_data['score'] -= 10

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
        cell_update.vibrate_cell()

    def process_results(self, current_row):
        """
        Compare the guessed word against
        the_word and determine grid state
        """
        current_guess = self.decode_guess(current_row)
        translate_guess = self.translate_guess(current_guess)

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
        result = [' '] * len(self.the_word)

        # Make a copy of the word and guess as lists
        the_word_copy = list(self.the_word)
        the_guess_copy = list(guess)

        # Iterate through the guess and mark the correct letters
        for index, char in enumerate(guess):
            if char == self.the_word[index]:
                result[index] = 'G'
                the_guess_copy[index] = '0'  # Marked as checked
                the_word_copy.remove(char)

        # Iterate through the word and mark the misplaced letters
        for index, char in enumerate(the_guess_copy):
            if char != '0':
                if char in the_word_copy:
                    result[index] = 'Y'
                    the_guess_copy[index] = '0'  # Marked as checked
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
        return False

    def add_letter(self, current_row, current_col, letter):
        """Add a letter if the current guess has room; return the new column."""
        if current_col >= gc.GRID_SIZE.value[1]:
            return current_col

        self.letter_store[current_row][current_col] = letter
        self.status_message = ""
        return current_col + 1

    def remove_letter(self, current_row, current_col):
        """Remove the previous letter if one exists; return the new column."""
        if current_col == 0:
            return current_col

        current_col -= 1
        self.letter_store[current_row][current_col] = '_'
        self.status_message = ""
        return current_col

    def submit_guess(self, current_row):
        """Validate and score the current row. Return whether it was submitted."""
        if self.decode_guess(current_row).count('_'):
            self.status_message = "Enter a five-letter word"
            return False
        if not self.is_it_a_word(current_row):
            self.status_message = "Not in word list"
            return False

        self.status_message = ""
        self.process_results(current_row)
        self.update_score()
        self.have_we_won(current_row)
        return True

    def is_it_a_word(self, current_row):
        """
        Check if the word_store matches the_word
        Returns True if the word is "valid", False otherwise
        """
        current_guess = self.decode_guess(current_row)
        # Convert to a string
        guessed_word = "".join(current_guess)

        return guessed_word in self.valid_guesses

    def draw_title(self):
        """
        Draw the title to the screen
        Also, if we have lost, reveal the word
        """
        ui_area = GridCell(10, 10)
        ui_area.fill_ui_area("UI")
        string_to_render = gc.APP_NAME.value
        if self.game_data.get('lose'):
            string_to_render = self.the_word
        if self.game_data.get('win'):
            string_to_render = "YOU WON!"
        for i, letter in enumerate(list(string_to_render)):
            if i % 2 == 0:
                colour = "GREEN"
            elif i == len(string_to_render) - 1:
                colour = "GREY"
            else:
                colour = "YELLOW"
            display = Display((gc.CELL_SIZE.value * 1.6) + i * 25,
                              gc.WINDOW_HEIGHT.value // 1.43,
                              gc.COLOURS.value[f"{colour}"],
                              "large",
                              letter,
                              True)
            display.draw()
        if self.status_message:
            display = Display(gc.WINDOW_WIDTH.value // 4,
                              gc.WINDOW_HEIGHT.value // 1.3,
                              gc.COLOURS.value["WHITE"],
                              "small",
                              self.status_message,
                              False)
            display.draw()
        if self.game_data.get('game_over'):
            go_message = "GAME OVER - SPACE TO PLAY AGAIN"
            score_message = f"Score: {self.game_data.get('score')}"
            display = Display((gc.WINDOW_WIDTH.value // 6),
                              gc.WINDOW_HEIGHT.value // 1.2,
                              gc.COLOURS.value["WHITE"],
                              "large",
                              go_message,
                              False)
            display.draw()
            self.update_score()
            display = Display((gc.WINDOW_WIDTH.value // 6),
                              gc.WINDOW_HEIGHT.value // 1.1,
                              gc.COLOURS.value["WHITE"],
                              "large",
                              score_message,
                              False)
            display.draw()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Play a simple Wordle clone.")
    parser.add_argument(
        "-d", "--debug", action="store_true",
        help="print the secret word at the start of each round")
    return parser.parse_args(argv)


def main(argv=None):
    """
    Main game loop function
    """
    args = parse_args(argv)

    # Create a Game Instance
    wordle = Wordle(debug=args.debug)
    audio = AudioFeedback()
    current_col = wordle.game_state.get('current_col')
    current_row = wordle.game_state.get('current_row')

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
                if pygame.K_a <= event.key <= pygame.K_z\
                        and not wordle.game_data['game_over']:
                    key_char = chr(event.key).upper()
                    next_col = wordle.add_letter(
                        current_row, current_col, key_char)
                    if next_col != current_col:
                        audio.play("type")
                    current_col = next_col
                if event.key == pygame.K_BACKSPACE\
                        and not wordle.game_data['game_over']:
                    next_col = wordle.remove_letter(current_row, current_col)
                    if next_col != current_col:
                        audio.play("type")
                    current_col = next_col
                if event.key == pygame.K_RETURN\
                        and not wordle.game_data['game_over']:
                    if wordle.submit_guess(current_row):
                        if wordle.game_data['win']:
                            audio.play("win")
                        elif current_row == gc.GRID_SIZE.value[0] - 1:
                            wordle.game_data['lose'] = True
                            wordle.game_data['game_over'] = True
                            audio.play("lose")
                        else:
                            audio.play("submit")
                        # Increment the row and reset the col
                        current_row = current_row + 1
                        current_col = 0
                    else:
                        audio.play("invalid")
                if event.key == pygame.K_SPACE\
                        and wordle.game_data['game_over']:
                    wordle = Wordle(debug=args.debug)
                    current_col = wordle.game_state.get('current_col')
                    current_row = wordle.game_state.get('current_row')

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
