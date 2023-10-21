import pygame
import random
import sys



# Letter class
class Letter:

  def __init__(self, text, pos):
    self.text = text  
    self.pos = pos
    self.revealed = False
    self.angle = 180 # face down initially

  def draw(self, surface):
    font = pygame.font.SysFont("arial", 60)
    text_surface = font.render(self.text, True, (0,0,0))
    
    # Rotate surface by current angle
    rotated_surface = pygame.transform.rotate(text_surface, self.angle) 
    surface.blit(rotated_surface, self.pos)

  def reveal(self):
    self.revealed = True

# In game loop:

letters = [Letter(l, (x, y)) for l, x, y in zip("HELLO", [50]*5, [100, 150, 200, 250, 300])]

pygame.init()
surface = pygame.display.set_mode((300, 300))
font = pygame.font.Font(None, 36)

while True:

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
       pygame.quit()
       sys.exit()
       
  surface.fill((255,255,255))

  for letter in letters:
    if not letter.revealed:
      if letter.angle < 360: 
        letter.angle += 10 # Rotate letter
      if letter.angle >= 180:
        letter.reveal() # Flip complete
        
    letter.draw(surface)  

  pygame.display.update()
