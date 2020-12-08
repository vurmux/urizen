#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A
from urizen.generators.rooms.room_default import room_default


def building_stables(w=16, h=16):
    """
    Construct stables with storage and two rows of horse boxes.

    Constraints:

        - Map width and map height must be >= 16 and <=23.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    """
    
    # Initial checks. Don't accept too small/big stables
    if w < 16 or h < 16:
        raise ValueError('Building is too small: w or h < 16')
    elif w > 23 or h > 23:
        raise ValueError('Building is too big: w or h > 25')

    M = Map(w, h, fill_cell=C.floor_rocks)
    for x in range(w):
        for y in range(h):
            if random.random() > 0.75:
                M[x, y] = C.flora_grass()

    # Calculate w and h for storage, horse boxes and stables.
    horse_box_size_w = w // 2 - 4
    horse_box_size_h = 2
    stables_size_w = horse_box_size_w * 2 + 3
    stables_shift_h = (h - 1) % 3
    stables_size_h = h - stables_shift_h
    storage_size_w = w - stables_size_w + 1
    storage_size_h = h * 2 // 3
    storage_start_w = w - storage_size_w

    # Meld stables, storage, add dog.
    main_stables = _room_horse_stables(stables_size_w, stables_size_h, horse_box_size_w, horse_box_size_h)
    M.meld(main_stables, 0, 0)
    main_storage = _room_storage(storage_size_w,storage_size_h)
    M.meld(main_storage, storage_start_w, 0)
    M[w-(w-stables_size_w)//2, storage_size_h].put(T.well())
    dog_place_x = random.randint(stables_size_w, w-1)
    dog_place_y = random.randint(storage_size_h+1, h-1)
    M[dog_place_x, dog_place_y].put(A.animal_dog())           
    if random.choice([True, False]):
        M.hmirror()

    return M

def _room_horse_stables(w,h, horse_box_size_w, horse_box_size_h):
    """
    Construct big stable with horse boxes.

    The stable consits of some small horse boxes with animal or without.
    """
    M = room_default(w, h, wall_type=C.wall_plank, floor_type=C.floor_rocks)
    number_of_horse_box = (h - 1) // 3

    # Place left and right rows of horse boxes.
    for y in range(number_of_horse_box):
        cell_y = 1 + (y*3)
        left_stable = _room_horse_box(horse_box_size_w, horse_box_size_h)
        M.meld(left_stable, 1, cell_y)
        right_stable = _room_horse_box(horse_box_size_w, horse_box_size_h, orientation='right')
        M.meld(right_stable, horse_box_size_w+2, cell_y)

        # Place fence after every horse box, except the last.
        if y == 0:
            continue
        for x in range(1, horse_box_size_w+1):
            M[x, cell_y-1] = C.wall_fence()
        for x in range(horse_box_size_w+2, w-1):
            M[x, cell_y-1] = C.wall_fence()
    M[w//2, h-1] = C.door_open_empty()
    return M

def _room_horse_box(w,h,orientation='left'):
    """
    Construct small horse box.
    """
    M = Map(w, h, fill_cell=C.floor_rocks)

    # Place watertrough and horse food.
    M[0, 0].put(T.water_trough())
    M[w-1, 0] = C.door_closed()
    M[0, h-1].put(T.water_trough())
    M[w-1, h-1] = C.wall_fence()
    if h > 2:
        for y in range(1, h-1):
            M[0, y].put(T.water_trough())
            M[w-1, y] = C.wall_fence()

    # Create horse box with animal or without.
    stable_with_horse_chance = random.random()
    all_coord = []
    while True:
        x = random.randint(1, w-2)
        y = random.randint(0, h-1)
        if (x, y) not in all_coord:
            M[x, y] = C.flora_grass()
            all_coord.append((x, y))
            break
    if stable_with_horse_chance > 0.3:
        while True:
            x = random.randint(1, w-2)
            y = random.randint(0, h-1)
            if (x, y) not in all_coord:
                M[x, y].put(T.farm_mangler())
                all_coord.append((x, y))
                break
        while True:
            x = random.randint(1, w-2)
            y = random.randint(0, h-1)
            if (x, y) not in all_coord:
                M[x, y].put(A.animal_horse())
                all_coord.append((x, y))
                break
    if orientation == 'right':
        M.hmirror()

    return M

def _room_storage(w, h):
    """
    Construct small storage with horse food and some stuff for stableman.
    """

    M = room_default(w, h, wall_type=C.wall_plank, floor_type=C.floor_dirt)
    number_of_items = (w-1) * (h-1) // 10

    # Place horse food.
    all_coord = []
    for item_class in (
        T.farm_mangler,
        T.furniture_barrel,
        T.furniture_box_filled
        ):
        for _ in range(number_of_items):
            while True:
                x = random.randint(1,w-2)
                y = random.randint(1,h*2//3-1)
                if (x, y) not in all_coord:
                    M[x, y].put(item_class())
                    all_coord.append((x, y))
                    break
    
    # Place horseman stuff.
    M[w//2-1, h-1] = C.door_closed()
    M[1, h-2].put(T.light_torch())
    M[1, h-4].put(T.furniture_napsack())
    M[w-2, h-2].put(T.furniture_table())
    M[w-2, h-3].put(T.furniture_chair())

    return M