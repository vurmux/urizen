#!/usr/bin/python3

import random
from urizen.core.cell import Cell
from urizen.core.entity_collection import C


class Map(object):
    """
    Map class

    Attributes:
    w -- Map width
    h -- Map height
    cells -- Cell matrix
    fill_symbol -- Symbol to fill initial cell matrix
    tags -- Map tags
    """

    def __init__(self, w, h, fill_cell=Cell, tags=[]):
        self.w = w
        self.h = h
        self.tags = tags
        self.cells = [[fill_cell() for x in range(w)] for y in range(h)]
    
    def get_size(self):
        return self.w, self.h
    
    def __getitem__(self, pos):
        x, y = pos
        return self.cells[y][x]

    def __setitem__(self, pos, item):
        x, y = pos
        self.cells[y][x] = item
    
    def meld(self, other, x, y):
        ow, oh = other.get_size()
        if x + ow > self.w:
            raise IndexError('Melded map weigth is too big: {} + {} > {}'.format(x, ow, self.w))
        if y + oh > self.h:
            raise IndexError('Melded map height is too big: {} + {} > {}'.format(y, oh, self.h))
        for oy in range(oh):
            for ox in range(ow):
                self[x+ox, y+oy] = other[ox, oy]
    
    def transpose(self):
        self.w, self.h = self.h, self.w
        new_cells = []
        for line in zip(*self.cells):
            new_cells.append(list(line))
        self.cells = new_cells

    def hmirror(self):
        for line in self.cells:
            line.reverse()
    
    def vmirror(self):
        self.cells.reverse()

    def bordering(self, x, y):
        result = []
        if x > 0:
            result.append(self.cells[y][x-1])
        if x < self.w - 1:
            result.append(self.cells[y][x+1])
        if y > 0:
            result.append(self.cells[y-1][x])
        if y < self.h - 1:
            result.append(self.cells[y+1][x])
        return result

    def surrounding(self, x, y):
        result = []
        if x > 0:
            result.append(self.cells[y][x-1])
        if x < self.w - 1:
            result.append(self.cells[y][x+1])
        if y > 0:
            result.append(self.cells[y-1][x])
        if y < self.h - 1:
            result.append(self.cells[y+1][x])
        if x > 0 and y > 0:
            result.append(self.cells[y-1][x-1])
        if x < self.w - 1 and y > 0:
            result.append(self.cells[y-1][x+1])
        if x > 0 and y < self.h - 1:
            result.append(self.cells[y+1][x-1])
        if x < self.w - 1 and y < self.h - 1:
            result.append(self.cells[y+1][x+1])
        return result

    def up_to(self, x, y):
        if y <= 0:
            return C.unknown()
        else:
            return self.cells[y-1][x]

    def down_to(self, x, y):
        if y >= self.h - 1:
            return C.unknown()
        else:
            return self.cells[y+1][x]

    def left_to(self, x, y):
        if x <= 0:
            return C.unknown()
        else:
            return self.cells[y][x-1]

    def right_to(self, x, y):
        if x >= self.w - 1:
            return C.unknown()
        else:
            return self.cells[y][x+1]

    def scatter(self, x1, y1, x2, y2, entities, exclude=[]):
        if x2 < x1:
            raise IndexError('Bounding box x2 < x1: {} < {}'.format(x2, x1))
        if y2 < y1:
            raise IndexError('Bounding box y2 < y1: {} < {}'.format(y2, y1))
        if x1 < 0 or y1 < 0:
            raise IndexError('Bounding box x1/y1 < 0: {} or {} < 0'.format(x1, y1))
        if x2 > self.w or y2 > self.h:
            raise IndexError('Bounding box x2/y2 is too big: {} > {} or {} > {}'.format(x2, self.w, y2, self.h))

        free_cells = []
        exclude_with_tuple_coordinates = [(x, y) for x, y in exclude]
        for y in range(y1, y2):
            for x in range(x1, x2):
                cell_is_free = (
                    len(self.cells[y][x].actors) == 0 and
                    len(self.cells[y][x].things) == 0 and
                    (x, y) not in exclude_with_tuple_coordinates
                )
                if cell_is_free:
                    free_cells.append((x, y))

        sample_len = min(len(entities), len(free_cells))
        cells_sample = random.sample(free_cells, sample_len)
        entities_sample = random.sample(entities, sample_len)
        for i in range(sample_len):
            x, y = cells_sample[i]
            self.cells[y][x].put(entities_sample[i])
