#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default

def building_ruined_house(w=6, h=6, material=None):
    """
    Construct ruined house.
    It contain chimney, barrel and some animal.

    Constraints:

        - Map width and map height must be >= 6 and <= 10.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    """

    # Initial checks. Don't accept too small/big house.
    if w < 6 or h < 6:
        raise ValueError('Building is too small: w or h < 6')
    elif w > 10 or h > 10:
        raise ValueError('Building is too big: w or h > 10')

    # Choose materials
    wall_material = None
    if not material:
        wall_material = random.choice([C.wall_block, C.wall_plank, C.wall_stone, C.wall_brick])
    elif material not in (['block', 'plank', 'stone', 'brick']):
        raise ValueError('Material should be "block", "plank", "stone" or "brick"')

    if material == 'stone':
        wall_material = C.wall_stone
    elif material == 'block':
        wall_material = C.wall_block
    elif material == 'plank':
        wall_material = C.wall_plank
    elif material == 'brick':
        wall_material = C.wall_brick

    M = room_default(w, h, wall_type=wall_material, floor_type=C.floor_rocks)

    # Calculate % of replaced walls and added grass. 10% for walls and 20% for grass.
    grass_count = int((w - 2) * (h - 2) * 0.2)
    wall_ruined = int(w * h * 0.1)
    M[w//2, h-1] = C.door_open_dark()

    # Place some furniture and animals.
    all_coord = [(w//2, h-1), (w//2, h-2)]
    for item_class in (
            T.furniture_chimney, 
            A.animal_bat,
            A.animal_spider,
            T.web,
            T.furniture_barrel
            ):
        while True:
            x = random.randint(1, w-2)
            y = random.randint(1, h-2)
            if (x, y) not in all_coord:
                M[x, y].put(item_class())
                all_coord.append((x, y))
                break

    # Place some grass.
    for _ in range(grass_count):
        while True:
            x = random.randint(0, w-1)
            y = random.randint(0, h-1)
            if (x, y) not in all_coord:
                M[x, y] = C.flora_grass()
                all_coord.append((x, y))
                break

    # Replace some walls with rocks.
    for _ in range(wall_ruined):
        while True:
            x = random.randint(0, w-1)
            y = random.choice([0, h-1])
            if (x, y) not in all_coord:
                M[x, y] = C.floor_rocks()
                all_coord.append((x, y))
                break

    return M