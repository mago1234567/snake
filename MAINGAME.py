import pygame
import sys
import random
from pygame.math import Vector2
import time

class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

    def draw_snake(self):
        # Draws the snake on the screen
        for block in self.body:
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
            pygame.draw.rect(screen, (183, 111, 122), block_rect)

    def move_snake(self):
        # Moves the snake in a given direction
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        # Adds a new block to the snake's body
        self.new_block = True

    def add_wall(self):
        # Adds a new wall to the game
        self.new_block = True


class Fruit:
    def __init__(self, apple_image):
        self.apple_image = apple_image
        self.randomize()

    def draw_fruit(self, screen):
        # Draws the fruit on the screen
        fruit_rect = self.apple_image.get_rect(topleft=(self.pos.x * cell_size, self.pos.y * cell_size))
        screen.blit(self.apple_image, fruit_rect)

    def randomize(self):
        # Randomizes the position of the fruit
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit(apple_image)
        self.score = 0
        self.walls = []
        self.wall_pos = self.randomize_wall()

    def update(self):
        # Updates the game state
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        # Draws the fruit, snake, and walls on the screen
        self.fruit.draw_fruit(screen)
        self.snake.draw_snake()
        for item in self.walls:
            wall_rect = pygame.Rect(item.x * cell_size, item.y * cell_size, cell_size, cell_size)
            screen.blit(wall_image, wall_rect)

    def check_collision(self):
        # Checks for collisions between the snake and the fruit or walls
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 10
            self.snake.add_wall()
            wall_pos = self.randomize_wall()
            self.walls.append(wall_pos)
            eat_sound.play()

    def check_fail(self):
         # Checks for the snake hitting the walls or itself
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

        for wall in self.walls:
            if wall == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        # Ends the game, pauses and exits
        death_sound.play()
        time.sleep(0.5)
        pygame.quit()
        sys.exit()

    def randomize_wall(self):
        # Randomizes the position of a wall
        pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        while pos in self.snake.body or pos in self.walls:
            pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))
        return pos

# Creats grid from cell size and cell number
# Window is created from how big grid is and frame rate
pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()

# Sound and Images
death_sound = pygame.mixer.Sound("death_sound1.mp3")
eat_sound = pygame.mixer.Sound("eat_sound.mp3")
apple_image = pygame.image.load("apple.png")
apple_image = pygame.transform.scale(apple_image, (cell_size, cell_size))
wall_image = pygame.image.load("wall_image.png")
wall_image = pygame.transform.scale(wall_image, (cell_size, cell_size))
fruit = Fruit(apple_image)

# Set up timer for SCREEN_UPDATE event for every 150 milliseconds
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = Main()


while True:
    # The game ends if called
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        # Arrow keys are used to for the direction and movement of snake
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

# Fill screen with green, draws the line and score, and makes the frames per second 60
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    for i in range(cell_number):
        pygame.draw.line(screen, (50, 50, 50), (0, i * cell_size), (cell_number * cell_size, i * cell_size), 2)
        score_font = pygame.font.Font(None, 30)
        score_text = score_font.render("Score: " + str(main_game.score), True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        pygame.draw.line(screen, (50, 50, 50), (i * cell_size, 0), (i * cell_size, cell_number * cell_size), 2)
    pygame.display.update()
    clock.tick(60)
