#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_building_floor_stone,
    cell_building_floor_wooden,
    cell_building_wall_stone,
    cell_building_wall_wooden,
    cell_building_closed_door,
    cell_dungeon_stairs_down
)
from urizen.core.thing_collection import (
    furniture_hearth,
    furniture_table,
    furniture_chair,
    furniture_bed,
    furniture_chest,
    furniture_wardrobe,
    other_bonfire,
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
    wall_cell_type = cell_building_wall_stone if material == 'stone' else cell_building_wall_wooden
    floor_cell_type = cell_building_floor_stone if material == 'stone' else cell_building_floor_wooden

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
        M[door_param, size-1] = cell_building_closed_door(door_param, size-1)
    else:
        M[0, door_param] = cell_building_closed_door(0, door_param)
    
    # Place bonfire or hearth in the middle of the room. Place chairs
    M[size//2-1, size//2].things.append(furniture_chair())
    M[size//2+1, size//2].things.append(furniture_chair())
    if type_house == 'hunter':
        M[size//2, size//2].things.append(furniture_hearth())
    else:
        M[size//2, size//2].things.append(other_bonfire())
    
    # Randomly choose where escape is. Place stairs and wardrobes. 
    escape = random.choice([True, False])
    if escape:
        M[size-2, 1] = cell_dungeon_stairs_down(size-2, 1)
        if type_house == 'robber':
            M[size-3, 1].things.append(furniture_wardrobe())
            M[size-3, 2].things.append(furniture_wardrobe())
            M[size-2, 2].things.append(furniture_wardrobe())
        elif type_house == 'hunter':
            M[size-2, size-2].things.append(furniture_wardrobe())
    else:
        M[1,1] = cell_dungeon_stairs_down(1,1)
        if type_house == 'robber':
            M[2, 1].things.append(furniture_wardrobe())
            M[2, 2].things.append(furniture_wardrobe())
            M[1, 2].things.append(furniture_wardrobe())
        elif type_house == 'hunter':
            M[size-2, size-2].things.append(furniture_wardrobe())

    # Place beds near walls
    beds_start = 1 if escape else size//3+1
    beds_end = size//2 if escape else size-1
    if escape:
        for x in range(beds_start, beds_end+1, 2):
            M[x, 1].things.append(furniture_bed())
    else:
        for x in range(beds_start+1, beds_end, 2):
            M[x, 1].things.append(furniture_bed())    

    # Place chests
    M[size-2, size//2-1].things.append(furniture_chest())
    M[size-2, size//2].things.append(furniture_chest())

    # Place table with chairs
    for x in range(size//5, size//2):
        M[x, size-2].things.append(furniture_table())
    for x in range(size//5+1, size//2, 2):
        M[x, size-3].things.append(furniture_chair())
    
    return M