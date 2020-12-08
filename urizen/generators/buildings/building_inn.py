#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default


def building_inn(w=22, h=22, wall_material=None, floor_material=None, has_exterior=True):
    """
    Construct inn with living room for poor, living room for rich, kitchen/storage, big saloon and outdoor.

    Constraints:

        - Map width and map height must be >= 22
        - Map width and map height must be <= 27.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    """
    # Initial checks. Don't accept too small/big inn
    if w < 22 or h < 22:
        raise ValueError('Building is too small: w or h < 22')
    elif w > 27 or h > 27:
        raise ValueError('Building is too big: w or h > 27')
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

    # Calculate main room h. We have three situations: rich room h = 5, 6, 7.
    # If rich room h = 6 or 7, we expand main room h + 1 or + 2.
    main_room_h = 13 + (h - 1) % 3
    kitchen_w = 15
    M = room_default(w, h, wall_type=C.void, floor_type=C.void)
    main_room = room_default(w, main_room_h, wall_type=wall_material, floor_type=floor_material)
    M.meld(main_room, 0, 0)
    M[kitchen_w-2, main_room_h-1] = C.door_closed_window()
    for y in range(5, main_room_h-3):
        M[kitchen_w-1, y] = wall_material()
    kitchen = _room_kitchen(kitchen_w, 6, wall_material, floor_material)
    M.meld(kitchen, 0, 0)
    living_room = _room_living(9, h-5, wall_material, floor_material)
    M.meld(living_room, 0, 5)
    private_room = _room_private(w-kitchen_w+1, 4, wall_material, floor_material)
    M.meld(private_room, kitchen_w-1, 0)
    vending = _interior_vending(5, main_room_h-7, wall_material, floor_material,)
    M.meld(vending, 9, 6)
    bar = _interior_bar(w-kitchen_w-1, main_room_h-5, floor_material,)
    M.meld(bar, kitchen_w, 4)
    if has_exterior:
        outdoor = _room_outdoor(w-9, h - main_room_h)
        M.meld(outdoor, 9, main_room_h)

    return M


def building_roadhouse(w=15, h=15, wall_material=None, floor_material=None):
    """
    Construct roadhouse with living room for poor, kitchen/storage and saloon.

    Constraints:

        - Map width and map height must be >= 15.
        - Map width and map height must be <= 21.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    """
    # Initial checks. Don't accept too small/big inn
    if w < 15 or h < 15:
        raise ValueError('Building is too small: w or h < 15')
    elif w > 21 or h > 21:
        raise ValueError('Building is too big: w or h > 21')
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
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[13, h-1] = C.door_closed_window()
    kitchen = _room_kitchen(w, 6, wall_material, floor_material)
    M.meld(kitchen, 0, 0)
    living_room = _room_living(9, h-5, wall_material, floor_material)
    M.meld(living_room, 0, 5)
    vending = _interior_vending(w-10, h-7, wall_material, floor_material)
    M.meld(vending, 9, 6)

    return M


def _room_kitchen(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    storage = room_default(6, 6, wall_type=wall_material, floor_type=floor_material)
    M.meld(storage, 0, 0)
    M[5, h-3] = C.door_open_empty()
    M[10, h-1] = C.door_open_empty()
    M[7, 0] = C.door_closed_window()
    for x in range(1, 3):
        for y in range(1, 3):
            M[x, y] = C.flora_mushroom_button()
    storage_items = [
        T.furniture_barrel(),
        T.furniture_barrel(),
        T.furniture_barrel(),
        T.furniture_barrel(),
        T.furniture_box_filled(),
        T.furniture_box_filled(),
        T.bag(),
        T.food_leaf()
    ]
    storage_w = 6
    M.scatter(1, 1, 5, h-1, storage_items, exclude=[
        (storage_w-2, h-3),
        (storage_w-3, h-3),
        (storage_w-4, h-3),
        (storage_w-3, h-4),
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2)
    ])
    for x in range(8, 11):
        M[x, 1].put(T.furniture_hearth())
    for x in range(8, 11):
        M[x, 3].put(T.furniture_table())
    M[13, 1] = C.stairs_down()
    M[11, 1].put(T.bucket())
    for y in range(1, 3):
        M[6, y].put(T.food_meat())
    M[6, 4].put(T.food_egg())
    M[11, 3].put(T.furniture_box_filled())
    M.scatter(6, 1, 14, 5, [A.animal_cat()])
    if w > 15:
        num_of_items = (w - 15) * 2
        food_items = [
            T.furniture_barrel(),
            T.furniture_barrel(),
            T.furniture_barrel(),
            T.furniture_box_filled(),
            T.furniture_box_filled(),
            T.bag()
        ]
        M.scatter(15, 1, w-1, h-1, random.sample(food_items, min(len(food_items), num_of_items)))
    return M


def _room_living(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    if h < 17:
        num_rooms = (h - 3) // 3
        for i in range(num_rooms):
            room_y = i * 3
            poor_room = _room_poor(4, 4, wall_material, floor_material, direction='right')
            M.meld(poor_room, 0, room_y)
            poor_room = _room_poor(4, 4, wall_material, floor_material, direction='left')
            M.meld(poor_room, 5, room_y)
        M[w-1, h-2] = C.door_open_empty()
        M[1, h-2].put(A.animal_spider())
        corridor_h = h - num_rooms * 3 - 1
        if corridor_h > 2:
            M[1, h-corridor_h].put(T.washtub())
            M[2, h-corridor_h].put(T.washtub())
            M[w-2, h-corridor_h].put(T.furniture_stool())
        M.scatter(1, h-corridor_h, w-2, h-1, [(A.animal_cat())])
    elif h >= 17:
        rich_room_h = 5 + (h - 2) % 3
        rich_1 = _room_rich(5, rich_room_h, wall_material, floor_material)
        M.meld(rich_1, 0, 0)
        rich_2 = _room_rich(5, rich_room_h, wall_material, floor_material)
        M.meld(rich_2, 4, 0)
        M[w-1, rich_room_h+1] = C.door_open_empty()
        M[1, rich_room_h+1].put(A.animal_spider())
        M.scatter(1, rich_room_h, w-1, rich_room_h+2, [(A.animal_cat())])
        num_rooms = (h - rich_room_h - 3) // 3
        for i in range(num_rooms):
            room_y = i * 3
            poor_room = _room_poor(4, 4, wall_material, floor_material, direction='right')
            M.meld(poor_room, 0, rich_room_h+2+room_y)
            poor_room = _room_poor(4, 4, wall_material, floor_material, direction='left')
            M.meld(poor_room, 5, rich_room_h+2+room_y)
    return M


def _room_rich(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[random.randint(1, w-2), 1].put(T.furniture_bed_double())
    items = [
        T.furniture_chest_profile(),
        T.furniture_bookcase(),
        T.light_lantern_oil(),
        T.furniture_cabinet(),
        T.furniture_closet()
    ]
    M.scatter(1, 1, w-1, h-1, items, exclude=[(2, h-2), (2, h-3), (2, h-4), (1, h-3), (3, h-3)])
    M[2, h-1] = C.door_closed()
    return M


def _room_poor(w, h, wall_material, floor_material, direction='right'):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[w-1, 1] = C.door_closed()
    room_items = {
        'default_room': [T.furniture_bed_single(), T.furniture_chest_profile(), T.furniture_torch()],
        'default_room_2': [T.furniture_bed_single(), T.furniture_cabinet(), T.furniture_torch()],
        'poor_room': [T.furniture_napsack(), T.light_candle(), T.web()],
        'poor_room_2': [T.furniture_napsack(), T.furniture_chair()]
    }
    M.scatter(1, 1, w-1, h-1, random.choice(list(room_items.values())), exclude=[(w-2, 1)])
    if direction == 'left':
        M.hmirror()
    return M


def _room_private(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for x in (1, 4):
        M[x, 1].put(T.furniture_chair())
    for x in (2, 3):
        M[x, 1].put(T.furniture_longtable())
    M[5, 1].put(T.light_lantern_oil())
    M[w-2, h-1] = C.door_closed()
    return M


def _interior_vending(w, h, wall_material, floor_material):
    M = Map(w, h, fill_cell=floor_material)
    for x in range(w):
        M[x, 2].put(T.furniture_longtable_showcase())
    M[0, 1].put(T.money_pile())
    M[w//2, 1].put(T.dining_mug())
    for x in range(1, w, 2):
        M[x, 3].put(T.furniture_stool())
    M[1, h-1].put(T.furniture_barrel())
    M[2, h-1].put(T.furniture_barrel())
    if w > 7:
        M[w-2, h-1].put(T.furniture_table())
        M[w-1, h-1].put(T.furniture_stool())
        M[w-3, h-1].put(T.furniture_stool())
    if h > 6:
        for x in range(1, w-2, 3):
            for y in range(5, h-2, 3):
                M[x, y].put(T.furniture_table())
                M[x+1, y].put(T.furniture_stool())
    return M


def _interior_bar(w, h, floor_material):
    M = Map(w, h, fill_cell=floor_material)
    M[0, 0].put(T.furniture_table())
    M[1, 0].put(T.furniture_stool())
    for x in range(w//3, w):
        for y in (h//3, h//3*2+1):
            M[x, y].put(T.furniture_longtable())
    M.scatter(w//3, h//3-1, w, h//3+2, [T.furniture_stool() for _ in range(w-w//3)], exclude=[(w//3, h//3-1)])
    M.scatter(w//3, h//3*2, w, h//3*2+3, [T.furniture_stool() for _ in range(w-w//3)], exclude=[(w//3, h//3*2+2)])
    M[0, h-1].put(T.furniture_table())
    M[1, h-1].put(T.furniture_stool())
    M[w-1, h-1].put(T.light_lantern_oil())
    return M


def _room_outdoor(w, h):
    M = Map(w, h, fill_cell=C.floor_rocks)
    for i in range(w*h//3):
        grass_x = random.randint(0, w-1)
        grass_y = random.randint(0, h-1)
        M[grass_x, grass_y] = random.choice([C.flora_grass, C.flora_tree, C.floor_grass])()
    for x in (1, 8):
        M[x, 0].put(T.furniture_table())
    for x in (0, 2, 7, 9):
        M[x, 0].put(T.furniture_stool())
    if w > 13:
        M[11, 0].put(T.furniture_table())
        M[10, 0].put(T.furniture_stool())
        M[12, 0].put(T.furniture_stool())
    for y in range(0, h):
        M[4, y] = C.floor_cobblestone()

    num_stables = (h - 5) // 2
    stables = Map(3, 2, fill_cell=C.void)
    for x in range(3):
        stables[x, 0] = C.wall_fence_thin()
    stables[2, 1] = C.wall_fence_thin()
    stables[0, 1] = C.door_close_fence()
    stables[1, 1].put(A.animal_horse())
    last_stable_y = h - 1
    for i in range(num_stables):
        stable_x = w - 3
        stable_y = 4 + (i * 2)
        M.meld(stables, stable_x, stable_y)
        last_stable_y = stable_y
    for x in range(w-3, w):
        M[x, last_stable_y + 2] = C.wall_fence_thin()
    M[2, h-1].put(T.sign_pointer())
    M[3, 0].put(T.light_torch())
    for y in (h//2-1, h//2):
        M[0, y].put(T.washtub())
    if w > 9:
        M[0, h//2+1].put(T.washtub())
    M[5, 0] = C.flora_flower()

    return M
