import pygame

import constants
import player as _player
import wall as _wall

class MovingWall:
    x: float
    y: float
    movement_pattern: list[str]
    movement_counter: int
    border_pattern: int

    def __init__(self, x: float, y: float, movement_pattern: list[str|int], speed: float, border_pattern: int):
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

        self.border_pattern = border_pattern
    
    def update(self, player:_player.Player):
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

        player_rect = pygame.Rect(player.x, player.y, constants.PLAYER_SPRITE.get_width(), constants.PLAYER_SPRITE.get_height())
        wall_rect = pygame.Rect(self.x, self.y, constants.WALL_SPRITE.get_width(), constants.WALL_SPRITE.get_height())

        if wall_rect.colliderect(player_rect):
            top_dst = player_rect.bottom - wall_rect.top
            bottom_dst = wall_rect.bottom - player_rect.top
            right_dst = wall_rect.right - player_rect.left
            left_dst = player_rect.right - wall_rect.left

            if top_dst <= bottom_dst and top_dst <= right_dst and top_dst <= left_dst:
                player.y -= top_dst
            if bottom_dst <= top_dst and bottom_dst <= right_dst and bottom_dst <= left_dst:
                player.y += bottom_dst
            if right_dst <= top_dst and right_dst <= left_dst and right_dst <= bottom_dst:
                player.x += right_dst
            if left_dst <= top_dst and left_dst <= right_dst and left_dst <= bottom_dst:
                player.x -= left_dst

    def render(self, window: pygame.Surface):
        window.blit(constants.WALL_SPRITE, (self.x, self.y))

        if self.border_pattern & _wall.BORDER_LEFT:
            window.blit(_wall.VERT_BORDER_SURF, (self.x, self.y))
        if self.border_pattern & _wall.BORDER_TOP:
            window.blit(_wall.HOR_BORDER_SURF, (self.x, self.y))
        if self.border_pattern & _wall.BORDER_RIGHT:
            window.blit(_wall.VERT_BORDER_SURF, (self.x + (constants.WALL_SPRITE.get_width() - _wall.VERT_BORDER_SURF.get_width()), self.y))
        if self.border_pattern & _wall.BORDER_BOTTOM:
            window.blit(_wall.HOR_BORDER_SURF, (self.x, self.y + (constants.WALL_SPRITE.get_height() - _wall.HOR_BORDER_SURF.get_height())))