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

def __convert_converted_mp_back_to_valid_json_format(converted_mp: list[str]):
    if not converted_mp:
        return []
    
    result = []
    current_element = converted_mp[0]
    count = 1

    for i in range(1, len(converted_mp)):
        if converted_mp[i] == current_element:
            count += 1
        else:
            result.extend([count, current_element])
            current_element = converted_mp[i]
            count = 1

    result.extend([count, current_element])

    return result


def save_level(path: str, _player: player.Player, checkpoints: list[checkpoint.Checkpoint], enemies: list[enemy.Enemy], walls: list[wall.Wall], coins: list[coin.Coin], movable_walls: list[moving_wall.MovingWall]):
    output_dict = {
        "spawn": {
            "x": _player.starting_x,
            "y": _player.starting_y
        },
        "checkpoints": [],
        "enemies": [],
        "walls": [],
        "coins": [],
        "mwalls": []
    }

    for cp in checkpoints:
        output_dict["checkpoints"].append({
            "x": cp.rect.x,
            "y": cp.rect.y,
            "w": cp.rect.w,
            "h": cp.rect.h,
            "start": cp.is_start,
            "finish": cp.is_finish
        })
    
    for _enemy in enemies:
        output_dict["enemies"].append({
            "x": _enemy.x,
            "y": _enemy.y,
            "mp": __convert_converted_mp_back_to_valid_json_format(_enemy.movement_pattern),
            "spd": _enemy.speed
        })
    
    for _wall in walls:
        output_dict["walls"].append({
            "x": _wall.x,
            "y": _wall.y,
            "bp": _wall.border_pattern
        })
    
    for _coin in coins:
        output_dict["coins"].append({
            "x": _coin.x,
            "y": _coin.y
        })
    
    for mwall in movable_walls:
        output_dict["mwalls"].append({
            "x": mwall.x,
            "y": mwall.y,
            "mp": __convert_converted_mp_back_to_valid_json_format(mwall.movement_pattern),
            "spd": mwall.speed,
            "bp": mwall.border_pattern
        })
    
    with open(path, "w") as f:
        f.write(json.dumps(output_dict))