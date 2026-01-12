import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 900, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pong Game")

WHITE, BLACK = (255, 255, 255), (0, 0, 0)
clock = pygame.time.Clock()

# Sound (placeholder, not used)
hit_sound = None

# Paddles
player = pygame.Rect(20, HEIGHT//2 - 40, 10, 80)
computer = pygame.Rect(WIDTH - 30, HEIGHT//2 - 40, 10, 80)

# Ball
ball = pygame.Rect(WIDTH//2, HEIGHT//2, 15, 15)
ball_speed_x, ball_speed_y = 5, 5

# Score
player_score, computer_score = 0, 0
font = pygame.font.Font(None, 40)

paused = False
difficulty = "Medium"

def ai_speed():
    return {"Easy": 3, "Medium": 5, "Hard": 7}[difficulty]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = not paused

    if not paused:
        keys = pygame.key.get_pressed()

        # Player movement
        if (keys[pygame.K_w] or keys[pygame.K_UP]) and player.top > 0:
            player.y -= 6
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]) and player.bottom < HEIGHT:
            player.y += 6

        # AI movement
        if computer.centery < ball.centery:
            computer.y += ai_speed()
        if computer.centery > ball.centery:
            computer.y -= ai_speed()

        # Ball movement
        ball.x += ball_speed_x
        ball.y += ball_speed_y

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            ball_speed_y *= -1

        if ball.colliderect(player) or ball.colliderect(computer):
            ball_speed_x *= -1

        if ball.left <= 0:
            computer_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)

        if ball.right >= WIDTH:
            player_score += 1
            ball.center = (WIDTH//2, HEIGHT//2)

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, player)
    pygame.draw.rect(screen, WHITE, computer)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH//2, 0), (WIDTH//2, HEIGHT))

    p_text = font.render(str(player_score), True, WHITE)
    c_text = font.render(str(computer_score), True, WHITE)
    screen.blit(p_text, (WIDTH//2 - 50, 20))
    screen.blit(c_text, (WIDTH//2 + 30, 20))

    if paused:
        pause_text = font.render("PAUSED", True, WHITE)
        screen.blit(pause_text, (WIDTH//2 - 60, HEIGHT//2))

    pygame.display.flip()
    clock.tick(60)
