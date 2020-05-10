#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T
from urizen.generators.rooms.room_prison_cell import room_prison_cell


def building_prison(w, h):
    """
    Construct a prison interior.

    This function choose different prison construction algorithms depends on given prison size.

    Possible algorithms are:

        - Linear prison - with linear corridor, cells on the side of it and rooms on it's ends.
        - Rectangular prison - with rectangular corridor, cells outside of it and rooms inside.
    
    Constraints:

        - Map width and map height must be >= 11.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    
    """

    if w >= 17 and h >= 17:
        return building_prison_rectangular(w, h)
    elif w >= h:
        return building_prison_linear(w, h)
    else:
        return building_prison_linear(w, h, orientation='vertical')


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
    M = Map(w, h, fill_cell=C.void)

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
            M[w-1, y] = C.wall_stone()
            M[w-5, y] = C.wall_stone()
        for x in range(w-5, w):
            M[x, jailer_y_start] = C.wall_stone()
            M[x, jailer_y_end] = C.wall_stone()
        for y in range(jailer_y_start+1, jailer_y_end):
            for x in range(w-4, w-1):
                M[x, y] = C.floor_flagged()   
        M[w-5, h//2] = C.door_closed()

        # Place some furniture
        M[w-4, jailer_y_start+1].put(T.furniture_table())
        M[w-3, jailer_y_start+1].put(T.furniture_table())
        M[w-2, jailer_y_start+1].put(T.furniture_chair())
        M[w-4, jailer_y_end-1].put(T.furniture_torch())
        M[w-3, jailer_y_end-1].put(T.furniture_bed_single())
        M[w-2, jailer_y_end-1].put(T.furniture_chest())
    else:
        # Create walls, floor and door
        for y in range(jailer_y_start, jailer_y_end+1):
            M[0, y] = C.wall_stone()
            M[4, y] = C.wall_stone()
        for x in range(0, 5):
            M[x, jailer_y_start] = C.wall_stone()
            M[x, jailer_y_end] = C.wall_stone()
        for y in range(jailer_y_start+1, jailer_y_end):
            for x in range(1, 4):
                M[x, y] = C.floor_flagged()
        M[4, h//2] = C.door_closed()

        # Place some furniture
        M[1, jailer_y_start+1].put(T.furniture_table())
        M[2, jailer_y_start+1].put(T.furniture_table())
        M[3, jailer_y_start+1].put(T.furniture_chair())
        M[1, jailer_y_end-1].put(T.furniture_chest())
        M[2, jailer_y_end-1].put(T.furniture_bed_single())
        M[3, jailer_y_end-1].put(T.furniture_torch())

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
            M[x, 0] = C.wall_stone()
            M[x, h-1] = C.wall_stone()
        for y in range(0, h-1):
            M[torture_start, y] = C.wall_stone()
            M[torture_end, y] = C.wall_stone()
        for x in range(torture_start+1, torture_end):
            for y in range(1, h-1):
                M[x, y] = C.floor_flagged()
        M[torture_end, h//2] = C.door_closed()

        # Place some furniture. If torture_end == 2 (just a corridor), then we set only stairs.
        M[torture_end-1, h-2] = C.stairs_up()
        if torture_end != 2:
            M[(torture_end-torture_start)//2, h//2].put(T.furniture_torture())
            all_coord = [(torture_end-1, h-2), ((torture_end-torture_start)//2, h//2)]
            for item_class in (T.bones, T.bones_skull, T.tool_tongs):
                while True:
                    x = random.randint(1, torture_end-1)
                    y = random.randint(1, h-2)
                    if (x, y) not in all_coord:
                        M[x, y].put(item_class())
                        all_coord.append((x,y))
                        break
    else:
        # If torture room is right, we are using the torture room width for calculations.
        # If torture_width = 7, then we reduce torture room for a one cell's width (-4).
        torture_width = w % 4 + 4
        if torture_width == 7:
            torture_width = 3
        torture_end = w - 1

        # Create walls, floor and door
        for x in range(w-torture_width, torture_end):
            M[x, 0] = C.wall_stone()
            M[x, h-1] = C.wall_stone()
        for y in range(0, h):
            M[w-torture_width, y] = C.wall_stone()
            M[torture_end, y] = C.wall_stone()
        for x in range(w-torture_width+1, torture_end):
            for y in range(1, h-1):
                M[x, y] = C.floor_flagged()
        M[w-torture_width, h//2] = C.door_closed()

        # Place some furniture. If torture_width = 3 (just a corridor), then we set only stairs.
        M[w-2, h-2] = C.stairs_up()
        if torture_width != 3:
            M[w-2, h//2].put(T.furniture_torture())
            all_coord = [(w-1, h-2), (w-2, h//2)]
            for item_class in (T.bones, T.bones_skull, T.tool_tongs):
                while True:
                    x = random.randint(w-torture_width+1, w-2)
                    y = random.randint(1,h-2)
                    if (x, y) not in all_coord:
                        M[x, y].put(item_class())
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
            M[x, h//2] = C.floor_flagged()
    else:
        for x in range(cor_start, cor_end+1):
            M[x, h//2-1] = C.floor_flagged()
            M[x, h//2] = C.floor_flagged()
    
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

def building_prison_rectangular(w=17, h=17):
    """
    Construct a rectangular prison interior.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    
    """
    
    # Initial checks. Don't accept too small prisons
    if w < 17 or h < 17:
        raise ValueError('Building is too small: w or h < 17')
    M = Map(w, h, fill_cell=C.void)

    # Calculate prison cells sizes depends on prison size.
    cell_shift_w = (w - 1) % 4
    if cell_shift_w == 1:
        left_w = 4
        right_w = 5
    elif cell_shift_w == 2:
        left_w = 5
        right_w = 5
    elif cell_shift_w == 3:
        left_w = 5
        right_w = 6
    else:
        left_w = 4
        right_w = 4

    cell_shift_h = (h - 1) % 4
    if cell_shift_h == 1:
        top_h = 4
        bottom_h = 5
    elif cell_shift_h == 2:
        top_h = 5
        bottom_h = 5
    elif cell_shift_h == 3:
        top_h = 5
        bottom_h = 6
    else:
        top_h = 4
        bottom_h = 4

    # Calculate the number of prison cells fits horizontally/vertically
    num_cell_w = (w - left_w - right_w) // 4
    num_cell_h = (h - top_h - bottom_h) // 4

    # Place cells
    for cell_index in range(num_cell_w):
        cell_x = left_w + (cell_index * 4)

        # Place upper cell
        M_cell = room_prison_cell(w=5, h=top_h+1)
        M.meld(M_cell, cell_x, 0)

        # Place lower cell
        M_cell = room_prison_cell(w=5, h=bottom_h+1, direction='up')
        M.meld(M_cell, cell_x, h-bottom_h-1)

    for cell_index in range(num_cell_h):
        cell_y = top_h + (cell_index * 4)

        # Place left cell
        M_cell = room_prison_cell(w=left_w+1, h=5, direction='left')
        M.meld(M_cell, 0, cell_y)

        # Place right cell
        M_cell = room_prison_cell(w=right_w+1, h=5, direction='right')
        M.meld(M_cell, w-right_w-1, cell_y)

    center_room_w = w - (left_w + 1) - (right_w + 1) - 2
    center_room_h = h - (top_h + 1) - (bottom_h + 1) - 2

    center_room = _room_prison_center(center_room_w, center_room_h)
    M.meld(center_room, left_w+2, top_h+2)

    # Construct the corridor
    for x in range(left_w+1, w-right_w-1):
        M[x, top_h+1] = C.floor_flagged()
        M[x, h-bottom_h-2] = C.floor_flagged()
    for y in range(top_h+1, h-bottom_h-1):
        M[left_w+1, y] = C.floor_flagged()
        M[w-right_w-2, y] = C.floor_flagged()

    return M
    
def _room_prison_center(w=5, h=5):
    M = Map(w, h, fill_cell=C.floor_flagged)
    if w > 8 and h > 4:
        jailer_room = _room_jailer(w//2+1, h)
        M.meld(jailer_room, 0, 0)
        torture_room = _room_torture(w-w//2, h)
        M.meld(torture_room, (w-w//2)-1, 0)
    elif h > 8 and w > 4:
        jailer_room = _room_jailer(w, h//2+1)
        M.meld(jailer_room, 0, 0)
        torture_room = _room_torture(w, h-h//2)
        M.meld(torture_room, 0, (h-h//2)-1)
    else:
        for x in range(0, w):
            M[x, 0] = C.wall_stone()
            M[x, h-1] = C.wall_stone()
        for y in range(0, h):
            M[0, y] = C.wall_stone()
            M[w-1, y] = C.wall_stone()
        M[w//2, 0] = C.door_closed()
        M[w//2, h//2] = C.stairs_up()
    
    return M

def _room_jailer(w=5, h=5):
    M = Map(w, h, fill_cell=C.floor_flagged)

    # Create walls
    for x in range(0, w):
        M[x, 0] = C.wall_stone()
        M[x, h-1] = C.wall_stone()
    for y in range(0, h):
        M[0, y] = C.wall_stone()
        M[w-1, y] = C.wall_stone()
    M[w//2, 0] = C.door_closed()
    

    # Place furniture and items in the room
    all_coord = [(w//2, 1)]
    for item_class in (T.furniture_bed_single,
            T.furniture_chest,
            T.furniture_chair,
            T.furniture_table,
            T.furniture_torch):
        while True:
            x = random.randint(1, w-2)
            y = random.randint(1, h-2)
            if (x, y) not in all_coord:
                M[x, y].put(item_class())
                all_coord.append((x, y))
                break
    return M

def _room_torture(w=5, h=5):
    M = Map(w, h, fill_cell=C.floor_flagged)

    # Create walls
    for x in range(0, w):
        M[x, 0] = C.wall_stone()
        M[x, h-1] = C.wall_stone()
    for y in range(0, h):
        M[0, y] = C.wall_stone()
        M[w-1, y] = C.wall_stone()
    M[w//2, h-1] = C.door_closed()
    M[w//2+1, h-2] = C.stairs_up()
    

    # Place furniture and items in the room
    M[w//2, h//2].put(T.furniture_torture())
    all_coord = [(w//2, h-2), (w//2, h//2), (w//2+1, h-2)]
    for item_class in (T.bones, T.bones_skull, T.tool_tongs):
            while True:
                x = random.randint(1, w-2)
                y = random.randint(1, h-2)
                if (x, y) not in all_coord:
                    M[x, y].put(item_class())
                    all_coord.append((x, y))
                    break
    return M