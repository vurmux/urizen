#!/usr/bin/python3

from urizen.core.map import Map


def room_default(w, h, wall_type, floor_type):
    """
    Create an empty room with given wall type, floor type.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    
    wall_type : Cell
        Wall cell type

    floor_typr : Cell
        Floor cell type
    """

    M = Map(w, h, fill_cell=floor_type)

    # Create walls
    for x in range(0, w):
        M[x, 0] = wall_type()
        M[x, h-1] = wall_type()
    for y in range(0, h):
        M[0, y] = wall_type()
        M[w-1, y] = wall_type()

    return M