import pygame

import constants
import coin

class Player:
    x: float
    y: float

    starting_x: float
    starting_y: float

    moving_right: bool
    moving_left: bool
    moving_down: bool
    moving_up: bool

    cp_coin_state: list[coin.Coin]

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

        self.moving_right = self.moving_down = self.moving_left = self.moving_up = False

        self.starting_x = x
        self.starting_y = y

        self.cp_coin_state = None

    def kill(self, coins: list[coin.Coin]):
        # For some reason this happens after going back to cp
        if self.cp_coin_state:
            for i, _ in enumerate(coins):
                cpc = self.cp_coin_state[i]
                coins[i].collected = cpc.collected
                coins[i].do_render = cpc.do_render
        else:
            for c in coins:
                c.collected = False
                c.do_render = True

        self.x = self.starting_x
        self.y = self.starting_y

    def update(self, window: pygame.Surface, delta_time: int):
        window.blit(constants.PLAYER_SPRITE, (self.x, self.y))

        if self.moving_left:
            self.x -= delta_time * constants.PLAYER_SPEED

        if self.moving_right:
            self.x += delta_time * constants.PLAYER_SPEED

        if self.moving_up:
            self.y -= delta_time * constants.PLAYER_SPEED

        if self.moving_down:
            self.y += delta_time * constants.PLAYER_SPEED