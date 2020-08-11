import pygame
import scenes
import objects
pygame.init()

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import (
#     K_UP,
#     K_DOWN,
#     K_LEFT,
#     K_RIGHT,
#     K_ESCAPE,
#     KEYDOWN,
#     QUIT,
# )

# Define constants for the screen width and height
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 775
SCREEN_CENTER = (SCREEN_WIDTH/2, SCREEN_HEIGHT/2)

# Define constants for black and white and fonts
black_color = (0, 0, 0)
white_color = (255, 255, 255)
text_font = pygame.font.SysFont('Arial', 30)
    
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()

# Create player entity
player = objects.Player()

# Variable for loop
running = True

# For not, default state is rehearsal.
rehearsal_state = scenes.Rehearsal(screen, player)

# Main loop
while running:

    # for loop through the event queue
    events = pygame.event.get()
    for event in events:

        # Check for QUIT event. If QUIT, then set running to false.
        if event.type == pygame.QUIT:
            running = False

        # Check for KEYDOWN event
        elif event.type == pygame.KEYDOWN:
            # If the Esc key is pressed, then exit the main loop
            if event.key == pygame.K_ESCAPE:
                running = False

    rehearsal_state.render()
    rehearsal_state.handle_events(events)
    rehearsal_state.update()
    pygame.display.flip()
    clock.tick(50)
