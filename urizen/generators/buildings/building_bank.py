#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T, A

from urizen.generators.rooms.room_default import room_default


def building_bank(w=21, h=21, direction='down'):
    """
    Construct bank with big vault, employee office, rich part and poor part.

    Rich part consists of two private rooms and luxury hall. Poor part consists of small office rooms and big hall.

    Constraints:

        - Map width and map height must be >= 19 and <= 31.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    """
    
    # Initial checks. Don't accept too small/big bank
    if w < 19 or h < 19:
        raise ValueError('Building is too small: w or h < 16')
    elif w > 31 or h > 31:
        raise ValueError('Building is too big: w or h > 25')
    M = room_default(w, h, wall_type=C.wall_dungeon_smooth, floor_type=C.floor_plank)

    # Calculate office and vault heights based upon map height.
    office_h = (h - 11) // 2 + 1
    vault_h = office_h if h % 2 == 1 else office_h + 1

    # Meld rooms and vault.
    M.meld(_room_vault(w, vault_h), 0, 0)
    M.meld(_room_big_office(w, office_h), 0, vault_h - 1)
    M.meld(_room_private(6, 7), 0, vault_h+office_h-2)
    M.meld(_room_private(6, 7), 5, vault_h+office_h-2)
    M.meld(_room_rich_hall(11, 5), 0, vault_h+office_h+4)
    building_poor_w = w - 10
    M.meld(_room_poor_part(building_poor_w, 11), 10, vault_h + office_h - 2)

    if direction == 'up':
        M.vmirror()
    elif direction == 'left':
        M.transpose()
    elif direction == 'right':
        M.transpose()
        M.hmirror()

    return M

def _room_vault(w, h):
    """
    Construct vault with treasures.
    """
    M = room_default(w, h, wall_type=C.wall_dungeon_smooth, floor_type=C.floor_plank)
    # Place treasures in the vault
    # There are 11 types of items. We fill 60% of vault cells with items in the equal proportion.
    number_of_items = int(((w-2) * (h-2) * 0.6) // 11)
    all_coord = [(w//2, h-2)]
    for item_class in (
            T.material_ingot, 
            T.money_pile,
            T.money_coin,
            T.bag,
            T.mineral_crystal,
            T.mineral_diamond,
            T.necklace,
            T.ring,
            T.scroll_text,
            T.furniture_chest,
            T.furniture_chest_full,
            ):
        for _ in range(number_of_items):
            while True:
                x = random.randint(1, w-2)
                y = random.randint(1, h-2)
                if (x, y) not in all_coord:
                    M[x, y].put(item_class())
                    all_coord.append((x, y))
                    break

    return M

def _room_big_office(w, h):
    """
    Construct big office only for employees.
    """
    M = room_default(w, h, wall_type=C.wall_dungeon_smooth, floor_type=C.floor_plank)

    # Place lanterns and bookcases from the center to the right end of the room.
    M[w//2, 0] = C.door_closed_bars()
    for y in range(1, h-3, 2):
        M[w-2, y].put(T.light_lantern_oil())
        for x in range(w//2+1, w-1):
            M[x, y+1].put(T.furniture_bookcase())

    # Place tables, chairs, etc.
    for y in range(3, h-1, 2):
        M[1, y].put(T.furniture_table())
        M[2, y].put(T.furniture_chair())
        M[3, y].put(T.light_lantern_oil())
        M[6, y].put(T.furniture_table())
        M[7, y].put(T.furniture_chair())
        if w > 26:
            M[10, y].put(T.furniture_table())
            M[11, y].put(T.furniture_chair())
    all_coord = []
    for item_class in (
            T.furniture_bookcase,
            T.book_clear,
            T.book,
            T.furniture_bookcase,
            T.furniture_bookcase,
            T.scroll_text
            ):
        while True:
            x = random.randint(1, w//2-2)
            y = 1
            if (x, y) not in all_coord:
                M[x, y].put(item_class())
                all_coord.append((x, y))
                break

    return M

def _room_private(w, h, orientation='left'):
    """
    Construct private room.
    """
    M = room_default(w, h, wall_type=C.wall_dungeon_smooth, floor_type=C.floor_plank)

    # Place some things.
    M[1, 1].put(T.book())
    M[1, h//2].put(T.furniture_longtable())
    for x in range(1, w-2):
        M[x, h//2+1].put(T.furniture_chair())
    M[w//2-1, h//2-1].put(T.furniture_chair())
    if w > 5:
        for x in range(2, w-3):
            M[x, h//2].put(T.furniture_longtable())
    M[w-3, h//2].put(T.furniture_longtable())
    M[w-2, 0] = C.door_closed()
    M[w-2, h//2].put(T.furniture_chandelier())

    if orientation == 'right':
        M.hmirror()
    
    return M

def _room_rich_hall(w, h):
    """
    Construct luxury hall.
    """
    M = room_default(w, h, wall_type=C.wall_dungeon_smooth, floor_type=C.floor_plank)

    # Place sofa, flowers, etc.
    M[1, 1] = C.flora_flower()
    M[w//2, 1] = C.column_antique()
    M[w-2, 1] = C.flora_flower()
    M[1, 2].put(T.furniture_sofa())
    M[w-2, 2].put(T.furniture_sofa())
    M[w//2-1, h-2].put(T.furniture_chandelier())
    M[w//2+1, h-2].put(T.furniture_chandelier())
    M[2, 0] = C.door_closed()
    M[7, 0] = C.door_closed()
    M[w//2, h-1] = C.door_closed_wooden()
    return M

def _room_poor_part(w, h):
    """
    Construct poor part of the bank.

    It consists small office rooms for employees and hall for poors.
    """
    M = room_default(w, h, wall_type=C.wall_dungeon_smooth, floor_type=C.floor_plank)

    # Every small office has width=5 (with walls), except the last, so each small office will occupy 4 cells in width.
    num_of_small_office = w // 4

    # Calculate w-size of the last small office.
    shift_w = w % 4
    if shift_w == 1:
        small_room_w = 5
    elif shift_w == 2:
        small_room_w = 6
    elif shift_w == 3:
        small_room_w = 7
    elif shift_w == 0:
        small_room_w = 6

    # Place small office rooms.
    if shift_w == 1:
        # All small offices has an equal width and fill all width of the room.
        for cell_index in range(num_of_small_office):
            cell_x = cell_index * 4
            M_cell = _room_small_office(w=small_room_w, h=5)
            M.meld(M_cell, cell_x, 0)
    elif shift_w == 0:
        # The last small office is wider and there is the corridor to the main office in the end of the room.
        for cell_index in range(num_of_small_office - 1):
            cell_x = cell_index * 4
            M_cell = _room_small_office(w=5, h=5)
            M.meld(M_cell, cell_x, 0)
        M_room = _room_small_office(w=small_room_w, h=5)
        M.meld(M_room, (num_of_small_office-2)*4, 0)
        M[w-2, 0] = C.floor_plank()
        M[w-2, 4] = C.door_closed()
    else:
        # The last small office is wider and small offices fill all width of the room.
        for cell_index in range(num_of_small_office - 1):
            cell_x = cell_index * 4
            M_cell = _room_small_office(w=5, h=5)
            M.meld(M_cell, cell_x, 0)
        M_room = _room_small_office(w=small_room_w, h=5)
        M.meld(M_room, (num_of_small_office-1)*4, 0)

    # Place two longtables in right and left part of hall and some chairs.
    table_length = w // 3
    for x in range(1, table_length):
        M[x, h-4].put(T.furniture_longtable())
    for x in range(1, table_length, 2):
        M[x, h-3].put(T.furniture_stool())
    for x in range(w-table_length, w-1):
        M[x, h-4].put(T.furniture_longtable())
    for x in range(w-table_length, w-1, 2):
        M[x, h-3].put(T.furniture_stool())

    M[w//2, h-1] = C.door_closed()

    return M

def _room_small_office(w, h):
    """
    Construct small office for employees in poor part.
    """
    M = room_default(w, h, wall_type=C.wall_dungeon_smooth, floor_type=C.floor_plank)

    # Place things and actor - employee.
    work_chance = random.choice([True, False])
    M[w//2, 0] = C.door_open_empty()
    M[1, h-1] = C.wall_bars()
    M[w-2, h-1] = C.wall_bars()
    M[2, h-1].put(T.furniture_longtable())
    if w > 5:
        for x in range(2, w-2):
            M[x, h-1].put(T.furniture_longtable())
    M[w//2, h-2].put(T.furniture_chair())
    M[w-2, 1].put(T.furniture_bookcase())
    M[1, 1].put(T.money_pile())
    if work_chance:
        M[1, h-2].put(A.player_female())
        M[w-2, h-2].put(T.book())
    else:
        M[w-2, h-2].put(T.book_clear())

    return M