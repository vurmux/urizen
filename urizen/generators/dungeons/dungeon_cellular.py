#!/usr/bin/python3

import random
from copy import deepcopy
from urizen.core.map import Map
from urizen.core.entity_collection import C


def dungeon_cellular_simple(w, h, start_floor_chance=0.55, smooth_level=3):
    """
    Construct the dungeon map using simple cellular automata.

    Note that this map can contain disconnected areas.

    Visual
    ------
    Natural-looking cave-like map.

    Parameters
    ----------
    w : int
        Map width

    h : int
        Map height
    
    start_floor_chance : float
        Chance of the floor cell in the first map fill
    
    smooth_level : int
        Number of sequential smooth functions
    """

    M = Map(w, h, fill_cell=C.wall_cave)

    # Randomly fill all-but-border cells by floor with start_floor_chance probability
    for y, line in enumerate(M.cells[1: -1]):
        for x, _ in enumerate(line[1: -1]):
            chance = random.random()
            if chance <= start_floor_chance:
                M.cells[y+1][x+1] = C.floor_dirt()
    
    # Sequentially smooth the map smooth_level times
    for _ in range(smooth_level):
        M = _smooth_map(M)

    return M

def _smooth_map(M):
    """
    Smooth a map using cellular automata.

    If number of walls around the cell (including it) is more than number of floors, replace the cell with a wall.
    In other case replace the cell with a floor.
    """

    # Already replaced cells must not affect current so we need a copy of the original map 
    M2 = deepcopy(M)
    for y, line in enumerate(M2.cells[1: -1]):
        for x, _ in enumerate(line[1: -1]):
            true_x = x + 1
            true_y = y + 1
            # Check the number of walls in ORIGINAL map
            number_of_walls = sum(
                cell.__class__.__name__ == 'wall_cave'
                for cell in [
                    M.cells[true_y][true_x],
                    M.cells[true_y+1][true_x],
                    M.cells[true_y-1][true_x],
                    M.cells[true_y][true_x+1],
                    M.cells[true_y+1][true_x+1],
                    M.cells[true_y-1][true_x+1],
                    M.cells[true_y][true_x-1],
                    M.cells[true_y+1][true_x-1],
                    M.cells[true_y-1][true_x-1],
                ]
            )
            # And set them in smoothed map
            M2.cells[true_y][true_x] = (
                C.wall_cave()
                if number_of_walls >= 5
                else C.floor_dirt()
            )
    return M2