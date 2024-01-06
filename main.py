import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH, PADDLE_HEIGHT = 100, 20
BALL_RADIUS = 10
BRICK_WIDTH, BRICK_HEIGHT = 80, 30
BRICK_ROWS = 5
BRICK_COLS = 10
WALL_PADDING = 50  # Padding above the wall
HIGH_SCORE_FILE = "data.txt"  # File to store the high score

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Game")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Paddle
paddle = pygame.Rect((WIDTH - PADDLE_WIDTH) // 2, HEIGHT - PADDLE_HEIGHT - 10, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
ball_speed = [5, 5]

# Bricks
bricks = []
for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick = pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + WALL_PADDING, BRICK_WIDTH, BRICK_HEIGHT)
        # Generate a random color for each brick
        brick_color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
        bricks.append((brick, brick_color))

# Score and High Score
score = 0
high_score = 0

# Read the high score from the file
try:
    with open(HIGH_SCORE_FILE, "r") as file:
        content = file.read().strip()
        high_score = int(content) if content.isdigit() else 0
except FileNotFoundError:
    # If the file doesn't exist, create it with an initial high score of 0
    with open(HIGH_SCORE_FILE, "w") as file:
        file.write("0")


# Game over flag
game_over = False

# Countdown before the ball starts moving
countdown_seconds = 3
start_time = time.time()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Save the high score before quitting
            with open(HIGH_SCORE_FILE, "w") as file:
                file.write(str(high_score))
            pygame.quit()
            sys.exit()

    # Display the countdown
    current_time = time.time()
    elapsed_time = current_time - start_time
    countdown = countdown_seconds - int(elapsed_time)
    if countdown > 0:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        text = font.render(str(countdown), True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.delay(1000)
        continue

    if not game_over:
        keys = pygame.key.get_pressed()
        # Move paddle with left and right arrow keys
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-5, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(5, 0)

        # Move the ball
        ball.move_ip(ball_speed[0], ball_speed[1])

        # Ball collisions with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_speed[0] = -ball_speed[0]
        if ball.top <= 0:
            ball_speed[1] = -ball_speed[1]

        # Ball collisions with paddle
        if ball.colliderect(paddle):
            ball_speed[1] = -ball_speed[1]

        # Ball collisions with bricks
        for brick, brick_color in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove((brick, brick_color))
                ball_speed[1] = -ball_speed[1]
                score += 10
                break  # Exit the loop after breaking the first brick

        # Check for game over (ball falls off the bottom)
        if ball.bottom >= HEIGHT:
            game_over = True
            if score > high_score:
                high_score = score

    # Draw everything
    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, paddle)
    pygame.draw.ellipse(screen, WHITE, ball)
    for brick, brick_color in bricks:
        pygame.draw.rect(screen, brick_color, brick)

    # Draw the score and high score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"High Score: {high_score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 10, 10))

    # Display "Game Over" message
    if game_over:
        game_over_text = font.render("Game Over! ", True, WHITE)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(game_over_text, game_over_rect)

        # Reset the game state after a delay
        pygame.display.flip()
        pygame.time.delay(3000)  # Pause for 3 seconds
        game_over = False
        ball.x = WIDTH // 2
        ball.y = HEIGHT // 2
        paddle.x = (WIDTH - PADDLE_WIDTH) // 2
        bricks = [(pygame.Rect(col * BRICK_WIDTH, row * BRICK_HEIGHT + WALL_PADDING, BRICK_WIDTH, BRICK_HEIGHT), (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))) for row in range(BRICK_ROWS) for col in range(BRICK_COLS)]
        score = 0
        start_time = time.time()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)
