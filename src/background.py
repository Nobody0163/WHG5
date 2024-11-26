import pygame

import colors

__bg_surf: pygame.Surface | None = None

def render_background(window: pygame.Surface):
    global __bg_surf
    if __bg_surf is None:
        __bg_surf = pygame.Surface((window.get_width(), window.get_height()))
        TILE_SIZE = 32

        dark_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))
        light_tile = pygame.Surface((TILE_SIZE, TILE_SIZE))

        dark_tile.fill((128, 128, 128))
        light_tile.fill(colors.WHITE)

        for i in range(__bg_surf.get_width() // TILE_SIZE):
            for j in range(__bg_surf.get_height() // TILE_SIZE):
                if (i + j) % 2 == 0:
                    __bg_surf.blit(dark_tile, (i * TILE_SIZE, j * TILE_SIZE))
                else:
                    __bg_surf.blit(light_tile, (i * TILE_SIZE, j * TILE_SIZE))
    window.blit(__bg_surf, (0, 0))