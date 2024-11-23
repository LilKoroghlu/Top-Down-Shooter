import pygame

from Assets._Scripts.Core.Player.player import Player
from Assets._Scripts.Core.Player.player_controller import PlayerController
from Assets._Scripts.Runtime.UIProperties import UIProperties
from Assets._Scripts.Core.Enemy.knight import Knight
from Assets._Scripts.Core.Enemy.enemy import Enemy
import random

pygame.init()
screen = pygame.display.set_mode((UIProperties.Get_Width(), UIProperties.Get_Height()))
clock = pygame.time.Clock()
running = True

player = Player()
player_controller = PlayerController(player)

floorView = pygame.image.load('../Art/Environment/Floor.png')
floorView = pygame.transform.scale(floorView, (20, 20))
floor_surface = pygame.Surface((UIProperties.Get_Width(),  UIProperties.Get_Height()))


for i in range(0, 64):
    for j in range(0, 36):
        floor_surface.blit(floorView, (i * 20, j * 20))

spawnEnemyCount = 0
spawnedEnemiesCount = 0
spawnEnemyCooldown = 5
timer = 0
spawnedEnemies = []
nextWave = True

cursorView = pygame.image.load('../Art/UI/Cursor.png')
pygame.mouse.set_visible(False)

while running:
    deltaTime = clock.tick(60) / 1000
    timer += deltaTime
    if player.playerHealth <= 0:
        running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.blit(floor_surface, (0, 0))

    if nextWave:
        if timer >= spawnEnemyCooldown:
            spawnEnemyCount += 1
            spawnEnemy = random.randint(1, len(Enemy))
            if Enemy(spawnEnemy) == Enemy.Knight:
                spawnedEnemies.append(Knight(player))
            if len(spawnedEnemies) == spawnEnemyCount:
                nextWave = False
            timer = 0

    if not(nextWave):
        if len(spawnedEnemies) == 0:
            nextWave = True

    player_controller.Tick(deltaTime)
    for bullet in player_controller.get_bullets():
        bullet.Tick()
        bulletWidth, bulletHeight = bullet.bulletView.get_size()
        bulletPos = pygame.Vector2(bullet.bulletTransform.x - bulletWidth / 2, bullet.bulletTransform.y - bulletHeight / 2)
        screen.blit(bullet.bulletView, bullet.bulletTransform)
        for enemy in spawnedEnemies:
            if (bulletPos.x >= enemy.enemyTransform.x - 10 and bulletPos.x <= enemy.enemyTransform.x + 10) and (bulletPos.y >= enemy.enemyTransform.y -10 and bulletPos.y <= enemy.enemyTransform.y + 10):
                enemy.TakeDamage(50)
                if enemy.enemyHealth <= 0:
                    spawnedEnemies.remove(enemy)
    player.Tick(deltaTime)

    for enemy in spawnedEnemies:
        enemy.Tick(deltaTime)
        screen.blit(enemy.enemyView, (enemy.enemyTransform.x - enemy.enemyWidth / 2, enemy.enemyTransform.y - enemy.enemyHeight / 2))


    playerWidth, playerHeight = player.playerView.get_size()
    screen.blit(player.playerView, (player.playerTransform.x - playerWidth / 2, player.playerTransform.y - playerHeight / 2))

    cursorWidth, cursorHeight = cursorView.get_size()
    mousePos = pygame.math.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
    screen.blit(cursorView, (mousePos.x - cursorWidth / 2, mousePos.y - cursorHeight / 2))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
