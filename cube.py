import pygame
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cube")

# Define cube vertices
vertices = [
    [100, 100, 100],
    [100, 100, -100],
    [100, -100, 100],
    [100, -100, -100],
    [-100, 100, 100],
    [-100, 100, -100],
    [-100, -100, 100],
    [-100, -100, -100]
]

# Define cube edges
edges = [
    (0, 1),
    (1, 3),
    (3, 2),
    (2, 0),
    (4, 5),
    (5, 7),
    (7, 6),
    (6, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7)
]

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    screen.fill(WHITE)

    for edge in edges:
        start = vertices[edge[0]]
        end = vertices[edge[1]]
        pygame.draw.line(screen, BLACK, (start[0] + WIDTH // 2, start[1] + HEIGHT // 2), (end[0] + WIDTH // 2, end[1] + HEIGHT // 2), 2)

    pygame.display.flip()

# Quit Pygame
pygame.quit()

