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
        self.cells = [[fill_cell(x, y) for x in range(w)] for y in range(h)]
    
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
        self.cells = list(zip(*self.cells))

    def hmirror(self):
        for line in self.cells:
            line.reverse()
    
    def vmirror(self):
        self.cells.reverse()