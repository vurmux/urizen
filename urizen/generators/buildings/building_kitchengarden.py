#!/usr/bin/python3

import random
from copy import deepcopy
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default


def building_kitchengarden(w=17, h=17, wall_material=None, floor_material=None, direction='down'):
    """
    Construct kitchen garden with big storage, garden beds and cattle pens.

    Constraints:

        - Map width and map height must be >= 17
        - Map width and map height must be <= 22
        - Wall material must be 'block', 'plank' or 'stone'.
        - Floor material must be 'grit' or 'rocks'.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height

    wall_material : str
        Wall's material.

    floor_material : str
        Floor's material.

    direction : str
        Direction of the kitchen garden. Can be 'up', 'down', 'left' or 'right'.
    """
    # Initial checks. Don't accept too small/big kitchen garden
    if w < 17 or h < 17:
        raise ValueError('Building is too small: w or h < 17')
    elif w > 22 or h > 22:
        raise ValueError('Building is too big: w or h > 22')
    # Choose materials
    if not wall_material:
        wall_material = random.choice([C.wall_block, C.wall_plank, C.wall_stone])
    elif wall_material not in (['block', 'plank', 'stone']):
        raise ValueError('Wall material should be "block", "plank" or "stone"')
    if wall_material == 'block':
        wall_material = C.wall_block
    elif wall_material == 'plank':
        wall_material = C.wall_plank
    elif wall_material == 'stone':
        wall_material = C.wall_stone

    if not floor_material:
        floor_chance = random.random()
        if floor_chance > 0.3:
            floor_material = C.floor_rocks
        else:
            floor_material = C.floor_grit
    elif floor_material not in (['grit', 'rocks']):
        raise ValueError('Floor material should be "grit" or "rocks"')
    if floor_material == 'grit':
        floor_material = C.floor_grit
    elif floor_material == 'rocks':
        floor_material = C.floor_rocks

    M = Map(w, h, fill_cell=floor_material)
    storage_w = w // 3 * 2
    storage_h = h // 4 + 1
    garden_beds_w = w // 2

    for i in range(w*h//3):
        grass_x = random.randint(1, w-1)
        grass_y = random.randint(0, h-2)
        M[grass_x, grass_y] = random.choice([C.flora_grass, C.flora_tree, C.floor_grass])()
    garden_beds = _room_garden_beds(garden_beds_w, h-storage_h+1, wall_material, floor_material)
    M.meld(garden_beds, 0, storage_h-1)
    cattle_pens = _room_cattle_pens(w-garden_beds_w+1, h-storage_h+1, wall_material, floor_material)
    M.meld(cattle_pens, garden_beds_w-1, storage_h-1)
    storage = _room_storage(storage_w, storage_h, wall_material, floor_material, garden_beds_w)
    M.meld(storage, 0, 0)
    for x in range(storage_w, w-1):
        M[x, storage_h//2] = floor_material()
    for y in range(storage_h//2, storage_h-1):
        M[storage_w+1, y] = floor_material()

    if random.choice([True, False]):
        M.hmirror()
    if direction == 'up':
        M.vmirror()
    elif direction == 'left':
        M.transpose()
    elif direction == 'right':
        M.transpose()
        M.hmirror()

    return M


def _room_garden_beds(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=C.wall_fence, floor_type=floor_material)
    M[w-2, 1].put(T.well())
    M[w-2, h-2].put(T.tool_wheelbarrow())
    for y in range(h//2-2, h//2):
        M[w-2, y].put(T.farm_mangler())
    for y in range(h//2+1, h-5):
        M[w-2, y].put(T.furniture_box_filled())
    seed_plot_h = h // 3
    agricultures = [
        random.choice([C.farm_corn, C.farm_wheat]),
        random.choice([C.farm_vegetables_leafs, C.farm_vegetables_cabbage]),
        random.choice([C.farm_vegetables, C.farm_vegetables_cabbage])
    ]
    for x in range(1, w-3):
        for y in range(1, seed_plot_h):
            M[x, y] = agricultures[0]()
        for y in range(seed_plot_h+1, seed_plot_h*2):
            M[x, y] = agricultures[1]()
        for y in range(seed_plot_h*2+1, h-1):
            M[x, y] = agricultures[2]()
    M[w-4, seed_plot_h].put(T.washtub())

    return M


def _room_cattle_pens(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=C.wall_fence, floor_type=floor_material)
    M[w-7, 0] = C.door_close_fence()
    for i in range(w*h//3):
        grass_x = random.randint(1, w-2)
        grass_y = random.randint(1, h-2)
        M[grass_x, grass_y] = random.choice([C.flora_grass, C.flora_cane, C.floor_grass])()
    num_cattles = h // 4 + 1
    cowshed = Map(4, 3, fill_cell=floor_material)
    for y in (1, 2):
        cowshed[0, y] = C.wall_fence()
    for y in range(0, 3):
        cowshed[3, y].put(T.water_trough())
    for x in (1, 2):
        cowshed[x, 2] = wall_material()
    cowshed[1, 1].put(T.bucket())
    cowshed_y = 1
    for x in range(num_cattles):
        copied_cowshed = deepcopy(cowshed)
        M.meld(copied_cowshed, w-5, cowshed_y)
        cowshed_y += 3
    cows = [A.animal_cow() for _ in range(num_cattles)]
    M.scatter(1, 1, w-5, h-1, cows)

    return M


def _room_storage(w, h, wall_material, floor_material, garden_beds_w):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[w-1, h//2] = C.door_closed_window()
    M[w-2, h-1] = C.door_closed_window()
    M[garden_beds_w-3, h-1] = C.door_open()
    M[w-2, 1].put(T.light_torch())
    M[w-4, 1].put(T.dining_bottle())
    M[w-3, h-2].put(T.furniture_napsack())
    for x in range(1, w//2):
        for y in range(1, h-1):
            items = random.choice([T.farm_mangler, T.furniture_box_filled, T.furniture_barrel, T.food_milk])()
            M[x, y].put(items)

    return M
