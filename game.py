import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
FPS = 60
LANE_WIDTH = WINDOW_WIDTH // 4
NOTE_WIDTH = LANE_WIDTH // 2
NOTE_HEIGHT = 20
HIT_AREA_HEIGHT = 80
BUTTON_HEIGHT = 30  # Reduced button height
BUTTON_WIDTH = LANE_WIDTH  # Button width fills the whole lane
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)  # Adjusted gray color
RED = (255, 0, 0)
BLUE = (0, 0, 255)
TRANSPARENT = (0, 0, 0, 0)  # Transparent color

# Game variables
running = True
hit_area_highlight = False  # Flag to control hit area highlight

# Define Note class
class Note:
    def __init__(self, lane, delay):
        self.lane = lane
        self.delay = delay
        self.speed = (WINDOW_HEIGHT - HIT_AREA_HEIGHT) / 300  # Adjust speed so it reaches the hit area in 3 seconds
        self.spawn_y = -self.speed * delay
        self.color = BLUE  # Blue color for notes
        self.hit = False  # Flag to track if note is hit

    def move(self):
        self.spawn_y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.lane * LANE_WIDTH + (LANE_WIDTH - NOTE_WIDTH) // 2, self.spawn_y, NOTE_WIDTH, NOTE_HEIGHT))

# Predetermined notes
notes_sequence = [
    {"lane": 0, "delay": 1000},  # Example note with 1000 ms delay in lane 0
    {"lane": 1, "delay": 2000},  # Example note with 2000 ms delay in lane 1
    # Add more notes as needed
]

# Create Note objects from the notes_sequence
notes = [Note(note["lane"], note["delay"]) for note in notes_sequence]

# Text rendering
font = pygame.font.Font(None, 18)  # Adjusted font size

# Function to handle button press
def handle_button_press(lane):
    global hit_area_highlight
    for note in notes:
        if note.lane == lane and abs(note.spawn_y - (WINDOW_HEIGHT - HIT_AREA_HEIGHT)) < 10:  # Adjust hit range
            note.hit = True
            accuracy = abs(note.delay - pygame.time.get_ticks())
            if accuracy <= 50:
                score_text = font.render("Perfect! 300", True, WHITE)
            elif accuracy <= 200:
                score_text = font.render("Good! 100", True, WHITE)
            else:
                score_text = font.render("Miss! 0", True, WHITE)
            screen.blit(score_text, (note.lane * LANE_WIDTH, WINDOW_HEIGHT // 2))
            pygame.display.update()  # Update the display after blitting text
            pygame.time.delay(500)  # Delay to display score
            # Set flag to highlight hit area
            hit_area_highlight = True

# Main game loop
while running:
    screen.fill(WHITE)  # Background color

    # Draw transparent hit area
    pygame.draw.rect(screen, TRANSPARENT, (0, WINDOW_HEIGHT - HIT_AREA_HEIGHT, WINDOW_WIDTH, HIT_AREA_HEIGHT))

    # Draw button labels and colored boxes
    button_labels = ["D", "F", "J", "K"]
    for i, label in enumerate(button_labels):
        # Draw button labels
        text = font.render(label, True, (0, 0, 0))  # Adjusted to black color
        text_rect = text.get_rect(center=((i * LANE_WIDTH) + (LANE_WIDTH // 2), WINDOW_HEIGHT - (BUTTON_HEIGHT // 2)))
        screen.blit(text, text_rect)

    # Highlight hit area if a key was pressed
    if hit_area_highlight:
        pygame.draw.rect(screen, GRAY, (0, WINDOW_HEIGHT - HIT_AREA_HEIGHT, WINDOW_WIDTH, HIT_AREA_HEIGHT))

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Capture keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                handle_button_press(0)
            elif event.key == pygame.K_f:
                handle_button_press(1)
            elif event.key == pygame.K_j:
                handle_button_press(2)
            elif event.key == pygame.K_k:
                handle_button_press(3)

    # Move and draw notes
    for note in notes:
        note.move()
        note.draw()

        # Check for missed notes
        if note.spawn_y > WINDOW_HEIGHT and not note.hit:
            note.color = RED  # Change color to indicate a missed note

    # Reset hit area highlight flag
    hit_area_highlight = False

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
