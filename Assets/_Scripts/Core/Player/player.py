import pygame
import os


from .player_animation import  PlayerAnimation

class Player:

    def __init__(self):
        self.__playerIdleImage = pygame.image.load('../Art/Player/Idle/Idle.png')
        self.__playerRunImages = [pygame.image.load(os.path.join('../Art/Player/Run', f'Run {i}.png')) for i in range(1, 5)]
        self.__playerShootImages = [pygame.image.load(os.path.join('../Art/Player/Shoot', f'Shoot {i}.png')) for i in range(1, 5)]

        self.__playerView = self.__playerIdleImage

        self.__playerMovementSpeed = 5
        self.__playerMaxHealth = 100
        self.__playerHealth = self.__playerMaxHealth

        self.__playerFlipX = False
        self.__playerTransform = pygame.math.Vector2(0, 0)

        self.playerAnimationIndex = 0
        self.__playerAnimation = PlayerAnimation.Idle
        self.__animationSpeed = 0.1
        self.__animationTimer = 0

        self.__shootAnimationPlaying = False

    @property
    def playerMovementSpeed(self):
        return self.__playerMovementSpeed

    @property
    def playerHealth(self):
        return self.__playerHealth

    def takeDamage(self, damage: int):
        self.__playerHealth -= damage

    @property
    def playerFlipX(self):
        return self.__playerFlipX

    @playerFlipX.setter
    def playerFlipX(self, flip):
        self.__playerFlipX = flip
        self.update_player_view()

    @property
    def playerView(self):
        return pygame.transform.flip(self.__playerView, self.__playerFlipX, False)

    @property
    def playerTransform(self):
        return self.__playerTransform

    @playerTransform.setter
    def playerTransform(self, transform):
        if isinstance(transform, pygame.math.Vector2):
            self.__playerTransform = transform
        else:
            raise ValueError("playerTransform must be a Vector2")

    @property
    def playerAnimation(self):
        return self.__playerAnimation

    @playerAnimation.setter
    def playerAnimation(self, animation):
        if isinstance(animation, PlayerAnimation):
            self.__playerAnimation = animation
            self.update_player_view()

    def Tick(self, delta_time):
        self.__animationTimer += delta_time

    def update_player_view(self):
        if self.__playerAnimation == PlayerAnimation.Idle and self.__animationTimer >= self.__animationSpeed:
            self.__animationTimer = 0
            self.__playerView = self.__playerIdleImage
        elif self.__playerAnimation == PlayerAnimation.Run and self.__animationTimer >= self.__animationSpeed:
            self.__animationTimer = 0
            self.playerAnimationIndex = (self.playerAnimationIndex + 1) % len(self.__playerRunImages)
            self.__playerView = self.__playerRunImages[self.playerAnimationIndex]
        elif self.__playerAnimation == PlayerAnimation.Shoot and self.__animationTimer >= self.__animationSpeed:
            self.__animationTimer = 0
            self.playerAnimationIndex = (self.playerAnimationIndex + 1) % len(self.__playerShootImages)
            self.__playerView = self.__playerShootImages[self.playerAnimationIndex]