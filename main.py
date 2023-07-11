"""
This is a game with space invader theme
"""

import pygame
import random
import math

# initialize pygame
pygame.init()

# Create game screen
screen = pygame.display.set_mode((800, 600))  # El paréntesis adentro del otro es una tupla

# Set icon, tittle and background
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load("ovni.png")
pygame.display.set_icon(icon)
background = pygame.image.load("galaxia.jpg")

# Player variables
img_player = pygame.image.load("astronave.png")
player_x = 368
player_y = 536
player_x_change = 0
player_y_change = 0

# Enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
number_of_enemies = 5

for i in range(number_of_enemies):
    img_enemy.append(pygame.image.load("enemu.png"))
    enemy_x.append(random.randint(0, 768))
    enemy_y.append(random.randint(30, 200))
    enemy_x_change.append(0.3)
    enemy_y_change.append(30)

# Bullet variables
img_bullet = pygame.image.load("bala.png")
bullet_x = 0
bullet_y = 536
bullet_x_change = 0
bullet_y_change = 0.5
bullet_visible = False

# Score variables
score = 0
score_font = pygame.font.Font("freesansbold.ttf", 32)
score_text_x = 10
score_text_y = 10

#End game
end_font =  pygame.font.Font("freesansbold.ttf", 64)

#End message
def final_message():
    final_text = end_font.render(f"Game Over: ", True, (255, 255, 255))
    screen.blit(final_text, (200,200))

#Show score
def show_score(x, y):
    text = score_font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(text,(x,y))



# Show player in screen
def player(x, y):
    screen.blit(img_player, (x, y))


# Show enemy in screen
def enemy(x, y, enemy_index):
    screen.blit(img_enemy[enemy_index], (x, y))
    # que aparezca el enemigo de la posición tal


# Show bullet
def shoot_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    # screen.blit(img_enemy, (x, y))
    screen.blit(img_bullet, (x + 16, y + 10))


# Detect collision
def detect_collision(x_1, y_1, x_2, y_2):
    x_sub = x_2 - x_1
    y_sub = y_2 - y_1
    distance = math.sqrt(math.pow(x_sub, 2) + math.pow(y_sub, 2))
    if distance < 27:
        return True
    else:
        return False


# Game infinite loop
is_running = True
while is_running:
    # RGB
    screen.fill((200, 200, 200))
    # screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # Es cuando le das a la X
            is_running = False
        if event.type == pygame.KEYDOWN:  # Si el tipo de evento fue presionar una tecla...
            if event.key == pygame.K_LEFT:
                player_x_change -= 0.5
            if event.key == pygame.K_RIGHT:
                player_x_change += 0.5
                """
            if event.key == pygame.K_DOWN:
                player_y_change += 0.5
            if event.key == pygame.K_UP:
                player_y_change -= 0.5
                """
            if event.key == pygame.K_SPACE:
                # shoot_bullet(player_x, player_y)
                if not bullet_visible:
                    bullet_x = player_x
                    shoot_bullet(player_x, bullet_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:  # or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player_x_change = 0
                player_y_change = 0

    # Update player location
    pygame.display.update()

    # Keep player inside the screen
    if player_x <= 0:
        player_x = 0
    if player_x >= 768:
        player_x = 768
    if player_y <= 0:
        player_y = 0
    if player_y >= 568:
        player_y = 568

    for i in range(number_of_enemies):
        #End of game
        if enemy_y[i] > 450:
            for j in range (number_of_enemies):
                enemy_y[j] = 1000
            final_message()
            break
        # Update enemy location
        enemy_x[i] += enemy_x_change[i]

        # Keep enemy inside the screen
        if enemy_x[i] <= 0:
            enemy_x_change[i] += 0.3
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 768:
            enemy_x_change[i] -= 0.3
            enemy_y[i] += enemy_y_change[i]

        # detect collision
        collision = detect_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
            enemy_x[i] = random.randint(0, 768)
            enemy_y[i] = random.randint(50, 200)
            bullet_visible = False
            bullet_y = 500
            score += 1
            print(score)

        # Show enemy
        enemy(enemy_x[i], enemy_y[i], i)

    # Shoot bullet
    if bullet_y <= -64:
        bullet_y = 500
        bullet_visible = False
    if bullet_visible:  # == True
        shoot_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # Show player
    player_x += player_x_change
    player_y += player_y_change
    player(player_x, player_y)

    #Show score
    show_score(score_text_x,score_text_y)

    # Update screen
    pygame.display.update()