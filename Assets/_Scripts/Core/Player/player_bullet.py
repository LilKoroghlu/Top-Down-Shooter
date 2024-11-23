import math
import pygame


class PlayerBullet:
    def __init__(self, transform: pygame.Vector2, destination: pygame.Vector2):
        self.bulletView = pygame.image.load('../Art/Bullet/Bullet.png')
        self.spawnBullet(transform, destination)
        self.bulletTransform = transform

    def spawnBullet(self, transform: pygame.Vector2, destination: pygame.Vector2):
        direction = (destination - transform).normalize()
        self.angle = math.degrees(math.atan2(-direction.y, direction.x))

        self.bulletView = pygame.transform.rotate(self.bulletView, self.angle)

    def Tick(self):
        speed = 5
        direction = pygame.math.Vector2(math.cos(math.radians(self.angle)), -math.sin(math.radians(self.angle)))
        self.bulletTransform += direction * speed
