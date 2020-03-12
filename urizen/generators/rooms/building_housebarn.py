#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_building_floor_stone,
    cell_building_floor_dirt,
    cell_building_wall_stone,
    cell_building_wall_wooden,
    cell_building_closed_door,
    cell_fence_wooden,
)
from urizen.core.thing_collection import (
    furniture_hearth,
    furniture_table,
    furniture_chair,
    furniture_bed,
    furniture_manger,
    other_bonfire,
)


HORIZONTAL = 'horizontal'
VERTICAL = 'vertical'
WOODEN = 'wooden'
STONE = 'stone'
LIVING_LEFT = 'living_left'
LIVING_RIGHT = 'living_right'


def building_housebarn(w=30, h=15, material=None):
    if w < 10 or h < 10:
        raise ValueError('Building is too small: w/h < 10')
    if not material:
        material = random.choice([WOODEN, STONE])
    if material not in (WOODEN, STONE):
        raise ValueError('Material should be "stone" or "wooden"')
    wall_cell_type = cell_building_wall_stone if material == STONE else cell_building_wall_wooden

    orientation = HORIZONTAL if w >= h else VERTICAL
    if orientation == HORIZONTAL:
        if w < h * 2 or w > h * 3:
            raise ValueError('Building is too wide or too short.')
    else:
        if h < w * 2 or h > w * 3:
            raise ValueError('Building is too wide or too short.')

    if orientation == VERTICAL:
        w, h = h, w
    M = Map(w, h, fill_cell=cell_building_floor_stone)
    
    for x in range(w):
        M[x, 0] = wall_cell_type(x, 0)
        M[x, h-1] = wall_cell_type(x, h-1)
    for y in range(h):
        M[0, y] = wall_cell_type(0, y)
        M[w-1, y] = wall_cell_type(w-1, y)
    
    living = random.choice([LIVING_LEFT, LIVING_RIGHT])
    living_wall_x = None
    barn_wall_x = None

    # Place central doors/corridor and calculate X-positions for vertical walls
    if w % 2 == 0:
        M[w//2, 0] = cell_building_floor_stone(w//2, 0)
        M[w//2-1, 0] = cell_building_floor_stone(w//2-1, 0)
        M[w//2, h-1] = cell_building_floor_stone(w//2, h-1)
        M[w//2-1, h-1] = cell_building_floor_stone(w//2-1, h-1)
        living_wall_x = (w // 2 - 3) if living == LIVING_LEFT else (w // 2 + 2)
        barn_wall_x = (w // 2 + 2) if living == LIVING_LEFT else (w // 2 - 3)
    else:
        M[w//2, 0] = cell_building_closed_door(w//2, 0)
        M[w//2, h-1] = cell_building_closed_door(w//2, h-1)
        living_wall_x = (w // 2 - 2) if living == LIVING_LEFT else (w // 2 + 2)
        barn_wall_x = (w // 2 + 2) if living == LIVING_LEFT else (w // 2 - 2)
    
    # Place vertical walls
    for i in range(1, h//3):
        M[living_wall_x, i] = wall_cell_type(living_wall_x, i)
        M[living_wall_x, h-i-1] = wall_cell_type(living_wall_x, h-i-1)
    for i in range(1, h-1):
        M[barn_wall_x, i] = cell_fence_wooden(barn_wall_x, i)
    M[barn_wall_x, h//2] = cell_building_closed_door(barn_wall_x, h//2)

    # Create living room
    lx_start = 1 if living == LIVING_LEFT else living_wall_x + 1
    lx_end = living_wall_x - 1 if living == LIVING_LEFT else w - 1
    beds_dx = int((lx_end - lx_start) % 2 == 0 and living == LIVING_RIGHT)
    beds_dy = random.choice([0, 1])
    
    for bed_x in range(lx_start + beds_dx, lx_end, 2):
        M[bed_x, 1+beds_dy].things.append(furniture_bed())
        M[bed_x, h-2-beds_dy].things.append(furniture_bed())

    is_bonfire = random.choice([True, False])
    if is_bonfire:
        M[(lx_start+lx_end)//2, h//2].things.append(other_bonfire())
    elif living == LIVING_LEFT:
        M[1, h//2].things.append(furniture_hearth())
    else:
        M[w-2, h//2].things.append(furniture_hearth())

    # Create barn
    bx_start = 1 if living == LIVING_RIGHT else barn_wall_x + 1
    bx_end = barn_wall_x - 1 if living == LIVING_RIGHT else w - 2
    
    for x in range(bx_start, bx_end + 1):
        for y in range(1, h-1):
            M[x, y] = cell_building_floor_dirt(x, y)

    #is_central_barn = True
    #if is_central_barn:
    #    for x in range(bx_start + 2, bx_end - 1, 2):
    #        M[x, h//2] = cell_fence_wooden(x, h//2)

    return M