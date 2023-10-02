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
    return word_to_guess


def main():
    """
    Main game loop function
    """
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption(su.app_name)

    # Load word list
    the_word = load_random_word()

    # Initialise the letter 
    # Need to make a spare end column for backspace
    letter_store = [[ '_' for _ in range(su.grid_size[1] + 1)] for _ in range(su.grid_size[0])]

    # Initialise the guessed word
    print("Debug here is the word " + the_word)
    guessed_word = ['_' for _ in the_word]

    # Initialise the row and col counter
    current_row = 0
    current_col = 0
    check_flag = False

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
                        print("Congratulations! You guessed the word:", the_word)

                    check_flag = True
                    current_row = current_row + 1
                    current_col = 0
                    if current_row == su.grid_size[0]:
                        current_row = 0
                        current_col = 0
                    # Add logic to check if we got any letters etc
                if event.key == pygame.K_BACKSPACE:
                    letter_store[current_row][current_col - 1] = '_'
                    current_col = current_col - 1
                    if current_col <= 0:
                        current_col = 0



            if event.type == pygame.KEYDOWN and event.key >= 97 and event.key <= 122:
                check_flag = False
                key_char = chr(event.key).upper()
                letter_store[current_row][current_col] = key_char
      
                # Increment the col
                current_col = current_col + 1
                if current_col >= su.grid_size[1]:
                    current_col = su.grid_size[1]
                

        # Clear the screen with background color
        su.surface.fill(su.bg_colour)
        
        # Draw the game 
        draw_grid(su.surface)
        font = pygame.font.Font(None, 36)
        
        #print(letter_store)
        for row in range(su.grid_size[0]):
             for col in range(su.grid_size[1]):
                key_char_text = font.render(letter_store[row][col], True, su.grey)
                if check_flag:
                    if letter_store[row][col] == the_word[col]:
                        key_char_text = font.render(letter_store[row][col], True, su.green)
                    if letter_store[row][col] in the_word and not letter_store[row][col] == the_word[col]:
                        key_char_text = font.render(letter_store[row][col], True, su.yellow)
                
                su.surface.blit(key_char_text, (col * su.cell_size + su.cell_size // 2 - key_char_text.get_width() // 2,
                                                row * su.cell_size + su.cell_size // 2 - key_char_text.get_height() // 2))
                
        
        # Update the display
        pygame.display.flip()

        # Limit frames per second (FPS)
        pygame.time.Clock().tick(60)  # Limit to 60 frames per second


if __name__ == "__main__":
    main()
