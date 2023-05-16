
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# GONNA MAKE MOUSE VERSION FROM SCRATCH
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

import random
import time
import pygame
import math
import datetime
from pygame import mixer
# initialize the pygame
pygame.init()

# create the screen
screenSize = pygame.display.Info()
width = screenSize.current_w
height = screenSize.current_h
screen = pygame.display.set_mode((width, height))

# Background
wallpaper = pygame.display.set_mode((width, height))
try:
    picture = pygame.image.load('space.png')
except:
    raise FileNotFoundError("File: \"space.png\" could not be found!")
else:
    picture = pygame.transform.scale(picture, (width, height))
    rect = picture.get_rect()
    rect = rect.move((0, 0))


# Title and Icon
pygame.display.set_caption('Galaxy Guard')
try:
    icon = pygame.image.load('ufo.png')
except:
    raise FileNotFoundError("File: \"ufo.png\" could not be found!")
else:
    pygame.display.set_icon(icon)

# Player
try:
    playerImg = pygame.image.load('spaceship.png')
except:
    raise FileNotFoundError("File: \"spaceship.png\" could not be found!")
playerX = (width - 64) / 2
playerY = height - (height * 2 / 8)
playerUp = 0
playerDown = 0
playerLeft = 0
playerRight = 0

# Enemy
enemyX = []
enemyY = []
enemyNums = 6  # 6
eMoveX = []
try:
    enemyImg = pygame.image.load('monster.png')
except:
    raise FileNotFoundError("File: \"monster.png\" could not be found!")
for i in range(enemyNums):
    eMoveX.append(0)
    enemyX.append(random.randint(3, width - 65))
    enemyY.append(random.randint(-70, -60))
# Explosion
try:
    explosionImg = pygame.image.load('explosion.png')
except:
    raise FileNotFoundError("File: \"explosion.png\" could not be found!")

# Bullet
try:
    bulletImg = pygame.image.load('bullet.png')
except:
    raise FileNotFoundError("File: \"bullet.png\" could not be found!")
bulletX = -100
bulletY = -100
bulletX_change = 0
bulletY_change = (height*width/1000000) * 5
bulletState = 'ready'

# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
scoreX = width / 2 - 58
scoreY = 10

# Background sound
try:
    mixer.music.load('backMusic.mp3')
    mixer.music.play(-1)
except:
    raise FileNotFoundError("File: \"backMusic.mp3\" could not be found !")

# ready =  ready to shoot / bullet is not visible
# fire = bullet is still going
def enemy(x, y):
    screen.blit(enemyImg, (x, y))
    # for a in random.randint(4):
def player(x, y):
    screen.blit(playerImg, (x, y))
# Control
def firebullet(x, y):
    global bulletState
    bulletState = 'fire'
    screen.blit(bulletImg, (x + 16, y + 10))

def isCollision(enX, enY, bulX, BulY):
    distance = math.sqrt(((enX - bulX) ** 2) + ((enY - BulY) ** 2)) ############################ IMPORTANT
    if distance < 32: #32pixels
        return True
def enemy_player_collision(enX, enY, plX, plY):
    distance = math.sqrt(((enX - plX) ** 2) + ((enY - plY) ** 2))
    if distance < 60:
        return True
def show_score(x, y):
    score = font.render("Score : {}".format(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

clock = pygame.time.Clock()
fpsfont = pygame.font.SysFont("Arial", 18)

def update_fps():
    fps = str(int(clock.get_fps()))
    fps_text = fpsfont.render(fps, 1, pygame.Color("coral"))
    return fps_text

move = 0
# Gameloop
running = True
while running:
    screen.fill((104, 22, 156))  # RGB
    wallpaper.blit(picture, rect)
    screen.blit(update_fps(), (10, 10))
    # Button presses:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if bulletState == 'ready':
                try:
                    laser = mixer.Sound('laser.wav')
                except:
                    raise FileNotFoundError("File: \"laser.wav\" could not be found!")
                else:
                    laser.set_volume(0.1)
                    laser.play()
                bulletX = playerX
                bulletY = playerY
                firebullet(bulletX, bulletY)
            bulletState = 'fire'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if bulletState == 'ready':
                    try:
                        laser = mixer.Sound('laser.wav')
                    except:
                        raise FileNotFoundError("File: \"laser.wav\" could not be found!")
                    else:
                        laser.set_volume(0.1)
                        laser.play()
                    bulletX = playerX
                    bulletY = playerY
                    firebullet(bulletX, bulletY)
                bulletState = 'fire'
            if event.key == pygame.K_a:
                playerLeft = -(height*width/1000000 * 1.5)
            if event.key == pygame.K_d:
                playerRight = height*width/1000000 * 1.5
            if event.key == pygame.K_w:
                playerUp = -(height*width/1000000 * 1.5)
            if event.key == pygame.K_s:
                playerDown = height*width/1000000 * 1.5
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                playerLeft = 0
            if event.key == pygame.K_d:
                playerRight = 0
            if event.key == pygame.K_s:
                playerDown = 0
            if event.key == pygame.K_w:
                playerUp = 0
    # Player borader
    if playerX + playerLeft + playerRight < (width - 65) and playerX + playerLeft + playerRight > 1:
        playerX += playerLeft + playerRight
    if playerY + playerUp + playerDown < (height - 65) and playerY + playerUp + playerDown > 2:
        playerY += playerDown + playerUp

    # Bullet Movement
    if bulletY <= 0:
        bulletState = 'ready'
        bulletY = playerY
    if bulletState == 'fire':
        firebullet(bulletX, bulletY)
        bulletY -= bulletY_change

    # Enemy movement
    for i in range(enemyNums):
        if move % 400 == 0:
            eMoveX[i] = random.randint(-(int(height*width/150000)), int(height*width/200000)) / 10
        move += 1
        enemyX[i] += eMoveX[i]
        enemyY[i] += random.randint(0, int(height*width/100000)) / 20

        # Enemy boarder
        if enemyX[i] <= 0:
            enemyX[i] = 1
        if enemyX[i] >= (width - 65):
            enemyX[i] = width - 65
        if enemyY[i] >= (height + 2):
            enemyY[i] = random.randint(-70, -60)
            enemyX[i] = random.randint(3, width - 65)

        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            bulletY = -100
            bulletState = 'ready'
            score_value += 1
            print('score: {}'.format(score_value))
            eMoveX[i] = 0
            try:
                point = mixer.Sound('point.wav')
            except:
                raise FileNotFoundError("File: \"point.wav\" could not be found!")
            else:
                point.set_volume(0.2)
                point.play()
            enemyX[i] = random.randint(3, width - 65)
            enemyY[i] = random.randint(-70, -60)

        if enemy_player_collision(enemyX[i], enemyY[i], playerX, playerY):
            bulletY = -100
            bulletState = 'ready'
            score_value -= 1
            print('score: {}'.format(score_value))
            try:
                expl = mixer.Sound('Explosion.wav')
            except:
                raise FileNotFoundError("File: \"Explosion.wav\" could not be found!")
            else:
                expl.set_volume(0.3)
                expl.play()
            screen.blit(explosionImg, (playerX-30, playerY-20))
            pygame.display.update()
            time.sleep(0.2)
            playerX = (width - 64) / 2
            playerY = height - (height * 2 / 8)
            pygame.display.update()
            enemyX[i] = random.randint(3, width - 65)
            enemyY[i] = random.randint(2, int(height - height * 99 / 100))# Player, Enemy and gun interactions
        player(playerX, playerY)
        enemy(enemyX[i], enemyY[i])
    show_score(scoreX, scoreY)
    clock.tick(300)
    pygame.display.update()

fileName = 'Score.txt'
with open(fileName, 'a') as f:
    f.write('Your Score %s/%s/%s  %s:%s   :   %s \n' % (datetime.datetime.now().year, datetime.datetime.now().month,
                                                           datetime.datetime.now().day, datetime.datetime.now().hour,
                                                           datetime.datetime.now().minute, score_value))
