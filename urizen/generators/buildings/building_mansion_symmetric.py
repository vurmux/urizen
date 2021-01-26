#!/usr/bin/python3

import random
from copy import deepcopy
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default


def building_mansion_symmetric(w=25, h=25, wall_material=None, floor_material=None, direction='down'):
    """
    Construct medieval mansion with living rooms, kitchen, library, treasury, servant's room and outdoor.

    Constraints:

        - Map width and map height must be >= 20
        - Map width and map height must be <= 25
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

    direction : str
        Direction of the house. Can be 'up', 'down', 'left' or 'right'.
    """
    # Initial checks. Don't accept too small/big house
    if w < 20 or h < 20:
        raise ValueError('Building is too small: w or h < 20')
    elif w > 25 or h > 25:
        raise ValueError('Building is too big: w or h > 25')
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

    M = room_default(w, h, wall_type=wall_material, floor_type=C.void)
    default_room_w = w // 4 + 1
    default_room_h = h // 4
    library_h = h // 2 - 1
    second_bedroom_h = h // 4 + 2

    treasury = _room_treasury(default_room_w, default_room_h, wall_material, floor_material)
    M.meld(treasury, 0, 0)
    bedroom = _room_bedroom(default_room_w, h-second_bedroom_h-default_room_h+2, wall_material, floor_material)
    M.meld(bedroom, 0, default_room_h-1)
    second_bedroom = _room_second_bedroom(default_room_w, second_bedroom_h, wall_material, floor_material)
    M.meld(second_bedroom, 0, h-second_bedroom_h)
    sacrifice = _room_of_sacrifice(default_room_w, default_room_h, wall_material, floor_material)
    M.meld(sacrifice, w-default_room_w, 0)
    kitchen = _room_kitchen(default_room_w, h-default_room_h*2+1, wall_material, floor_material)
    M.meld(kitchen, w-default_room_w, default_room_h-1)
    servant = _room_servant(default_room_w, default_room_h+1, wall_material, floor_material)
    M.meld(servant, w-default_room_w, h-default_room_h-1)
    library = _room_library(w-default_room_w*2+2, library_h, wall_material, floor_material)
    M.meld(library, default_room_w-1, 0)
    garden = _interior_garden(w-default_room_w*2, h-library_h-1, wall_material, floor_material)
    M.meld(garden, default_room_w, library_h)
    for x in range(w//2-1, w//2+1+w%2):
        M[x, h-1] = C.door_closed_wooden()
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


def _room_treasury(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    items = [
        T.money_pile(),
        T.money_pile(),
        T.necklace(),
        T.mineral_geode(),
        T.mineral_diamond(),
        T.magic_orb(),
        T.scroll_text(),
        T.ring(),
        T.bag(),
    ]
    M.scatter(1, 1, w-1, h-1, items, exclude=[(w-2, h-3)])

    return M


def _room_bedroom(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for x in range(1, w-2):
        M[x, 1].put(T.furniture_longtable())
    M[2, 2].put(T.furniture_chair())
    M[w-2, 1].put(T.furniture_bookcase())
    M[w-2, h-5].put(T.furniture_closet())
    M[1, h-5].put(T.furniture_chandelier())
    M[2, h-5].put(T.furniture_bed_double())
    M[w-2, h//3].put(T.urn())
    for x in range(1, w-2):
        M[x, h-4] = wall_material()
    M[w-2, h-4] = C.door_open_stairs()
    items = [
        T.light_lantern_oil(),
        T.magic_alchemisttable(),
        T.book_magic(),
        T.furniture_chair()
    ]
    M.scatter(1, h-3, w-1, h-1, items, exclude=[(2, h-3), (3, h-3), (4, h-3)])
    return M


def _room_second_bedroom(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    M[1, 1] = C.flora_flower()
    M[w-3, 1].put(T.furniture_table())
    M[w-2, 1].put(T.furniture_chair())
    M[1, h//2].put(T.furniture_closet())
    items = [
        T.furniture_cabinet(),
        T.furniture_bed_single(),
        T.furniture_chandelier()
    ]
    M.scatter(1, h-2, w-1, h-1, items)
    M[w-1, h-5] = C.door_closed()

    return M


def _room_of_sacrifice(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=C.floor_flagged)
    M[w-2, h//2].put(T.magic_portal())
    items = [
        T.effect_blood(),
        T.effect_blood(),
        T.book_magic(),
        T.weapon_dagger(),
        T.bones_remains()
    ]
    M.scatter(1, 1, w-2, h-1, items, exclude=[(1, 2), (w-2, h//2)])

    return M


def _room_kitchen(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for x in range(2, w-1):
        M[x, h-4].put(T.furniture_longtable())
    for x in range(3, w-1):
        M[x, h-2].put(T.furniture_box_filled())
    M[w-2, h-3].put(T.furniture_stool())
    for y in range(4, h-5):
        M[1, y].put(T.furniture_barrel())
    M[w-2, 5].put(T.furniture_hearth())
    M[1, h-2].put(T.bucket())
    M[w-2, 3] = C.stairs_down()
    M[1, 1].put(T.farm_mangler())
    items = [
        T.food_apple(),
        T.food_cheese(),
        T.food_chicken(),
        T.food_egg()
    ]
    M.scatter(w-2, 1, w-1, h-6, items, exclude=[(w-2, 3)])

    return M


def _room_servant(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for y in range(2, h-1, 2):
        M[1, y].put(T.furniture_bed_single())
    num_table = 1 if h < 8 else h - 3
    for y in (1, num_table):
        M[w-2, y].put(T.furniture_table_round())
        M[w-3, y].put(T.furniture_stool())
        M[w-2, y+1].put(T.furniture_stool())
    items = [
        T.light_torch(),
        T.furniture_cabinet(),
        T.furniture_chest_profile()
    ]
    M.scatter(1, h-3, w-1, h-1, items)
    M[2, 0] = C.door_closed_window()

    return M


def _room_library(w, h, wall_material, floor_material):
    M = room_default(w, h, wall_type=wall_material, floor_type=floor_material)
    for x in range(1, w//2-1):
        M[x, 1].put(T.furniture_bookcase())
    for x in range(w//2+1+w%2, w-1):
        M[x, 1].put(T.furniture_bookcase())
    for x in (1, w-2):
        M[x, 2].put(T.furniture_bookcase())
        M[x, h-2] = C.column_antique()
    for x in (0, w-1):
        M[x, 2] = C.door_open_stairs()
        M[x, h-3] = C.door_closed()
    for x in range(w//2-1, w//2+1+w%2):
        M[x, 1].put(T.furniture_hearth())
        M[x, 3].put(T.furniture_sofa())
        M[x, h-3].put(T.furniture_chair())
        M[x, h-1] = C.door_open_empty()
    items = [
        T.book(),
        T.book()
    ]
    M.scatter(2, 2, w-2, 3, items)
    for x in range(3, w-3):
        M[x, h-4].put(T.furniture_longtable())
    for x in (2, w-3):
        M[x, h-4].put(T.furniture_chair())
    for x in (3, w-4):
        M[x, h-5].put(T.furniture_chandelier())

    return M


def _interior_garden(w, h, wall_material, floor_material):
    M = Map(w, h, fill_cell=C.floor_flagged)
    garden_part = Map(w//2, h, fill_cell=C.flora_grass)
    for y in range(0, h):
        garden_part[w//2-1, y] = C.floor_flagged()
    for x in range(1, w//2-1):
        for y in range(1, 4):
            garden_part[x, y] = C.floor_flagged()
    for x in range(2, w//2):
            garden_part[x, 2].put(T.water_trough())
    for y in range(h-3, h):
        garden_part[0, y] = C.flora_tree()
        garden_part[1, y].put(T.water_trough())
        garden_part[2, y] = C.flora_flower()
    garden_part[w//2-2, 0] = C.flora_flower()
    garden_part[0, h-5].put(T.furniture_sofa())
    garden_part[1, h-5].put(T.furniture_table_round())
    garden_part[2, h-6].put(T.urn())
    M.meld(garden_part, 0, 0)
    garden_part2 = deepcopy(garden_part)
    garden_part2.hmirror()
    M.meld(garden_part2, w//2+w%2, 0)
    for x in range(0, w//2-1):
        M[x, h-4] = C.floor_flagged()
    M.scatter(0, 0, w-1, h-1, [A.animal_cat()])

    return M
