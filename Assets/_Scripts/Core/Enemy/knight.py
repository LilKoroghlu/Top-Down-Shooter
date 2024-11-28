import random

from pygame import Surface

from .enemy_animation import EnemyAnimation
import pygame
import os
from  Assets._Scripts.Runtime.UIProperties import  UIProperties
from Assets._Scripts.Core.Player.player import Player

class Knight():
    def __init__(self, player: Player):
        self.__player = player

        self.__enemyRunImage = [pygame.image.load(os.path.join('../Art/Enemy/Knight/Run', f'Run {i}.png')) for i in
                                range(1, 8)]
        self.__enemyAttackImage = [pygame.image.load(os.path.join('../Art/Enemy/Knight/Attack', f'Attack {i}.png')) for
                                   i in range(1, 22)]
        self.__enemyIdleImage = [pygame.image.load(os.path.join('../Art/Enemy/Knight/Idle', f'Idle {i}.png')) for i in
                                 range(1, 15)]

        self.__enemyRunImageFlipped = [pygame.transform.flip(img, True, False) for img in self.__enemyRunImage]
        self.__enemyAttackImageFlipped = [pygame.transform.flip(img, True, False) for img in self.__enemyAttackImage]
        self.__enemyIdleImageFlipped = [pygame.transform.flip(img, True, False) for img in self.__enemyIdleImage]

        self.__enemyAnimationIndex = 0
        self.__enemyAnimationTimer = 0
        self.__enemyAnimationSpeed = 0.1
        self.__enemyMovementSpeed = 5
        self.__attackRange = 50
        self.__enemySpeed = 1
        self.__enemyDamage = 20
        self.__enemyAttackSpeed = 1
        self.__enemyHealth = 100
        self.__enemyAttackTimer = 0

        self.__spawnX = random.randint(0, UIProperties.Get_Width())
        self.__spawnY = random.randint(0, UIProperties.Get_Height())
        self.__enemyTransform = pygame.Vector2(self.__spawnX, self.__spawnY)
        self.__enemyWidth, self.__enemyHeight = self.__enemyIdleImage[0].get_size()
        self.__enemyWidth *= 2
        self.__enemyHeight *= 2

        self.__enemyFlipX = False
        self.__enemyPlayingAttackAnimation = False
        self.__enemyAnimation = EnemyAnimation.Run
        self.__enemyView = pygame.transform.scale(self.__enemyRunImage[self.__enemyAnimationIndex],
                                                  (self.__enemyWidth, self.__enemyHeight))

        self.__isAlive = True

    @property
    def enemyWidth(self):
        return self.__enemyWidth

    @property
    def enemyHeight(self):
        return self.__enemyHeight

    @property
    def enemyHealth(self):
        return self.__enemyHealth

    @property
    def enemyTransform(self):
        return self.__enemyTransform

    @property
    def isAlive(self):
        return self.__isAlive

    @property
    def enemyView(self):
        return self.__enemyView

    def Tick(self, deltaTime):
        self.__enemyAnimationTimer += deltaTime

        playerTransform = self.__player.playerTransform
        direction = playerTransform - self.enemyTransform

        distance_to_player = direction.length()
        if distance_to_player > 0:
            direction = direction.normalize()

        self.__enemyFlipX = direction.x < 0

        if distance_to_player <= self.__attackRange:
            if not self.__enemyPlayingAttackAnimation:
                self.__enemyPlayingAttackAnimation = True
                self.__enemyAnimation = EnemyAnimation.Attack
                self.__enemyAnimationIndex = 0
            elif self.__enemyPlayingAttackAnimation:
                if self.__enemyAnimationIndex == len(self.__enemyAttackImage) - 1:
                    self.__enemyPlayingAttackAnimation = False
                    self.AttackPlayer()
                else:
                    if not(self.__enemyAnimation == EnemyAnimation.Attack):
                        self.__enemyAnimation = EnemyAnimation.Attack
        else:
            self.__enemyPlayingAttackAnimation = False
            self.__enemyAnimation = EnemyAnimation.Run
            self.__enemyTransform += direction * self.__enemyMovementSpeed

        self.UpdateView()

    def AttackPlayer(self):
        self.__player.takeDamage(self.__enemyDamage)

    def UpdateView(self):
        if self.__enemyAnimation == EnemyAnimation.Idle and self.__enemyAnimationTimer >= self.__enemyAnimationSpeed and not self.__enemyPlayingAttackAnimation:
            self.__enemyAnimationTimer = 0
            frame_list = self.__enemyIdleImageFlipped if self.__enemyFlipX else self.__enemyIdleImage
            self.__enemyView = pygame.transform.scale(frame_list[self.__enemyAnimationIndex],
                                                      (self.__enemyWidth, self.__enemyHeight))

        elif self.__enemyAnimation == EnemyAnimation.Run and self.__enemyAnimationTimer >= self.__enemyAnimationSpeed and not self.__enemyPlayingAttackAnimation:
            self.__enemyAnimationTimer = 0
            frame_list = self.__enemyRunImageFlipped if self.__enemyFlipX else self.__enemyRunImage
            self.__enemyView = pygame.transform.scale(frame_list[self.__enemyAnimationIndex],
                                                      (self.__enemyWidth, self.__enemyHeight))

        elif self.__enemyAnimation == EnemyAnimation.Attack and self.__enemyAnimationTimer >= self.__enemyAnimationSpeed:
            self.__enemyAnimationTimer = 0
            frame_list = self.__enemyAttackImageFlipped if self.__enemyFlipX else self.__enemyAttackImage
            self.__enemyView = pygame.transform.scale(frame_list[self.__enemyAnimationIndex],
                                                      (self.__enemyWidth, self.__enemyHeight))
            if self.__enemyAnimationIndex == len(self.__enemyAttackImage) - 1:
                self.__enemyPlayingAttackAnimation = False

        if self.__enemyAnimation == EnemyAnimation.Run:
            self.__enemyAnimationIndex += 1
            if self.__enemyAnimationIndex >= len(self.__enemyRunImage):
                self.__enemyAnimationIndex = 0

        elif self.__enemyAnimation == EnemyAnimation.Idle:
            self.__enemyAnimationIndex += 1
            if self.__enemyAnimationIndex >= len(self.__enemyIdleImage):
                self.__enemyAnimationIndex = 0

        elif self.__enemyAnimation == EnemyAnimation.Attack:
            self.__enemyAnimationIndex += 1
            if self.__enemyAnimationIndex >= len(self.__enemyAttackImage):
                self.__enemyAnimationIndex = 0

    def TakeDamage(self, damage):
        self.__enemyHealth -= damage
        if self.__enemyHealth <= 0:
            self.__isAlive = False