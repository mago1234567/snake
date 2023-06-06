import pygame
import random

pygame.init()

# set up game window
window_width = 800
window_height = 600
game_window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Penalty Shootout")

# set up colors
white = (255, 255, 255)
black = (0, 0, 0)

# set up fonts
title_font = pygame.font.SysFont(None, 50)
text_font = pygame.font.SysFont(None, 30)

# set up variables
score = 0
attempts_left = 5

# set up goal post
goal_post_x = window_width // 2
goal_post_y = 100
goal_post_width = 200
goal_post_height = 300

# set up ball
ball_x = window_width // 2
ball_y = window_height - 50
ball_radius = 10
ball_speed = 5

# set up clock
clock = pygame.time.Clock()

# main game loop
running = True
while running:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # handle key presses
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT]:
        ball_x += ball_speed

    # handle ball movement
    ball_y -= ball_speed
    if ball_y < goal_post_y + goal_post_height and ball_x > goal_post_x - goal_post_width // 2 and ball_x < goal_post_x + goal_post_width // 2:
        score += 1
        ball_y = window_height - 50
        ball_x = random.randint(goal_post_x - goal_post_width // 2, goal_post_x + goal_post_width // 2)
        attempts_left -= 1
        if attempts_left == 0:
            running = False

    # draw game objects
    game_window.fill(white)
    pygame.draw.rect(game_window, black, (goal_post_x - goal_post_width // 2, goal_post_y, goal_post_width, goal_post_height), 2)
    pygame.draw.circle(game_window, black, (ball_x, ball_y), ball_radius)
    title_text = title_font.render("Penalty Shootout", True, black)
    game_window.blit(title_text, (window_width // 2 - title_text.get_width() // 2, 50))
    score_text = text_font.render(f"Score: {score}", True, black)
    game_window.blit(score_text, (10, 10))
    attempts_left_text = text_font.render(f"Attempts Left: {attempts_left}", True, black)
    game_window.blit(attempts_left_text, (10, 40))
    pygame.display.update()

    # limit frame rate
    clock.tick(60)

# quit game
pygame.quit()





