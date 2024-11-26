import player as _player
import pygame
import constants

class Coin:
    x: float
    y: float

    collected: bool
    do_render: bool

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.collected = False
        self.do_render = True
    
    def update(self, player, coins_collected: list[int]):
        if pygame.Rect(player.x, player.y, constants.PLAYER_SPRITE.get_width(), constants.PLAYER_SPRITE.get_height()).colliderect(pygame.Rect(self.x, self.y, constants.COIN_SPRITE.get_width(), constants.COIN_SPRITE.get_height())):
            if not self.collected:
                coins_collected[0] += 1
                self.collected = True
                self.do_render = False
    
    def render(self, window: pygame.Surface):
        if self.do_render:
            window.blit(constants.COIN_SPRITE, (self.x, self.y))
    
    def __repr__(self) -> str:
        return f"X: {self.x} Y: {self.y} collected: {self.collected} do_render: {self.do_render}"