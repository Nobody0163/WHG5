import pygame

import constants
import player as _player
import coin

class Enemy:
    x: float
    y: float
    movement_pattern: list[str]
    movement_counter: int
    speed: float

    # Movement pattern format: [NUMBER, STR, NUMBER, STR ...]
    def __init__(self, x: float, y: float, movement_pattern: list[str|int], speed: float):
        self.x = x
        self.y = y

        self.movement_pattern = []

        i = 0
        while i < len(movement_pattern):
            for _ in range(movement_pattern[i]):
                self.movement_pattern.append(movement_pattern[i + 1])
            i += 2

        self.movement_counter = 0
        self.speed = speed
    
    def update(self, player: _player.Player, deaths: list[int], coins: list[coin.Coin]):
        direction = self.movement_pattern[self.movement_counter]
        self.movement_counter += 1

        self.movement_counter %= len(self.movement_pattern)

        if direction == "<":
            self.x -= self.speed
        elif direction == ">":
            self.x += self.speed
        elif direction == "^":
            self.y -= self.speed
        elif direction == "v":
            self.y += self.speed

        # Check if player is colliding with enemy.
        if pygame.Rect(player.x, player.y, constants.PLAYER_SPRITE.get_width(), constants.PLAYER_SPRITE.get_height()).colliderect(pygame.Rect(self.x, self.y, constants.ENEMY_SPRITE.get_width(), constants.ENEMY_SPRITE.get_height())):
            player.kill(coins)
            deaths[0] += 1

    def render(self, window: pygame.Surface):
        window.blit(constants.ENEMY_SPRITE, (self.x, self.y))