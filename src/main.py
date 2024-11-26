import pygame

import debug
import background
import threading
import constants
import gui
import colors
import checkpoint as _checkpoint
import load_level

pygame.init()

do_render_debug_menu = True

window = pygame.display.set_mode((1280, 736))
pygame.display.set_caption("Worlds Hardest Game 5")
pygame.display.set_icon(pygame.image.load("assets/sprites/icon.png"))
clock = pygame.time.Clock()
running = True
deaths = [0]
coins_collected = [0]

levels_path = "assets/levels/"
next_level_name = "01.json"

level = load_level.load_level("assets/levels/00.json")
player = level[0]
checkpoints = level[1]
enemies = level[2]
walls = level[3]
coins = level[4]
mwalls = level[5]

dbg_fdt = 0
dbg_ffps = 0

def fixed_update():
    fixed_update_clock = pygame.time.Clock()

    global player
    global checkpoints
    global enemies
    global walls
    global coins
    global coins_collected
    global next_level_name
    global running
    global mwalls
    global dbg_fdt
    global dbg_ffps

    try:
        while running:
            dbg_fdt = fixed_update_clock.tick(constants.FIXED_UPDATE_SPEED)
            dbg_ffps = fixed_update_clock.get_fps()

            for enemy in enemies:
                enemy.update(player, deaths, coins)

            for checkpoint in checkpoints:
                if checkpoint.update(player, coins) == _checkpoint.FinishStatus.FINISH:
                    try:
                        path = levels_path + next_level_name
                        n = int(next_level_name.split(".")[0]) + 1
                        next_level_name = ("0" + str(n) if n < 10 else str(n)) + ".json"
                        level = load_level.load_level(path)
                        coins_collected = [0]
                        player = level[0]
                        checkpoints = level[1]
                        enemies = level[2]
                        walls = level[3]
                        coins = level[4]
                        mwalls = level[5]
                    except FileNotFoundError: # Either the game is complete or the levels folder is fucked. We assume the former because I don't want to deal with the latter.
                        level = load_level.load_level("assets/levels/end.json")
                        player = level[0]
                        checkpoints = level[1]
                        enemies = level[2]
                        walls = level[3]
                        coins = level[4]
                        mwalls = level[5]

            for coin in coins:
                coin.update(player, coins_collected)

            for wall in walls:
                wall.update(player)

            for mwall in mwalls:
                mwall.update(player)

    except Exception as E:
        running = False
        raise E

fixed_update_thread = threading.Thread(target=fixed_update, daemon=True)
fixed_update_thread.start()

while running:
    delta_time = clock.tick()
    fps = clock.get_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                do_render_debug_menu = not do_render_debug_menu
            
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.moving_up = True

            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.moving_down = True

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.moving_left = True

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.moving_right = True
        
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                player.moving_up = False
                
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                player.moving_down = False

            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                player.moving_left = False

            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                player.moving_right = False
    
    background.render_background(window)

    if player.x < 0:
        player.x = 0
    
    if player.x > window.get_width() - constants.PLAYER_SPRITE.get_width():
        player.x = window.get_width() - constants.PLAYER_SPRITE.get_width()
    
    if player.y < 0:
        player.y = 0
    
    if player.y > window.get_height() - constants.PLAYER_SPRITE.get_height():
        player.y = window.get_height() - constants.PLAYER_SPRITE.get_height()

    for _enemy in enemies:
        _enemy.render(window)

    for checkpoint in checkpoints:
        checkpoint.render(window)

    for _coin in coins:
        _coin.render(window)

    for _wall in walls:
        _wall.render(window)

    for mwall in mwalls:
        mwall.render(window)

    player.update(window, delta_time)

    if do_render_debug_menu:
        debug.render_debug_menu(window, fps, delta_time, player, dbg_fdt, dbg_ffps)

    gui.render_text(window, f"Deaths: {deaths[0]}", (window.get_width() - 220, 0), "assets/fonts/Minecraft.ttf", 36, colors.BLACK)
    gui.render_text(window, f"Coins: {coins_collected[0]}/{len(coins)}", (window.get_width() - 200, 36), "assets/fonts/Minecraft.ttf", 24, colors.BLACK)

    pygame.display.flip()

pygame.quit()