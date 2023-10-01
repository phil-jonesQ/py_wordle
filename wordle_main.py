"""
Simple Wordle Clone
phil.jones.24.4@gmail.com
"""

import sys
import pygame
from setup import Setup

# Create the setup object
su = Setup()


def main():
    """
    Main game loop function
    """
    # Initialize Pygame
    pygame.init()

    pygame.display.set_caption(su.app_name)

    # Main game loop
    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Clear the screen with background color
        su.surface.fill(su.bg_colour)

        # Draw your graphics here
        pygame.draw.rect(su.surface,
                         (255, 0, 0),
                         (50, 50, 100, 100))

        # Update the display
        pygame.display.flip()

        # Limit frames per second (FPS)
        pygame.time.Clock().tick(60)  # Limit to 60 frames per second


if __name__ == "__main__":
    main()
