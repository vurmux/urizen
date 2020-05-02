#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_floor_flagged,
    cell_floor_plank,
    cell_wall_stone,
    cell_wall_plank,
    cell_door_closed,
    cell_stairs_down
)
from urizen.core.thing_collection import (
    item_furniture_hearth,
    item_furniture_table,
    item_furniture_stool,
    item_furniture_bed_single,
    item_furniture_chest,
    item_furniture_closet,
    item_furniture_bonfire,
)

def building_hunter_robber_house(size=10, material=None, type_house=None):
    """
    Construct the hunter or robber house.

    Parameters
    ----------
    size : int
        Square map size. This attribute will be applied for both `w` and `h`.
    
    material : string
        Wall material. Can be "wooden", "stone" or None. If None, a random
        material will be chosen.

    type_house : string
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
    wall_cell_type = cell_wall_stone if material == 'stone' else cell_wall_plank
    floor_cell_type = cell_floor_flagged if material == 'stone' else cell_floor_plank

    # Choose between robber house and hunter house
    if not type_house:
        type_house = random.choice(['robber', 'hunter'])
    if type_house not in ('robber', 'hunter'):
        raise ValueError('Type should be "robber" or "hunter"')

    M = Map(size, size, fill_cell=floor_cell_type)

    # Create outward walls
    for x in range(size):
        M[x, 0] = wall_cell_type(x, 0)
        M[x, size-1] = wall_cell_type(x, size-1)
    for y in range(size):
        M[0, y] = wall_cell_type(0, y)
        M[size-1, y] = wall_cell_type(size-1, y)

    # Create door
    door_random = random.choice([True, False])
    door_param = size//3 * 2
    if door_random:
        M[door_param, size-1] = cell_door_closed(door_param, size-1)
    else:
        M[0, door_param] = cell_door_closed(0, door_param)
    
    # Place bonfire or hearth in the middle of the room. Place chairs
    M[size//2-1, size//2].things.append(item_furniture_stool())
    M[size//2+1, size//2].things.append(item_furniture_stool())
    if type_house == 'hunter':
        M[size//2, size//2].things.append(item_furniture_hearth())
    else:
        M[size//2, size//2].things.append(item_furniture_bonfire())
    
    # Randomly choose where escape is. Place stairs and wardrobes. 
    escape = random.choice([True, False])
    if escape:
        M[size-2, 1] = cell_stairs_down(size-2, 1)
        if type_house == 'robber':
            M[size-3, 1].things.append(item_furniture_closet())
            M[size-3, 2].things.append(item_furniture_closet())
            M[size-2, 2].things.append(item_furniture_closet())
        elif type_house == 'hunter':
            M[size-2, size-2].things.append(item_furniture_closet())
    else:
        M[1,1] = cell_stairs_down(1,1)
        if type_house == 'robber':
            M[2, 1].things.append(item_furniture_closet())
            M[2, 2].things.append(item_furniture_closet())
            M[1, 2].things.append(item_furniture_closet())
        elif type_house == 'hunter':
            M[size-2, size-2].things.append(item_furniture_closet())

    # Place beds near walls
    beds_start = 1 if escape else size//3+1
    beds_end = size//2 if escape else size-1
    if escape:
        for x in range(beds_start, beds_end+1, 2):
            M[x, 1].things.append(item_furniture_bed_single())
    else:
        for x in range(beds_start+1, beds_end, 2):
            M[x, 1].things.append(item_furniture_bed_single())    

    # Place chests
    M[size-2, size//2-1].things.append(item_furniture_chest())
    M[size-2, size//2].things.append(item_furniture_chest())

    # Place table with chairs
    for x in range(size//5, size//2):
        M[x, size-2].things.append(item_furniture_table())
    for x in range(size//5+1, size//2, 2):
        M[x, size-3].things.append(item_furniture_stool())
    
    return M