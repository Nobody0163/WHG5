import pygame

import gui
import player as _player
import colors

def render_debug_menu(window: pygame.Surface, fps: float, delta_time: int, player: _player.Player, fdt: float, ffps: float):
    gui.render_text(window, f"Debug menu (F3 to toggle)", (0, 0), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)
    gui.render_text(window, f"FPS: {round(fps)}", (0, 20), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)
    gui.render_text(window, f"DT: {delta_time}", (0, 40), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)
    gui.render_text(window, f"X: {round(player.x, 1)} Y: {round(player.y, 1)}", (0, 60), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)
    gui.render_text(window, "font cache:", (0, 80), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)
    i = 0
    for cached_font_key in gui.__font_cache.keys():
        gui.render_text(window, f"  {" " if i < 10 else ""}{i}:" + str(cached_font_key), (0, 100 + i), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)
        i += 20
    gui.render_text(window, f"fdt: {fdt}", (0, 100 + i), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)
    gui.render_text(window, f"ffps: {round(ffps)}", (0, 120 + i), "assets/fonts/Minecraft.ttf", 20, colors.BLACK)