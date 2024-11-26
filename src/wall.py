import pygame

import constants
import player as _player

BORDER_LEFT = 1
BORDER_TOP = 2
BORDER_RIGHT = 4
BORDER_BOTTOM = 8

VERT_BORDER_SURF = pygame.Surface((2, constants.WALL_SPRITE.get_height()))
HOR_BORDER_SURF = pygame.Surface((constants.WALL_SPRITE.get_width(), 2))

class Wall:
    x: float
    y: float
    border_pattern: int

    def __init__(self, x: float, y: float, border_pattern: int):
        self.x = x
        self.y = y
        self.border_pattern = border_pattern
    
    def update(self, player:_player.Player):
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
        
        if self.border_pattern & BORDER_LEFT:
            window.blit(VERT_BORDER_SURF, (self.x, self.y))
        if self.border_pattern & BORDER_TOP:
            window.blit(HOR_BORDER_SURF, (self.x, self.y))
        if self.border_pattern & BORDER_RIGHT:
            window.blit(VERT_BORDER_SURF, (self.x + (constants.WALL_SPRITE.get_width() - 1), self.y))
        if self.border_pattern & BORDER_BOTTOM:
            window.blit(HOR_BORDER_SURF, (self.x, self.y + (constants.WALL_SPRITE.get_height() - 1)))