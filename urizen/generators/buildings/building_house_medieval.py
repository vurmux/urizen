#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default


def building_house_tworoom(w=12, h=9, wall_material=None, floor_material=None, has_exterior=True, direction='down'):
    """
    Construct house with living room, kitchen and outdoor.

    Constraints:

        - Map width and map height must be >= 9
        - Map width and map height must be <= 15
        - Wall material must be 'block', 'plank', 'brick' or 'stone'.
        - Floor material must be 'dirt', 'parquet' or 'cobblestone'.

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

    has_exterior : bool
        Flag that generates an exterior of the house.

    direction : str
        Direction of the house. Can be 'up', 'down', 'left' or 'right'.
    """
    # Initial checks. Don't accept too small/big house
    if w < 9 or h < 9:
        raise ValueError('Building is too small: w or h < 9')
    elif w > 12 or h > 12:
        raise ValueError('Building is too big: w or h > 15')
    # Choose materials
    if not wall_material:
        wall_material = random.choice([C.wall_block, C.wall_plank, C.wall_brick, C.wall_stone])
    elif wall_material not in (['block', 'plank', 'brick', 'stone']):
        raise ValueError('Wall material should be "block", "plank", "brick" or "stone"')
    if wall_material == 'block':
        wall_material = C.wall_block
    elif wall_material == 'plank':
        wall_material = C.wall_plank
    elif wall_material == 'brick':
        wall_material = C.wall_brick
    elif wall_material == 'stone':
        wall_material = C.wall_stone

    if not floor_material:
        floor_material = random.choice([C.floor_dirt, C.floor_parquet, C.floor_cobblestone])
    elif floor_material not in (['dirt', 'parquet', 'cobblestone']):
        raise ValueError('Floor material should be "dirt", "parquet" or "cobblestone"')
    if floor_material == 'dirt':
        floor_material = C.floor_dirt
    elif floor_material == 'parquet':
        floor_material = C.floor_parquet
    elif floor_material == 'cobblestone':
        floor_material = C.floor_cobblestone

    M = Map(w, h, fill_cell=C.void)
    main_room_h = h // 3 * 2
    living_room_w = w // 2 + 1
    living_room_h = h-main_room_h + 1
    main_room = _room_main(w, main_room_h, wall_material, floor_material)
    M.meld(main_room, 0, 0)
    living_room = _room_living(living_room_w, living_room_h, wall_material, floor_material)
    M.meld(living_room, w-living_room_w, main_room_h-1)
    if has_exterior:
        outdoor = _room_outdoor(w-living_room_w, living_room_h-1)
        M.meld(outdoor, 0, main_room_h)
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


def _room_main(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[1, h-2].put(T.furniture_closet())
    M[w-2, 1].put(random.choice([T.furniture_chimney(), T.furniture_hearth()]))
    M[w-2, 2].put(random.choice([T.food_meat(), T.food_egg()]))
    for x in (w-3, w-4):
        M[x, 1].put(T.furniture_longtable())
    M[w-5, 1].put(random.choice([T.bucket(), T.bag()]))
    M[w-2, h-2].put(T.furniture_chest_profile())
    lantern_w = random.randint(5, w-4)
    M[lantern_w, h-2].put(T.light_lantern())
    M[3, h-1] = C.door_closed()
    if w >= 11:
        table_h = 1 if h <= 7 else h // 2 - 1
        M[4, table_h].put(T.furniture_table())
        M[3, table_h].put(T.furniture_stool())
        M[5, table_h].put(T.furniture_stool())
        M[4, table_h+1].put(T.furniture_stool())
        if table_h > 1:
            pantry = _interior_pantry(3, h//3, wall_material, floor_material)
            M.meld(pantry, 1, 1)
    elif w < 11:
        pantry = _interior_pantry(3, h//3, wall_material, floor_material)
        M.meld(pantry, 1, 1)

    return M


def _interior_pantry(w, h, wall_material, floor_material):
    M = Map(w, h, fill_cell=floor_material)
    if random.random() < 0.5:
        for y in range(h):
            M[2, y] = wall_material()
        items = [
            T.tool_wateringcan(),
            T.tool_pitchfork(),
            T.tool_fishingrod()
        ]
        M.scatter(0, 0, w-1, h, items)
    else:
        M[0, 0] = C.stairs_down()
        M[0, 1].put(T.furniture_box_filled())

    return M


def _room_living(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[w-2, h-2].put(T.furniture_bed_double())
    M[1, h-2].put(T.furniture_bed_single())
    M[1, h-3].put(T.furniture_bed_single())
    num_of_items = (w - 2) * (h - 2) // 3
    items = [
        T.furniture_chest_profile(),
        T.furniture_torch(),
        T.furniture_cabinet(),
        T.furniture_basket()
    ]
    M.scatter(1, 1, w-1, h-1, random.sample(items, min(len(items), num_of_items)), exclude=[(w-3, 1), (w-4, 1)])
    M[w-3, 0] = C.door_open_empty()

    return M


def _room_outdoor(w, h):
    M = Map(w, h, fill_cell=C.floor_rocks)
    for i in range(w*h//3):
        grass_x = random.randint(1, w-1)
        grass_y = random.randint(0, h-2)
        M[grass_x, grass_y] = random.choice([C.flora_grass, C.flora_tree, C.floor_grass])()
    M[w-1, 0].put(T.washtub())
    for x in range(w):
        M[x, h-1] = C.wall_fence_thin()
    for y in range(h-1):
        M[0, y] = C.wall_fence_thin()
    for y in range(h-1):
        M[3, y] = C.floor_rocks()
    M[3, h-1] = C.door_close_fence()

    return M
