import pygame
from enum import Enum

import constants
import player as _player
import colors
import coin
import copy

class FinishStatus(Enum):
    NOT_FINISH = 0
    FINISH = 1

class Checkpoint:
    rect: pygame.Rect
    is_start: bool
    is_finish: bool

    def __init__(self, rect: pygame.Rect, is_start: bool, is_finish: bool):
        self.rect = rect
        self.is_start = is_start
        self.is_finish = is_finish
    
    def update(self, player: _player.Player, coins: list[coin.Coin]):
        if self.rect.colliderect(pygame.Rect(player.x, player.y, constants.PLAYER_SPRITE.get_width(), constants.PLAYER_SPRITE.get_height())):
            player.starting_x = self.rect.centerx - constants.PLAYER_SPRITE.get_width() / 2
            player.starting_y = self.rect.centery - constants.PLAYER_SPRITE.get_height() / 2

            player.cp_coin_state = copy.deepcopy(coins)
        
            if self.is_finish:
                do_finish = True
                for coin in coins:
                    if not coin.collected:
                        do_finish = False
                        break
                    
                if do_finish:
                    return FinishStatus.FINISH

        return FinishStatus.NOT_FINISH
        
    def render(self, window: pygame.Surface):
        surf = pygame.Surface((self.rect.w, self.rect.h))
        surf.fill(colors.CHECKPOINT)
        surf.set_alpha(200)
        window.blit(surf, (self.rect.x, self.rect.y))