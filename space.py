import pygame
import random
import math

# Init
pygame.init()

# Bildschirmgröße
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")

# Spieler
playerImg = pygame.Surface((50, 40))
playerImg.fill((0, 255, 0))
playerX = 375
playerY = 520
playerX_change = 0
player_speed = 5

# Gegner
enemyImg = pygame.Surface((40, 30))
enemyImg.fill((255, 0, 0))
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 3  # weniger Gegner

for i in range(num_of_enemies):
    enemyX.append(random.randint(0, 760))
    enemyY.append(random.randint(30, 100))  # weiter oben starten
    enemyX_change.append(1.5)  # langsamere Geschwindigkeit
    enemyY_change.append(20)

# Laser
laserImg = pygame.Surface((5, 20))
laserImg.fill((255, 255, 0))
laserX = 0
laserY = 520
laserY_change = 7  
laser_state = "ready"


score = 0
font = pygame.font.Font(None, 36)

def show_score(x, y):
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg, (x, y))

def fire_laser(x, y):
    global laser_state
    laser_state = "fire"
    screen.blit(laserImg, (x + 22, y))

def is_collision(enemyX, enemyY, laserX, laserY):
    distance = math.sqrt((enemyX - laserX) ** 2 + (enemyY - laserY) ** 2)
    return distance < 27


running = True
while running:
    screen.fill((0, 0, 50))  # Hintergrund dunkelblau

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Tastensteuerung
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -player_speed
            if event.key == pygame.K_RIGHT:
                playerX_change = player_speed
            if event.key == pygame.K_SPACE:
                if laser_state == "ready":
                    laserX = playerX
                    fire_laser(laserX, laserY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # Spieler Bewegung
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 750:
        playerX = 750

    # Gegner Bewegung
    for i in range(num_of_enemies):
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 1.5
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 760:
            enemyX_change[i] = -1.5
            enemyY[i] += enemyY_change[i]

        # Game over, wenn Gegner zu nah kommen
        if enemyY[i] > 480:
            for j in range(num_of_enemies):
                enemyY[j] = 1000  # Gegner verschwinden
            game_over_font = pygame.font.Font(None, 64)
            game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
            screen.blit(game_over_text, (300, 250))
            running = False

        # Kollision Laser - Gegner
        if is_collision(enemyX[i], enemyY[i], laserX, laserY):
            laserY = 520
            laser_state = "ready"
            score += 1
            enemyX[i] = random.randint(0, 760)
            enemyY[i] = random.randint(30, 100)

        enemy(enemyX[i], enemyY[i], i)

    # Laser Bewegung
    if laser_state == "fire":
        fire_laser(laserX, laserY)
        laserY -= laserY_change
    if laserY <= 0:
        laserY = 520
        laser_state = "ready"

    player(playerX, playerY)
    show_score(10, 10)

    pygame.display.update()
