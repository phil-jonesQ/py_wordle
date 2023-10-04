"""
Simple Wordle Clone
phil.jones.24.4@gmail.com
"""

import sys
import random
import pygame
from setup import Setup

# Create the setup object
su = Setup()


def have_we_won(current_row, word_store, the_word):
    """
	Check if the word_store matches the_word
	Returns True if won, False otherwise
	"""
    guessed_word_extract = []

    # Scan current row and build the word
    for index in range(su.grid_size[1]):
        guessed_word_extract.append(word_store[current_row][index])
    
    # Convert to a string
    guessed_word = "".join(guessed_word_extract)

    # Return the result
    if guessed_word == the_word:
        return True
    else:
        return 
    
def is_it_a_word(current_row, word_store, words):
    """
	Check if the word_store matches the_word
	Returns True if won, False otherwise
	"""
    guessed_word_extract = []

    # Scan current row and build the word
    for index in range(su.grid_size[1]):
        guessed_word_extract.append(word_store[current_row][index])
    
    # Convert to a string
    guessed_word = "".join(guessed_word_extract)

    # Return the result
    if guessed_word in words:
        return True
    else:
        return False


def draw_grid(surface):
    """
    Draw the grid on the surface
    """
    # Draw the grid
    for row in range(su.grid_size[0]):
        for col in range(su.grid_size[1]):
            pygame.draw.rect(surface,
                            (su.cyan),
                            (col * su.cell_size,
                             row * su.cell_size,
                             su.cell_size,
                             su.cell_size), 2)


def load_random_word():
    """
    Function to load the word_list
    Returns a random word string
    """
    # Load word list from a file
    try:
        with open("wordlist.txt", "r") as file:
            words = [line.strip().upper() for line in file.readlines()]
    except FileNotFoundError as file_error:
        print("File not found", file_error)
        sys.exit(1)
    # Select a random word for the player to guess
    word_to_guess = random.choice(words)
    return word_to_guess, words


def reset_variables():
    # Initialise variables
    global current_row, current_col, check_flag, win, loose, game_over, the_word, letter_store, score, words, not_a_word_flag
    current_row = 0
    current_col = 0
    score = 90
    check_flag = False
    win = False
    loose = False
    game_over = False
    not_a_word_flag = False

    # Load the random word and words in
    the_word, words = load_random_word()


    # Initialise the letter 
    # Need to make a spare end column for backspace
    letter_store = [[ '_' for _ in range(su.grid_size[1] + 1)] for _ in range(su.grid_size[0])]

    # Initialise the guessed word
    print("Debug here is the word " + the_word)


def main():
    """
    Main game loop function
    """
    # Initialise Pygame
    pygame.init()
    pygame.display.set_caption(su.app_name)

    # Initialise the font
    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 22)

    # call the initial resest function
    global current_row, current_col, check_flag, win, loose, game_over, the_word, letter_store, score, words, not_a_word_flag
    reset_variables()


    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and current_col == su.grid_size[1]:
                    if have_we_won(current_row, letter_store, the_word):
                        win = True
                    if not is_it_a_word(current_row, letter_store, words):
                        not_a_word_flag = True
                        break
                    check_flag = True
                    score -= 10
                    current_row = current_row + 1
                    current_col = 0
                    if current_row == su.grid_size[0]:
                        if not win:
                            loose = True
                        current_row = 0
                        current_col = 0

                if event.key == pygame.K_BACKSPACE:
                    letter_store[current_row][current_col - 1] = '_'
                    current_col = current_col - 1
                    if current_col <= 0:
                        current_col = 0

                if event.key == pygame.K_SPACE and game_over:
                    game_over = False
                    reset_variables()

            if event.type == pygame.KEYDOWN and event.key >= 97 and event.key <= 122:
                not_a_word_flag = False
                check_flag = False
                key_char = chr(event.key).upper()
                letter_store[current_row][current_col] = key_char
      
                # Increment the col
                current_col = current_col + 1
                if current_col >= su.grid_size[1]:
                    current_col = su.grid_size[1]
                

        # Clear the screen with background color
        su.surface.fill(su.bg_colour)

        #
        # Draw the game UI
        #

        # Draw the grid
        draw_grid(su.surface)

        # Populate the letters in the grid
        for row in range(su.grid_size[0]):
             for col in range(su.grid_size[1]):
                key_char_text = font.render(letter_store[row][col], True, su.grey)
                if check_flag:
                    if letter_store[row][col] == the_word[col]:
                        key_char_text = font.render(letter_store[row][col], True, su.green)
                    if not letter_store[row][col] == the_word[col]:
                            if letter_store[row][col] in the_word:
                                key_char_text = font.render(letter_store[row][col], True, su.yellow)
                                
                # Draw to the screen
                su.surface.blit(key_char_text, (col * su.cell_size + su.cell_size // 2 - key_char_text.get_width() // 2,
                                                row * su.cell_size + su.cell_size // 2 - key_char_text.get_height() // 2))
        # Draw ui messages  
        if win or loose:
            game_over = True
            if not loose:
                win_message1 = font_small.render("Congratulations!", True, su.green)
                intermediate_message2 = font_small.render("You guessed correctly!",True, su.green)
            else:
                win_message1 = font_small.render("Unlucky...", True, su.red)
                intermediate_message2 = font_small.render("You ran out of guesses!",True, su.black)
            intermediate_message3 = font_small.render(f"The word was: {the_word}", True, su.black)
            intermediate_message4 = font_small.render(f"Your score was: {score}", True, su.black)
            su.surface.blit(win_message1,((su.cell_size * 5 + su.pad), (su.cell_size // 4)))
            su.surface.blit(intermediate_message2, ((su.cell_size * 5 + su.pad), (su.cell_size // 4 + win_message1.get_height())))
            su.surface.blit(intermediate_message3, ((su.cell_size * 5 + su.pad), (su.cell_size // 4 + win_message1.get_height() * 2)))
            su.surface.blit(intermediate_message4, ((su.cell_size * 5 + su.pad), (su.cell_size // 4 + win_message1.get_height() * 3)))

        if game_over:
            game_over_message1 = font_small.render("Game Over!", True, su.red)
            game_over_message2 = font_small.render("SPACE to restart", True, su.green)
            su.surface.blit(game_over_message1,((su.cell_size * 5 + su.pad), (su.window_height // 2)))
            su.surface.blit(game_over_message2,((su.cell_size * 5 + su.pad), (su.window_height // 2 + game_over_message2.get_height())))
        
        if not_a_word_flag:
            not_a_word_message = font_small.render("Not a valid word!", True, su.red)
            su.surface.blit(not_a_word_message,((su.cell_size * 5 + su.pad), (su.window_height // 2)))

        # Update the display
        pygame.display.flip()

        # Limit frames per second (FPS)
        pygame.time.Clock().tick(60)  # Limit to 60 frames per second


if __name__ == "__main__":
    main()
