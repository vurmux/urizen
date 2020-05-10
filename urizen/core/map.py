#!/usr/bin/python3

from urizen.core.cell import Cell


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
            return None
        else:
            return self.cells[y-1][x]

    def down_to(self, x, y):
        if y >= self.h - 1:
            return None
        else:
            return self.cells[y+1][x]

    def left_to(self, x, y):
        if x <= 0:
            return None
        else:
            return self.cells[y][x-1]

    def right_to(self, x, y):
        if x >= self.w - 1:
            return None
        else:
            return self.cells[y][x+1]
