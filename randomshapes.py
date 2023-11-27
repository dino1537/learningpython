import pygame
import random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 30

# Colors
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Random Shapes")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # Generate a random position and size
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    size = random.randint(20, 100)

    # Generate a random color
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    # Randomly choose between drawing a circle or a rectangle
    if random.choice([True, False]):
        pygame.draw.circle(screen, color, (x, y), size)
    else:
        rect = pygame.Rect(x, y, size, size)
        pygame.draw.rect(screen, color, rect)

    pygame.display.flip()

    # Control the frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()
