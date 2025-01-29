import pygame
import sys

pygame.init()
# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong")
# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
# Paddle properties
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
paddle_speed = 5
# Ball properties
BALL_SIZE = 20
ball_speed_x = 4
ball_speed_y = 4
acceleration_factor = 1.1  # Увеличение скорости при каждом ударе
# Create paddles and ball
left_paddle = pygame.Rect(30, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 30 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
# Scores
left_score = 0
right_score = 0
# Font for displaying score and game over message
font = pygame.font.Font(None, 74)
game_over_font = pygame.font.Font(None, 100)
# Main game loop variables
clock = pygame.time.Clock()
game_running = True
game_over = False
winner = None

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # Restart the game
            left_score = 0
            right_score = 0
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = 4
            ball_speed_y = 4
            game_running = True
            game_over = False
            winner = None

    if game_running:
        # Get keys pressed
        keys = pygame.key.get_pressed()
        # Move left paddle
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= paddle_speed
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += paddle_speed
        # Move right paddle
        if keys[pygame.K_UP] and right_paddle.top > 0:
            right_paddle.y -= paddle_speed
        if keys[pygame.K_DOWN] and right_paddle.bottom < HEIGHT:
            right_paddle.y += paddle_speed
        # Move ball
        ball.x += ball_speed_x
        ball.y += ball_speed_y
        # Ball collision with top and bottom walls
        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1
        # Ball collision with paddles
        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            ball_speed_x *= -1
            # Increase speed with each paddle hit
            if ball_speed_x > 0:
                ball_speed_x *= acceleration_factor
            else:
                ball_speed_x *= acceleration_factor
            if ball_speed_y > 0:
                ball_speed_y *= acceleration_factor
            else:
                ball_speed_y *= acceleration_factor
        # Ball out of bounds
        if ball.left <= 0:
            right_score += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = 4  # Reset speed after scoring
            ball_speed_y = 4
        elif ball.right >= WIDTH:
            left_score += 1
            ball.x, ball.y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
            ball_speed_x = -4  # Reset speed after scoring
            ball_speed_y = 4

        # Check for game over condition
        if left_score >= 10:
            game_running = False
            game_over = True
            winner = "Left Player"
        elif right_score >= 10:
            game_running = False
            game_over = True
            winner = "Right Player"

    # Fill screen and draw objects
    screen.fill(BLACK)
    if game_running:
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
        # Display scores
        left_score_text = font.render(str(left_score), True, WHITE)
        right_score_text = font.render(str(right_score), True, WHITE)
        screen.blit(left_score_text, (WIDTH // 4, 30))
        screen.blit(right_score_text, (WIDTH * 3 // 4, 30))
    else:
        # Display game over message
        game_over_text = game_over_font.render("Game Over", True, WHITE)
        winner_text = game_over_font.render(f"{winner} Wins!", True, WHITE)
        restart_text = font.render("Press Space to Restart", True, WHITE)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        screen.blit(winner_text, (WIDTH // 2 - winner_text.get_width() // 2, HEIGHT // 2))
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))

    # Update display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 frames per second