#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_building_floor_stone,
    cell_building_wall_stone,
    cell_building_closed_door,
    cell_building_prison_bars,
    cell_void,
    cell_dungeon_stairs_up
)

from urizen.core.thing_collection import (
    item_candle,
    furniture_sleeping_bag,
    furniture_bed,
    furniture_chair,
    furniture_table,
    furniture_chest,
    furniture_torture_chair,
    item_bucket,
    item_bones,
    item_spider_web,
    item_skull,
    item_pliers
)
from urizen.generators.rooms.room_prison_cell import room_prison_cell

def building_prison_linear(w=21, h=12, orientation='horizontal'):
    """
    Construct a linear prison building interior.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    
    """

    # Initial checks. Don't accept:
    # - Too small prisons
    # - Too wide prisons (for both horizontal and vertical orientations)
    if w < 11 or h < 11:
        raise ValueError('Building is too small: w or h < 11')
    if h > 16 and orientation == 'horizontal':
        raise ValueError('Building is too big: h > 16 and orientation == "horizontal"')
    if w > 16 and orientation == 'vertical':
        raise ValueError('Building is too big: w > 16 and orientation == "vertical"')

    if orientation == 'vertical':
        w, h = h, w
    M = Map(w, h, fill_cell=cell_void)

    # Randomly choose where torture room and jailer room are.
    torture_left, jailer_right = None, None
    torture_left = random.choice([True, False])
    if torture_left:
        jailer_right = True
    else:
        jailer_right = False

    # Create jailer room. We have two situations: jailer room left/right.
    jailer_y_start = h // 4
    jailer_y_end = h // 3 * 2
    if jailer_right:
        # Create walls, floor and door
        for y in range(jailer_y_start, jailer_y_end+1):
            M[w-1, y] = cell_building_wall_stone(w-1, y)
            M[w-5, y] = cell_building_wall_stone(w-5, y)
        for x in range(w-5, w):
            M[x, jailer_y_start] = cell_building_wall_stone(x, jailer_y_start)
            M[x, jailer_y_end] = cell_building_wall_stone(x, jailer_y_end)
        for y in range(jailer_y_start+1, jailer_y_end):
            for x in range(w-4, w-1):
                M[x, y] = cell_building_floor_stone(x, y)   
        M[w-5, h//2] = cell_building_closed_door(w-5, h//2)

        # Place some furniture
        M[w-4, jailer_y_start+1].things.append(furniture_table())
        M[w-3, jailer_y_start+1].things.append(furniture_table())
        M[w-2, jailer_y_start+1].things.append(furniture_chair())
        M[w-4, jailer_y_end-1].things.append(item_candle())
        M[w-3, jailer_y_end-1].things.append(furniture_bed())
        M[w-2, jailer_y_end-1].things.append(furniture_chest())
    else:
        # Create walls, floor and door
        for y in range(jailer_y_start, jailer_y_end+1):
            M[0, y] = cell_building_wall_stone(0, y)
            M[4, y] = cell_building_wall_stone(4, y)
        for x in range(0, 5):
            M[x, jailer_y_start] = cell_building_wall_stone(x, jailer_y_start)
            M[x, jailer_y_end] = cell_building_wall_stone(x, jailer_y_end)
        for y in range(jailer_y_start+1, jailer_y_end):
            for x in range(1, 4):
                M[x, y] = cell_building_floor_stone(x, y)
        M[4, h//2] = cell_building_closed_door(4, h//2)

        # Place some furniture
        M[1, jailer_y_start+1].things.append(furniture_table())
        M[2, jailer_y_start+1].things.append(furniture_table())
        M[3, jailer_y_start+1].things.append(furniture_chair())
        M[1, jailer_y_end-1].things.append(furniture_chest())
        M[2, jailer_y_end-1].things.append(furniture_bed())
        M[3, jailer_y_end-1].things.append(item_candle())

    # Create torture room. We have two situations: torture room left/right. torture_start and torture_end - x-coord.
    # If torture_end = 0 or 1, there is no place for room (only one or two walls)
    # So we expand torture room for a one cell's width (+4)
    if jailer_right:
        torture_start = 0
        torture_end = (w-1)%4
        if torture_end == 0:
            torture_end = 4
        if torture_end == 1:
            torture_end = 5

        # Create walls, floor and door
        for x in range(torture_start, torture_end+1):
            M[x, 0] = cell_building_wall_stone(x, 0)
            M[x, h-1] = cell_building_wall_stone(x, h-1)
        for y in range(0, h-1):
            M[torture_start, y] = cell_building_wall_stone(y, torture_start)
            M[torture_end, y] = cell_building_wall_stone(y, torture_end)
        for x in range(torture_start+1, torture_end):
            for y in range(1, h-1):
                M[x, y] = cell_building_floor_stone(x, y)
        M[torture_end, h//2] = cell_building_closed_door(torture_end, h//2)

        # Place some furniture. If torture_end == 2 (just a corridor), then we set only stairs.
        M[torture_end-1, h-2] = cell_dungeon_stairs_up(torture_end-1, h-2)
        if torture_end != 2:
            M[(torture_end-torture_start)//2, h//2].things.append(furniture_torture_chair())
            all_coord = [(torture_end-1, h-2), ((torture_end-torture_start)//2, h//2)]
            for item_class in (item_bones, item_skull, item_pliers):
                while True:
                    x = random.randint(1,torture_end-1)
                    y = random.randint(1,h-2)
                    if (x, y) not in all_coord:
                        M[x, y].things.append(item_class())
                        all_coord.append((x,y))
                        break
    else:
        # If torture room is right, we are using the torture room width for calculations.
        # If torture_width = 7, then we reduce torture room for a one cell's width (-4).
        torture_width = w%4 + 4
        if torture_width == 7:
            torture_width = 3
        torture_end = w-1

        # Create walls, floor and door
        for x in range(w-torture_width, torture_end):
            M[x, 0] = cell_building_wall_stone(x, 0)
            M[x, h-1] = cell_building_wall_stone(x, h-1)
        for y in range(0, h):
            M[w-torture_width, y] = cell_building_wall_stone(w-torture_width, y)
            M[torture_end, y] = cell_building_wall_stone(torture_end, y)
        for x in range(w-torture_width+1, torture_end):
            for y in range(1, h-1):
                M[x, y] = cell_building_floor_stone(x, y)
        M[w-torture_width, h//2] = cell_building_closed_door(w-torture_width, h//2)

        # Place some furniture. If torture_width = 3 (just a corridor), then we set only stairs.
        M[w-2, h-2] = cell_dungeon_stairs_up(w-2, h-2)
        if torture_width != 3:
            M[w-2, h//2].things.append(furniture_torture_chair())
            all_coord = [(w-1, h-2), (w-2, h//2)]
            for item_class in (item_bones, item_skull, item_pliers):
                while True:
                    x = random.randint(w-torture_width+1, w-2)
                    y = random.randint(1,h-2)
                    if (x, y) not in all_coord:
                        M[x, y].things.append(item_class())
                        all_coord.append((x,y))
                        break
    
    # Fill corridor with a floor
    if jailer_right:
        cor_start = torture_end + 1
        cor_end = w - 6
    else:
        cor_start = 5
        cor_end = w - torture_width - 1
    if h % 2 == 1:
        for x in range(cor_start, cor_end+1):
            M[x, h//2] = cell_building_floor_stone(x, h//2)
    else:
        for x in range(cor_start, cor_end+1):
            M[x, h//2-1] = cell_building_floor_stone(x, h//2-1)
            M[x, h//2] = cell_building_floor_stone(x, h//2)
    
    # Place prison cells
    number_of_cells = (cor_end - cor_start + 2) // 4
    for cell_index in range(number_of_cells):
        cell_x = (cor_start-1) + (cell_index * 4)

        # Place upper cell
        M_cell = room_prison_cell(w=5, h=(h-1)//2)
        M.meld(M_cell, cell_x, 0)

        # Place lower cell
        M_cell = room_prison_cell(w=5, h=(h-1)//2, direction='up')
        M.meld(M_cell, cell_x, h//2+1)
    
    if orientation == 'vertical':
        M.transpose()

    return M