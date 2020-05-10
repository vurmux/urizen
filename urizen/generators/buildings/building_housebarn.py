#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T


def building_housebarn(w=30, h=15, material=None):
    """
    Construct the housebarn (also known as longhouse) building interior.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    
    material : string
        Wall material. Can be "wooden", "stone" or None. If None, a random
        material will be chosen.
    """

    # Initial checks. Don't accept:
    # - Too small buildings
    # - Too long/square buildings
    # - Wall types that are not "stone" or "wooden"
    if w < 10 or h < 10:
        raise ValueError('Building is too small: w/h < 10')
    if not material:
        material = random.choice(['wooden', 'stone'])
    if material not in ('wooden', 'stone'):
        raise ValueError('Material should be "stone" or "wooden"')
    wall_cell_type = C.wall_stone if material == 'stone' else C.wall_plank

    is_horizontal = True if w >= h else False
    if is_horizontal:
        if w < h * 2 or w > h * 3:
            raise ValueError('Building is too long or too short.')
    else:
        if h < w * 2 or h > w * 3:
            raise ValueError('Building is too long or too short.')

    # If parameters are vertial, we firstly construct horizontal building then transpose it.
    # It allows not to use two additional different subtypes of the building which will simplify the code.
    if not is_horizontal:
        w, h = h, w
    M = Map(w, h, fill_cell=C.floor_flagged)

    # Create outward walls
    for x in range(w):
        M[x, 0] = wall_cell_type()
        M[x, h-1] = wall_cell_type()
    for y in range(h):
        M[0, y] = wall_cell_type()
        M[w-1, y] = wall_cell_type()

    # Randomly choose where the living part is
    living_left = random.choice([True, False])
    living_wall_x = None
    barn_wall_x = None

    # Place central doors/corridor and calculate X-positions for vertical walls
    if w % 2 == 0:
        M[w//2, 0] = C.floor_flagged()
        M[w//2-1, 0] = C.floor_flagged()
        M[w//2, h-1] = C.floor_flagged()
        M[w//2-1, h-1] = C.floor_flagged()
        living_wall_x = (w // 2 - 3) if living_left else (w // 2 + 2)
        barn_wall_x = (w // 2 + 2) if living_left else (w // 2 - 3)
    else:
        M[w//2, 0] = C.door_closed_wooden()
        M[w//2, h-1] = C.door_closed_wooden()
        living_wall_x = (w // 2 - 2) if living_left else (w // 2 + 2)
        barn_wall_x = (w // 2 + 2) if living_left else (w // 2 - 2)

    # Place vertical walls
    for i in range(1, h//3):
        M[living_wall_x, i] = wall_cell_type()
        M[living_wall_x, h-i-1] = wall_cell_type()
    for i in range(1, h-1):
        M[barn_wall_x, i] = C.wall_fence_thin()
    M[barn_wall_x, h//2] = C.door_closed_wooden()

    # Create living room:
    # Set initial coordinates
    lx_start = 1 if living_left else living_wall_x + 1
    lx_end = living_wall_x - 1 if living_left else w - 1
    beds_dx = int((lx_end - lx_start) % 2 == 0 and not living_left)
    beds_dy = random.choice([0, 1])

    # Place beds near walls or at 1 cell from walls
    for bed_x in range(lx_start + beds_dx, lx_end, 2):
        M[bed_x, 1+beds_dy].put(T.furniture_bed_single())
        M[bed_x, h-2-beds_dy].put(T.furniture_bed_single())

    # Place bonfire in the middle of the room or hearth on the side of the room
    is_bonfire = random.choice([True, False])
    if is_bonfire:
        M[(lx_start+lx_end)//2, h//2].put(T.bonfire())
    elif living_left:
        M[1, h//2].put(T.furniture_hearth())
    else:
        M[w-2, h//2].put(T.furniture_hearth())

    # Create barn:
    # Set initial coordinates
    bx_start = 1 if not living_left else barn_wall_x + 1
    bx_end = barn_wall_x - 1 if not living_left else w - 2
    
    # Fill the barn floor with dirt
    for x in range(bx_start, bx_end + 1):
        for y in range(1, h-1):
            M[x, y] = C.floor_dirt()

    is_central_barn = random.choice([True, False])
    if is_central_barn:
        # Central barn: stalls in the center, two waterthroughs on the side
        for y in range(h//3, h*2//3):
            M[bx_start+2, y] = C.wall_fence_thin()
        for x in range(bx_start + 3, bx_end - 2, 2):
            M[x, h//2] = C.wall_fence_thin()
            M[x, h//2-1].put(T.farm_mangler())
            M[x, h//2+1].put(T.farm_mangler())
            for y in range(h//3, h*2//3):
                M[x+1, y] = C.wall_fence_thin()
        for x in range(bx_start + 1, bx_end):
            M[x, 1].put(T.water_trough())
            M[x, h-2].put(T.water_trough())
    else:
        # Side barn: stalls on the side, one waterthrough in the center
        for x in range(bx_start, bx_end - 1, 2):
            M[x, 1].put(T.farm_mangler())
            M[x, h-2].put(T.farm_mangler())
            for y in range(1, h//3):
                M[x+1, y] = C.wall_fence_thin()
            for y in range(h*2//3, h-1):
                M[x+1, y] = C.wall_fence_thin()
        for x in range(bx_start + 2, bx_end - 1):
            M[x, h//2].put(T.water_trough())

    # Transpose the building if it should be vertical
    if not is_horizontal:
        M.transpose()

    return M
