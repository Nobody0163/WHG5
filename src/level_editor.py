import pygame
import math

import debug
import background
import threading
import constants
import gui
import colors
import checkpoint as _checkpoint
import load_level
import player
import enemy
import wall
import coin
import moving_wall

# Convert x,y coordinate to list index
def ts_to_idx(tile_selected: tuple[int, int]):
    return tile_selected[1] * 40 + tile_selected[0]

window = pygame.display.set_mode((1280, 736))
running = True

output_path = ""
_player = player.Player(4, 4)
checkpoints: dict = {}
enemies = [None for _ in range(920)]
walls = [None for _ in range(920)]
coins = [None for _ in range(920)]
mwalls = []

tile_selected = (0, 0)
tile_selected_sprite = pygame.image.load("assets/sprites/tile_selected.png")

cp_start = None
cp_end = None

enemy_place_start = None

def fixed_update():
    while running:
        for _enemy in enemies:
            if _enemy is not None:
                _enemy.update(player.Player(-100, -100), [1], [])

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                _player = player.Player(tile_selected[0] * 32 + 4, tile_selected[1] * 32 + 4)
            
            elif event.key == pygame.K_w:
                if walls[ts_to_idx(tile_selected)] is None:
                    walls[ts_to_idx(tile_selected)] = wall.Wall(tile_selected[0] * 32, tile_selected[1] * 32, 0)
                else:
                    walls[ts_to_idx(tile_selected)] = None
            
            elif event.key == pygame.K_g:
                if coins[ts_to_idx(tile_selected)] is None:
                    coins[ts_to_idx(tile_selected)] = coin.Coin(tile_selected[0] * 32 + 8, tile_selected[1] * 32 + 8)
                else:
                    coins[ts_to_idx(tile_selected)] = None
            
            elif event.key == pygame.K_c:
                if cp_start is None:
                    cp_start = (tile_selected[0] * 32, tile_selected[1] * 32)
                else:
                    cp_end = (tile_selected[0] * 32, tile_selected[1] * 32)

                    if cp_start == cp_end:
                        try:
                            del checkpoints[cp_start]
                        except:
                            r = pygame.Rect(cp_start[0], cp_start[1], cp_end[0] - cp_start[0] + 32, cp_end[1] - cp_start[1] + 32)
                            checkpoints[cp_start] = _checkpoint.Checkpoint(r, r.colliderect(pygame.Rect(_player.x, _player.y, constants.PLAYER_SPRITE.get_width(), constants.PLAYER_SPRITE.get_height())), False)
                    
                    else:
                        r = pygame.Rect(cp_start[0], cp_start[1], cp_end[0] - cp_start[0] + 32, cp_end[1] - cp_start[1] + 32)
                        checkpoints[cp_start] = _checkpoint.Checkpoint(r, r.colliderect(pygame.Rect(_player.x, _player.y, constants.PLAYER_SPRITE.get_width(), constants.PLAYER_SPRITE.get_height())), False)
                    
                    cp_start = None
            
            elif event.key == pygame.K_s:
                _walls = []
                for _wall in walls:
                    if _wall is not None:
                        _walls.append(_wall)
                
                _coins = []
                for _coin in coins:
                    if _coin is not None:
                        _coins.append(_coin)

                load_level.save_level(input("Path to save to: "), _player, [checkpoints[cp] for cp in checkpoints], enemies, _walls, _coins, mwalls)
            
            elif event.key == pygame.K_e:
                if enemies[ts_to_idx(tile_selected)] is None:
                    enemies[ts_to_idx(tile_selected)] = enemy.Enemy(tile_selected[0] * 32 + 8, tile_selected[1] * 32 + 8, [1, ">", 1, "<"], 1)
                else:
                    enemies[ts_to_idx(tile_selected)] = None

    mpos = pygame.mouse.get_pos()
    tile_selected = (math.floor(mpos[0] / 32), math.floor(mpos[1] / 32))

    background.render_background(window)

    for _wall in walls:
        if _wall is not None:
            _wall.render(window)
    
    for cp in checkpoints:
        checkpoints[cp].render(window)

    _player.update(window, 0)

    for _coin in coins:
        if _coin is not None:
            _coin.render(window)
    
    for _enemy in enemies:
        if _enemy is not None:
            _enemy.render(window)

    window.blit(tile_selected_sprite, (tile_selected[0] * 32, tile_selected[1] * 32))

    pygame.display.flip()