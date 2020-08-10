import pygame
import helper_fxns
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
week = 1

# Create skills
skills = []
skills.append(objects.Skill("Intonation"))
skills.append(objects.Skill("Memorization"))
skills.append(objects.Skill("Musicality"))
skills.append(objects.Skill("Performance"))
skills.append(objects.Skill("Blend"))
# Keeps track of skill points acquired from gigs, weeks, etc.
acquired_skill_points = 5

# Create songs
songs = []
songs.append(objects.Song(title='Happy Birthday'))
songs.append(objects.Song(title='Sally in our Alley (Rat)'))
songs.append(objects.Song(title='Bridge Over Troubled Water'))
songs.append(objects.Song(title='Get Ready'))
songs.append(objects.Song(title='Fly Me to the Moon'))

# Variable for loop
running = True

# For not, default state is rehearsal.
rehearsal_state = scenes.Rehearsal(screen, week, songs, skills, acquired_skill_points)

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
    clock.tick(30)
