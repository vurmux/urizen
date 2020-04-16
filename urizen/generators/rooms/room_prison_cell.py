#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_building_floor_stone,
    cell_building_wall_stone,
    cell_building_closed_door,
    cell_building_prison_bars
)
from urizen.core.thing_collection import (
    item_candle,
    furniture_sleeping_bag,
    item_bucket,
    item_bones,
    item_spider_web,
    item_skull
)

def room_prison_cell(w=5, h=5, direction='down'):
    M = Map(w, h, fill_cell=cell_building_floor_stone)
    prison_cell_type = random.choice(['with_prisoner', 'with_bones', 'with_spyder_web'])
    
    # Create walls
    for x in range(0, w):
        M[x, 0] = cell_building_wall_stone(x, 0)
        M[x, h-1] = cell_building_wall_stone(x, h-1)
    for y in range(0, h):
        M[0, y] = cell_building_wall_stone(x, 0)
        M[w-1, y] = cell_building_wall_stone(w-1, y)
    
    # Create prison bars and door
    M[1,h-1] = cell_building_prison_bars(1, h-1)
    M[3, h-1] = cell_building_prison_bars(3, h-1)
    M[2, h-1] = cell_building_closed_door(2, h-1)

    # Place some things
    all_coord = []
    if prison_cell_type == 'with_prisoner':
        for item_class in (furniture_sleeping_bag, item_bucket, item_candle):
            while True:
                x = random.randint(1,3)
                y = random.randint(1,h-2)
                if (x, y) not in all_coord:
                    M[x, y].things.append(item_class())
                    all_coord.append((x,y))
                    break
    elif prison_cell_type == 'with_bones':
        for item_class in (item_bones, item_skull):
            while True:
                x = random.randint(1,3)
                y = random.randint(1,h-2)
                if (x, y) not in all_coord:
                    M[x, y].things.append(item_class())
                    all_coord.append((x,y))
                    break
    elif prison_cell_type == 'with_spyder_web':
        for item_class in (item_spider_web, item_skull):
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