import pygame
import sys
import random

# --- Config ---
CELL_SIZE = 20
GRID_WIDTH = 30   # number of cells horizontally
GRID_HEIGHT = 20  # number of cells vertically
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
FPS = 10  # snake speed (increase to make game faster)

# Colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 155, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# --- Helper functions ---
def random_food_position(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_rect(screen, pos, color):
    x, y = pos
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)

# --- Game setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)

def show_text(surface, text, x, y, color=WHITE):
    img = font.render(text, True, color)
    surface.blit(img, (x, y))

def game_loop():
    # initial snake: center, length 3, moving right
    start_x = GRID_WIDTH // 2
    start_y = GRID_HEIGHT // 2
    snake = [(start_x - i, start_y) for i in range(3)]  # head is snake[0]
    direction = RIGHT
    next_direction = RIGHT
    food = random_food_position(snake)
    score = 0
    game_over = False

    while True:
        # --- Events ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_UP) and direction != DOWN:
                    next_direction = UP
                elif event.key in (pygame.K_s, pygame.K_DOWN) and direction != UP:
                    next_direction = DOWN
                elif event.key in (pygame.K_a, pygame.K_LEFT) and direction != RIGHT:
                    next_direction = LEFT
                elif event.key in (pygame.K_d, pygame.K_RIGHT) and direction != LEFT:
                    next_direction = RIGHT
                elif event.key == pygame.K_r and game_over:
                    return  # restart the game loop from main

        if not game_over:
            direction = next_direction
            head_x, head_y = snake[0]
            dx, dy = direction
            new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)  # wrap-around

            # Check collisions with self
            if new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)  # move head

                # Check food
                if new_head == food:
                    score += 1
                    food = random_food_position(snake)
                    # (Do not pop tail; snake grows)
                else:
                    snake.pop()  # move forward (remove tail)

        # --- Drawing ---
        screen.fill(BLACK)

        # draw grid (subtle)
        for x in range(0, SCREEN_WIDTH, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, GRAY, (0, y), (SCREEN_WIDTH, y))

        # draw food
        draw_rect(screen, food, RED)

        # draw snake (head brighter)
        if snake:
            draw_rect(screen, snake[0], GREEN)
            for segment in snake[1:]:
                draw_rect(screen, segment, DARK_GREEN)

        # HUD
        show_text(screen, f"Score: {score}", 10, 6)

        if game_over:
            # overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))  # translucent black
            screen.blit(overlay, (0, 0))
            show_text(screen, "GAME OVER", SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 30, WHITE)
            show_text(screen, f"Final Score: {score}", SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 6, WHITE)
            show_text(screen, "Press R to Restart or Close Window to Exit", SCREEN_WIDTH // 2 - 220, SCREEN_HEIGHT // 2 + 46, WHITE)

        pygame.display.flip()
        clock.tick(FPS)

def main():
    while True:
        game_loop()  # returns when player restarts; loop continues

if __name__ == "__main__":
    main()
