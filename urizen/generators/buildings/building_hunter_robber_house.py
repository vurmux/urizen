#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C, T


def building_hunter_robber_house(size=10, material=None, house_type=None):
    """
    Construct the hunter or robber house.

    Parameters
    ----------
    size : int
        Square map size. This attribute will be applied for both `w` and `h`.
    
    material : string
        Wall material. Can be "wooden", "stone" or None. If None, a random
        material will be chosen.

    house_type : string
        Type of the house. Can be "hunter" or "robber". If None, a random 
        type will be chosen.
    """

    # Initial check. Don't accept too small/big building
    if size < 8 or size > 17:
        raise ValueError('Building is too small or too big: size < 8 or size > 17')

    # Choose materials
    if not material:
        material = random.choice(['wooden', 'stone'])
    if material not in ('wooden', 'stone'):
        raise ValueError('Material should be "stone" or "wooden"')
    wall_cell_type = C.wall_stone if material == 'stone' else C.wall_plank
    floor_cell_type = C.floor_flagged if material == 'stone' else C.floor_plank

    # Choose between robber house and hunter house
    if not house_type:
        house_type = random.choice(['robber', 'hunter'])
    if house_type not in ('robber', 'hunter'):
        raise ValueError('Type should be "robber" or "hunter"')

    M = Map(size, size, fill_cell=floor_cell_type)

    # Create outward walls
    for x in range(size):
        M[x, 0] = wall_cell_type()
        M[x, size-1] = wall_cell_type()
    for y in range(size):
        M[0, y] = wall_cell_type()
        M[size-1, y] = wall_cell_type()

    # Create door
    door_random = random.choice([True, False])
    door_param = size//3 * 2
    if door_random:
        M[door_param, size-1] = C.door_closed()
    else:
        M[0, door_param] = C.door_closed()
    
    # Place bonfire or hearth in the middle of the room. Place chairs
    M[size//2-1, size//2].put(T.furniture_chair())
    M[size//2+1, size//2].put(T.furniture_chair())
    if house_type == 'hunter':
        M[size//2, size//2].put(T.furniture_hearth())
    else:
        M[size//2, size//2].put(T.bonfire())
    
    # Randomly choose where escape is. Place stairs and wardrobes. 
    escape = random.choice([True, False])
    if escape:
        M[size-2, 1] = C.stairs_down()
        if house_type == 'robber':
            M[size-3, 1].put(T.furniture_closet())
            M[size-3, 2].put(T.furniture_closet())
            M[size-2, 2].put(T.furniture_closet())
        elif house_type == 'hunter':
            M[size-2, size-2].put(T.furniture_closet())
    else:
        M[1,1] = C.stairs_down()
        if house_type == 'robber':
            M[2, 1].put(T.furniture_closet())
            M[2, 2].put(T.furniture_closet())
            M[1, 2].put(T.furniture_closet())
        elif house_type == 'hunter':
            M[size-2, size-2].put(T.furniture_closet())

    # Place beds near walls
    beds_start = 1 if escape else size//3+1
    beds_end = size//2 if escape else size-1
    if escape:
        for x in range(beds_start, beds_end+1, 2):
            M[x, 1].put(T.furniture_bed_single())
    else:
        for x in range(beds_start+1, beds_end, 2):
            M[x, 1].put(T.furniture_bed_single())    

    # Place chests
    M[size-2, size//2-1].put(T.furniture_chest())
    M[size-2, size//2].put(T.furniture_chest())

    # Place table with chairs
    for x in range(size//5, size//2):
        M[x, size-2].put(T.furniture_longtable())
    for x in range(size//5+1, size//2, 2):
        M[x, size-3].put(T.furniture_chair())
    
    return M