# Candy Crush Game
# Developed by: Ekramul

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400
GRID_SIZE = 8
CANDY_SIZE = SCREEN_WIDTH // GRID_SIZE
FPS = 30
TOTAL_MOVES = 20  # Total number of moves allowed

# Load fruit images
fruit_images = [
    pygame.image.load('apple.png'),
    pygame.image.load('banana.png'),
    pygame.image.load('cherry.png'),
    pygame.image.load('grape.png'),
    pygame.image.load('orange.png')
]

# Scale images to fit the grid
fruit_images = [pygame.transform.scale(img, (CANDY_SIZE, CANDY_SIZE)) for img in fruit_images]

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Candy Crush")

# Create the grid with random fruits
grid = [[random.choice(fruit_images) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Initialize score and moves
score = 0
moves_left = TOTAL_MOVES

def draw_grid(selected=None):
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            rect = pygame.Rect(x * CANDY_SIZE, y * CANDY_SIZE, CANDY_SIZE, CANDY_SIZE)
            screen.blit(grid[y][x], rect)
            pygame.draw.rect(screen, pygame.Color("black"), rect, 1)

            # Highlight selected candy with a red border
            if selected and (x, y) == selected:
                pygame.draw.rect(screen, pygame.Color("red"), rect, 3)

def swap_candies(pos1, pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    grid[y1][x1], grid[y2][x2] = grid[y2][x2], grid[y1][x1]

def find_matches():
    matches = []
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            if x < GRID_SIZE - 2 and grid[y][x] == grid[y][x+1] == grid[y][x+2]:
                matches.append((x, y))
            if y < GRID_SIZE - 2 and grid[y][x] == grid[y+1][x] == grid[y+2][x]:
                matches.append((x, y))
    return matches

def remove_matches(matches):
    global score
    for x, y in matches:
        grid[y][x] = random.choice(fruit_images)
        score += 10  # Increase score for each match

def draw_score_and_moves():
    font = pygame.font.SysFont(None, 30)
    score_text = font.render(f"Score: {score}", True, pygame.Color("black"))
    moves_text = font.render(f"Moves Left: {moves_left}", True, pygame.Color("black"))
    screen.blit(score_text, (10, 10))
    screen.blit(moves_text, (SCREEN_WIDTH - 150, 10))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def start_screen():
    font = pygame.font.SysFont(None, 40)
    while True:
        screen.fill((255, 255, 255))
        draw_text("Fruits Crush", font, pygame.Color("black"), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
        draw_text("Developed by: Ekramul", font, pygame.Color("black"), screen, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4 + 40)

        # Draw buttons
        start_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, 50)
        exit_button = pygame.Rect(SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 60, SCREEN_WIDTH // 2, 50)

        pygame.draw.rect(screen, pygame.Color("green"), start_button)
        pygame.draw.rect(screen, pygame.Color("red"), exit_button)

        draw_text("Start", font, pygame.Color("white"), screen, start_button.centerx, start_button.centery)
        draw_text("Exit", font, pygame.Color("white"), screen, exit_button.centerx, exit_button.centery)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    return  # Start the game
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

def game_loop():
    global moves_left
    clock = pygame.time.Clock()
    selected = None

    running = True
    while running:
        screen.fill((255, 255, 255))
        draw_grid(selected)
        draw_score_and_moves()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                x //= CANDY_SIZE
                y //= CANDY_SIZE

                if selected:
                    swap_candies(selected, (x, y))
                    matches = find_matches()
                    if matches:
                        remove_matches(matches)
                        moves_left -= 1  # Decrease moves left after a valid swap
                    else:
                        swap_candies(selected, (x, y))  # Swap back if no match
                    selected = None
                else:
                    selected = (x, y)

        pygame.display.flip()
        clock.tick(FPS)

        # End game when no moves are left
        if moves_left <= 0:
            running = False

    pygame.quit()

if __name__ == "__main__":
    start_screen()
    game_loop()
