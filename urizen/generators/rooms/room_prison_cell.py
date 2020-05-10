#!/usr/bin/python3

import random
from urizen.core.map import Map

from urizen.core.entity_collection import C, T, A


def room_prison_cell(w=5, h=5, direction='down'):
    if direction == 'left' or direction == 'right':
        w, h = h, w
    M = Map(w, h, fill_cell=C.floor_flagged)
    prison_cell_type = random.choice(['with_prisoner', 'with_bones', 'with_blood', 'with_spider'])
    
    # Create walls
    for x in range(0, w):
        M[x, 0] = C.wall_stone()
        M[x, h-1] = C.wall_stone()
    for y in range(0, h):
        M[0, y] = C.wall_stone()
        M[w-1, y] = C.wall_stone()
    
    # Create prison bars and door
    M[1, h-1] = C.wall_bars()
    M[3, h-1] = C.wall_bars()
    M[2, h-1] = C.door_closed_bars()

    # Place some things
    all_coord = []
    if prison_cell_type == 'with_prisoner':
        for item_class in (T.furniture_napsack, T.bucket, T.furniture_torch):
            while True:
                x = random.randint(1, 3)
                y = random.randint(1, h-2)
                if (x, y) not in all_coord:
                    M[x, y].put(item_class())
                    all_coord.append((x,y))
                    break
    elif prison_cell_type == 'with_bones':
        for item_class in (T.bones, T.bones_skull):
            while True:
                x = random.randint(1, 3)
                y = random.randint(1, h-2)
                if (x, y) not in all_coord:
                    M[x, y].put(item_class())
                    all_coord.append((x, y))
                    break
    elif prison_cell_type == 'with_blood':
        for item_class in (T.bones_remains, T.effect_blood):
            while True:
                x = random.randint(1, 3)
                y = random.randint(1, h-2)
                if (x, y) not in all_coord:
                    M[x, y].put(item_class())
                    all_coord.append((x, y))
                    break
    elif prison_cell_type == 'with_spider':
        for item_class in (T.web, T.web, A.animal_spider):
            while True:
                x = random.randint(1, 3)
                y = random.randint(1, h-2)
                if (x, y) not in all_coord:
                    M[x, y].put(item_class())
                    all_coord.append((x, y))
                    break
    
    if direction == 'up':
        M.vmirror()
    elif direction == 'left':
        M.transpose()
    elif direction == 'right':
        M.transpose()
        M.hmirror()

    return M