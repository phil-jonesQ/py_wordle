import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load word list from a file
with open("wordlist.txt", "r") as file:
    words = [line.strip().upper() for line in file.readlines()]

# Select a random word for the player to guess
word_to_guess = random.choice(words)
print("Debug here is the word " + word_to_guess)
guessed_word = ['_' for _ in word_to_guess]

# Initialize Pygame window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Wordle Game")

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key >= 97 and event.key <= 122:
            # Check if the guessed letter is in the word
            key_char = chr(event.key).upper()
            if key_char in word_to_guess:
                letter_indices = [i for i, letter in enumerate(word_to_guess) if letter == key_char]
                for index in letter_indices:
                    guessed_word[index] = key_char

    # Check if the player has guessed the word correctly
    if ''.join(guessed_word) == word_to_guess:
        print("Congratulations! You guessed the word:", word_to_guess)
        pygame.quit()
        sys.exit()

    # Draw the game screen
    window.fill(WHITE)
    font = pygame.font.Font(None, 36)
    guessed_text = font.render(" ".join(guessed_word), True, BLACK)
    window.blit(guessed_text, (WIDTH // 2 - guessed_text.get_width() // 2, HEIGHT // 2 - guessed_text.get_height() // 2))

    pygame.display.flip()
