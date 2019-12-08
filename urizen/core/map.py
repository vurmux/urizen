#!/usr/bin/python3

from urizen.core.cell import Cell


class Map(object):
    """
    Map class

    Attributes:
    w -- Map width
    h -- Map height
    cells -- Cell matrix
    """

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.cells = [[Cell(x, y) for x in range(w)] for y in range(h)]