import player
import checkpoint
import enemy
import wall
import coin
import moving_wall

import json
import pygame

def load_level(path: str):
    with open(path, "r") as f:
        level_data = json.loads(f.read())

    _player = player.Player(level_data["spawn"]["x"], level_data["spawn"]["y"])
    checkpoints = [checkpoint.Checkpoint(pygame.Rect(cp["x"], cp["y"], cp["w"], cp["h"]), cp["start"], cp["finish"]) for cp in level_data["checkpoints"]]
    enemies = [enemy.Enemy(en["x"], en["y"], en["mp"], en["spd"]) for en in level_data["enemies"]]
    walls = [wall.Wall(_wall["x"], _wall["y"], _wall["bp"]) for _wall in level_data["walls"]]
    coins = [coin.Coin(_coin["x"], _coin["y"]) for _coin in level_data["coins"]]
    movable_walls = [moving_wall.MovingWall(mwall["x"], mwall["y"], mwall["mp"], mwall["spd"], mwall["bp"]) for mwall in level_data["mwalls"]]

    return (_player, checkpoints, enemies, walls, coins, movable_walls)