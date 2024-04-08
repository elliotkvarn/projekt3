import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up display
WINDOW_WIDTH = 600  # Reduced window width
WINDOW_HEIGHT = 600
FPS = 60
LANE_WIDTH = WINDOW_WIDTH // 4
NOTE_WIDTH = LANE_WIDTH // 2
NOTE_HEIGHT = 20
HIT_AREA_HEIGHT = 80  # Increased hit area height
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (200, 200, 200)  # Light gray for button boxes

# Game variables
running = True

# Define Note class
class Note:
    def __init__(self, lane, time):
        self.lane = lane
        self.time = time
        self.y = -((WINDOW_HEIGHT - HIT_AREA_HEIGHT) * time / 3000) - NOTE_HEIGHT  # Start above the screen
        self.speed = (WINDOW_HEIGHT - HIT_AREA_HEIGHT) / 3000  # Adjust speed so it reaches the hit area in 3 seconds
        self.color = GREEN  # Green for now
        self.hit = False  # Flag to track if note is hit

    def move(self):
        self.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, self.color, (self.lane * LANE_WIDTH + (LANE_WIDTH - NOTE_WIDTH) // 2, self.y, NOTE_WIDTH, NOTE_HEIGHT))

# Predetermined notes
notes_sequence = [
    {"lane": 0, "time": 1000},  # Example note at time 1000 ms in lane 0
    {"lane": 1, "time": 2000},  # Example note at time 2000 ms in lane 1
    # Add more notes as needed
]

# Create Note objects from the notes_sequence
notes = [Note(note["lane"], note["time"]) for note in notes_sequence]

# Text rendering
font = pygame.font.Font(None, 24)
score_display_time = 500  # Time in milliseconds to display score feedback

# Function to handle button press
def handle_button_press(lane):
    for note in notes:
        if note.lane == lane and abs(note.y - (WINDOW_HEIGHT - HIT_AREA_HEIGHT)) < 10:  # Adjust hit range
            note.hit = True
            accuracy = abs(note.time - pygame.time.get_ticks())
            if accuracy <= 50:
                score_text = font.render("Perfect! 300", True, BLACK)
            elif accuracy <= 200:
                score_text = font.render("Good! 100", True, BLACK)
            else:
                score_text = font.render("Miss! 0", True, BLACK)
            screen.blit(score_text, (note.lane * LANE_WIDTH, WINDOW_HEIGHT // 2))
            pygame.display.update()  # Update the display after blitting text
            pygame.time.delay(score_display_time)  # Delay to display score

# Main game loop
while running:
    screen.fill(WHITE)

    # Draw rectangle indicating perfect hit position
    pygame.draw.rect(screen, BLUE, (0, WINDOW_HEIGHT - HIT_AREA_HEIGHT, WINDOW_WIDTH, HIT_AREA_HEIGHT))

    # Draw button labels and colored boxes
    button_labels = ["D", "F", "J", "K"]
    for i, label in enumerate(button_labels):
        # Draw colored boxes
        pygame.draw.rect(screen, BUTTON_COLOR, ((2 * i) * (WINDOW_WIDTH // 8), WINDOW_HEIGHT - HIT_AREA_HEIGHT, WINDOW_WIDTH // 4, HIT_AREA_HEIGHT))
        # Draw button labels
        text = font.render(label, True, BLACK)
        text_rect = text.get_rect(center=((2 * i + 1) * (WINDOW_WIDTH // 8), WINDOW_HEIGHT - HIT_AREA_HEIGHT // 2))
        screen.blit(text, text_rect)

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
        if note.y > WINDOW_HEIGHT and not note.hit:
            note.color = RED  # Change color to indicate a missed note

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
