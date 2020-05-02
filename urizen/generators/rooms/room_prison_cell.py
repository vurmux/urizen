#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_floor_flagged,
    cell_wall_stone,
    cell_door_closed_bars,
    cell_wall_fence_metal
)
from urizen.core.thing_collection import (
    item_furniture_torch,
    item_furniture_napsack,
    item_furniture_bucket,
    item_bones_human,
    item_spider_web,
    item_bones_skull,
    item_bones_remains,
    other_blood
)

def room_prison_cell(w=5, h=5, direction='down'):
    if direction == 'left' or direction == 'right':
        w, h = h, w
    M = Map(w, h, fill_cell=cell_floor_flagged)
    prison_cell_type = random.choice(['with_prisoner', 'with_bones', 'with_blood'])
    
    # Create walls
    for x in range(0, w):
        M[x, 0] = cell_wall_stone(x, 0)
        M[x, h-1] = cell_wall_stone(x, h-1)
    for y in range(0, h):
        M[0, y] = cell_wall_stone(x, 0)
        M[w-1, y] = cell_wall_stone(w-1, y)
    
    # Create prison bars and door
    M[1, h-1] = cell_wall_fence_metal(1, h-1)
    M[3, h-1] = cell_wall_fence_metal(3, h-1)
    M[2, h-1] = cell_door_closed_bars(2, h-1)

    # Place some things
    all_coord = []
    if prison_cell_type == 'with_prisoner':
        for item_class in (item_furniture_napsack, item_furniture_bucket, item_furniture_torch):
            while True:
                x = random.randint(1,3)
                y = random.randint(1,h-2)
                if (x, y) not in all_coord:
                    M[x, y].things.append(item_class())
                    all_coord.append((x,y))
                    break
    elif prison_cell_type == 'with_bones':
        for item_class in (item_bones_human, item_bones_skull):
            while True:
                x = random.randint(1,3)
                y = random.randint(1,h-2)
                if (x, y) not in all_coord:
                    M[x, y].things.append(item_class())
                    all_coord.append((x,y))
                    break
    elif prison_cell_type == 'with_blood':
        for item_class in (item_bones_remains, other_blood):
            while True:
                x = random.randint(1,3)
                y = random.randint(1,h-2)
                if (x, y) not in all_coord:
                    M[x, y].things.append(item_class())
                    all_coord.append((x,y))
                    break
    
    if direction == 'up':
        M.vmirror()
    elif direction == 'left':
        M.transpose()
    elif direction == 'right':
        M.transpose()
        M.hmirror()

    return M