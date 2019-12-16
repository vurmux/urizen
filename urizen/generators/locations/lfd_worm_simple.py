#!/usr/bin/python3

import random
from urizen.core.map import Map


NORTH = 'N'
SOUTH = 'S'
EAST = 'E'
WEST = 'W'


class LFD_WormSimpleFactory(object):

    def generate(self, w, h, length=None, turn_chance=0.4):
        if not length:
            length = int(w*h/2)
        return self._gen_main(w, h, length, turn_chance)

    def _gen_main(self, xsize, ysize, length, turn_chance=0.4):
        M = Map(xsize, ysize, fill_symbol='#')

        worm_x = random.randint(int(xsize * 0.3), int(xsize * 0.6))
        worm_y = random.randint(int(ysize * 0.3), int(ysize * 0.6))
        move = random.choice([NORTH, SOUTH, EAST, WEST])
        for _ in range(length):
            worm_x, worm_y, move = self._move_worm(M, worm_x, worm_y, move, turn_chance)

        return M

    def _move_worm(self, M, x, y, move, turn_chance):
        self._dig_cell(M, x, y)
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

    def _dig_cell(self, M, x, y):
        try:
            M.cells[y][x].symbol = '.'
        except IndexError:
            pass

LFD_WormSimple = LFD_WormSimpleFactory()