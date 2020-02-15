#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import cell_dungeon_wall, cell_dungeon_floor


NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'


def dungeon_drunkard(w, h, length=None, turn_chance=0.4):
    M = Map(w, h, fill_cell=cell_dungeon_wall)
    if not length:
        length = int(w*h/2)
    worm_x = random.randint(int(w * 0.3), int(w * 0.6))
    worm_y = random.randint(int(h * 0.3), int(h * 0.6))
    move = random.choice([NORTH, SOUTH, EAST, WEST])
    for _ in range(length):
        M.cells[worm_y][worm_x] = cell_dungeon_floor(worm_x, worm_y)
        worm_x, worm_y, move = _move_worm(M, worm_x, worm_y, move, turn_chance)

    return M

def _move_worm(M, x, y, move, turn_chance):
    if random.random() > turn_chance:
        move = random.choice([NORTH, SOUTH, EAST, WEST])

    xsize, ysize = M.get_size()
    if x == xsize - 2 and move == EAST:
        move = WEST
    elif x == 1 and move == WEST:
        move = EAST
    elif y == ysize - 2 and move == SOUTH:
        move = NORTH
    elif y == 1 and move == NORTH:
        move = SOUTH

    if move == NORTH:
        new_state = [x, y - 1]
    elif move == SOUTH:
        new_state = [x, y + 1]
    elif move == EAST:
        new_state = [x + 1, y]
    else:
        new_state = [x - 1, y]
    new_state.append(move)
    return new_state
