import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Key mappings
KEY_MAPPING = {'d': 0, 'f': 1, 'j': 2, 'k': 3}

# Game area dimensions
GAME_AREA_WIDTH = 600
GAME_AREA_HEIGHT = 400
GAME_AREA_X = (SCREEN_WIDTH - GAME_AREA_WIDTH) // 2
GAME_AREA_Y = (SCREEN_HEIGHT - GAME_AREA_HEIGHT) // 2

# Lane dimensions
LANE_WIDTH = GAME_AREA_WIDTH // len(KEY_MAPPING)
LANE_HEIGHT = GAME_AREA_HEIGHT
LANE_X = GAME_AREA_X

# Note dimensions
NOTE_WIDTH = LANE_WIDTH
NOTE_HEIGHT = 20

# Note speed
NOTE_SPEED = 5

# Hit area marker dimensions
HIT_AREA_HEIGHT = NOTE_HEIGHT

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Keyboard Rhythm Game")

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# List to hold falling notes
falling_notes = []

# Function to create a new falling note
def create_note():
    lane_index = random.randint(0, len(KEY_MAPPING) - 1)
    x = LANE_X + lane_index * LANE_WIDTH
    y = 0
    note = {'rect': pygame.Rect(x, y, NOTE_WIDTH, NOTE_HEIGHT), 'color': RED, 'lane': lane_index}
    falling_notes.append(note)

# Function to draw falling notes
def draw_notes():
    for note in falling_notes:
        pygame.draw.rect(screen, note['color'], note['rect'])

# Function to move falling notes
def move_notes():
    for note in falling_notes:
        note['rect'].move_ip(0, NOTE_SPEED)

# Function to detect key presses
def check_key_press():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.unicode in KEY_MAPPING:
                key_index = KEY_MAPPING[event.unicode]
                for note in falling_notes:
                    if note['lane'] == key_index and is_hit(note['rect'], hit_areas[key_index]):
                        note['color'] = WHITE  # Change color when hit
                        # Additional actions when a note is hit can be added here

# Function to check if a note is hit
def is_hit(note_rect, hit_rect):
    return note_rect.colliderect(hit_rect)

# Main game loop
while True:
    screen.fill(BLACK)

    # Draw lines to represent the playing area
    pygame.draw.line(screen, WHITE, (GAME_AREA_X - 1, GAME_AREA_Y), (GAME_AREA_X - 1, GAME_AREA_Y + GAME_AREA_HEIGHT), 2)
    pygame.draw.line(screen, WHITE, (GAME_AREA_X + GAME_AREA_WIDTH, GAME_AREA_Y), (GAME_AREA_X + GAME_AREA_WIDTH, GAME_AREA_Y + GAME_AREA_HEIGHT), 2)

    # Draw hit area markers
    hit_areas = []
    for i in range(len(KEY_MAPPING)):
        hit_x = LANE_X + i * LANE_WIDTH
        hit_y = GAME_AREA_Y + GAME_AREA_HEIGHT - HIT_AREA_HEIGHT
        hit_area = pygame.Rect(hit_x, hit_y, NOTE_WIDTH, HIT_AREA_HEIGHT)
        hit_areas.append(hit_area)
        pygame.draw.rect(screen, WHITE, hit_area, 1)  # Hollow rectangle

    # Create new falling notes with a delay
    if random.randint(0, 100) < 3:  # Adjust this probability to control note frequency
        create_note()

    # Draw and move falling notes
    draw_notes()
    move_notes()

    # Check for key presses
    check_key_press()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(30)
