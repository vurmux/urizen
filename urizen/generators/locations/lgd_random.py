#!/usr/bin/python3

import random
from urizen.generators.basic_generator import BasicGenerator
from urizen.core.cell import Cell
from urizen.core.map import Map


class LGD_SimpleRandom(BasicGenerator):
    def generate(self, w, h):
        mask_map = [[1 for _ in range(w)] for _ in range(h)]
        for _ in range(20):
            x1 = random.randint(0, w-1)
            x2 = random.randint(x1, w-1)
            y1 = random.randint(0, h-1)
            y2 = random.randint(y1, h-1)
            mask_map = self._cut_rectangle(
                mask_map,
                x1, y1, x2, y2
            )
        M = Map(w, h)
        for i in range(h):
            for j in range(w):
                M.cells[i][j].symbol = '#' if mask_map[i][j] else '.'
        return M
    
    def _cut_rectangle(self, mask_map, x1, y1, x2, y2):
        for y in range(y1, y2):
            for x in range(x1, x2):
                mask_map[y][x] = 0
        return mask_map
