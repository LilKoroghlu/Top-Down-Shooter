import pygame

from .player_bullet import PlayerBullet
from .player import Player
from .player_animation import PlayerAnimation


class PlayerController:
    def __init__(self, player: Player):
        self.bullets = []
        self.__player = player
        self.mouse_clicked = False
        self.__shootAnimationTime = 0.6
        self.__passedShootAnimationTime = 0
        self.__shootAnimationState = False

    def get_bullets(self):
        return self.bullets

    def Tick(self, deltaTime):
        self.__passedShootAnimationTime += deltaTime
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        move_vector = pygame.math.Vector2(0, 0)

        if self.__shootAnimationState:
            self.__passedShootAnimationTime += deltaTime
            if self.__passedShootAnimationTime >= self.__shootAnimationTime:
                self.__passedShootAnimationTime = 0
                self.__shootAnimationState = False

        if keys[pygame.K_w]:
            if not self.__shootAnimationState:
                self.__player.playerAnimation = PlayerAnimation.Run
            move_vector.y -= 1
        if keys[pygame.K_s]:
            if not self.__shootAnimationState:
                self.__player.playerAnimation = PlayerAnimation.Run
            move_vector.y += 1
        if keys[pygame.K_d]:
            if not self.__shootAnimationState:
                self.__player.playerAnimation = PlayerAnimation.Run
            self.__player.playerFlipX = False
            move_vector.x += 1
        if keys[pygame.K_a]:
            if not self.__shootAnimationState:
                self.__player.playerAnimation = PlayerAnimation.Run
            self.__player.playerFlipX = True
            move_vector.x -= 1
        if not any(keys) and not self.__shootAnimationState:
            self.__player.playerAnimation = PlayerAnimation.Idle

        if mouse[0] and not self.mouse_clicked and not self.__shootAnimationState:
            self.__shootAnimationState = True
            self.__player.playerAnimation = PlayerAnimation.Shoot
            mousePos = pygame.Vector2(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])
            bullet = PlayerBullet(self.__player.playerTransform.copy(), mousePos)
            self.bullets.append(bullet)
            self.mouse_clicked = True

        if not mouse[0]:
            self.mouse_clicked = False

        move_vector = self.normalize_vector(move_vector)
        movement = self.__player.playerTransform + move_vector * self.__player.playerMovementSpeed
        if (movement.x >= 0 and movement.x <= pygame.display.Info().current_w) and (
                movement.y >= 0 and movement.y <= pygame.display.Info().current_h):
            self.__player.playerTransform += move_vector * self.__player.playerMovementSpeed

    def normalize_vector(self, vector):
        length = vector.length()
        return vector / length if length > 0 else vector
