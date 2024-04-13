import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Set up screen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = pygame.display.get_surface().get_size()
cell_size = 20
grid_width = screen_width // cell_size
grid_height = screen_height // cell_size
pygame.display.set_caption("Snake Game")

# Load background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (screen_width, screen_height))

# Load death image
death_image = pygame.image.load("death.png")
death_image = pygame.transform.scale(death_image, (screen_width, screen_height))

# Load sound effects
pygame.mixer.init()
collision_sound = pygame.mixer.Sound('you_are_dead.mp3')
level_up_sound = pygame.mixer.Sound('lvlup.mp3')
apple_eat_sound = pygame.mixer.Sound('bottle_of_water.mp3')

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Font
font = pygame.font.Font(None, 36)

# Snake class
class Snake:
    def __init__(self):
        self.body = [(grid_width // 2, grid_height // 2)]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])
        self.add_block()

    def move(self):
        head = self.body[0]
        x, y = head
        if self.direction == "UP":
            self.body.insert(0, (x, y - 1))
        elif self.direction == "DOWN":
            self.body.insert(0, (x, y + 1))
        elif self.direction == "LEFT":
            self.body.insert(0, (x - 1, y))
        elif self.direction == "RIGHT":
            self.body.insert(0, (x + 1, y))

        if len(self.body) > self.length:
            self.body.pop()

    def add_block(self):
        self.length = len(self.body) + 1

    def change_direction(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def draw(self):
        for segment in self.body:
            x, y = segment
            pygame.draw.rect(screen, white, (x * cell_size, y * cell_size, cell_size, cell_size))
            pygame.draw.rect(screen, black, (x * cell_size + 1, y * cell_size + 1, cell_size - 2, cell_size - 2))

    def check_collision(self):
        head = self.body[0]
        x, y = head
        if x < 0 or x >= grid_width or y < 0 or y >= grid_height:
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        x = random.randint(1, grid_width - 2)  # Avoid borders
        y = random.randint(1, grid_height - 2)  # Avoid borders
        return x, y

    def draw(self):
        x, y = self.position
        pygame.draw.rect(screen, green, (x * cell_size, y * cell_size, cell_size, cell_size))


# Main function
def main():
    clock = pygame.time.Clock()

    level = 1
    lives = 3
    snake = Snake()
    food = Food()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction("RIGHT")

        snake.move()

        if snake.check_collision():
            collision_sound.play()
            pygame.time.delay(2000)
            lives -= 1
            if lives == 0:
                # Display death image and run death.bat script
                screen.blit(death_image, (0, 0))
                pygame.display.flip()
                pygame.time.delay(2000)  # Adjust delay as needed
                pygame.quit()
                os.system("death.bat")
                sys.exit()
            else:
                snake = Snake()
                food = Food()

        if snake.body[0] == food.position:
            snake.add_block()
            food = Food()
            apple_eat_sound.play()  # Play apple eat sound
            if len(snake.body) % 5 == 0:
                level += 1
                level_up_sound.play()  # Play level up sound
                print("Level:", level)

        screen.blit(background, (0, 0))

        # Render lives and level
        lives_text = font.render("Lives: " + str(lives), True, blue)  # Render lives text in blue
        level_text = font.render("Level: " + str(level), True, blue)  # Render level text in blue
        screen.blit(lives_text, (10, 10))
        screen.blit(level_text, (10, 50))

        snake.draw()
        food.draw()
        pygame.display.flip()

        clock.tick(10)

if __name__ == "__main__":
    main()
