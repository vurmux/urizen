#!/usr/bin/python3


class Cell(object):
    """
    Cell class

    Attributes:
    x -- X coordinate
    y -- Y coordinate
    z -- Z coordinate
    height -- Cell height
    terrain -- Cell terrain
    cell_type -- Cell type
    objects -- List of objects inside the cell
    """

    def __init__(self, x, y, z=0, height=0, terrain=None, cell_type=None, objects=[], symbol='.',
            bg_color=None, fg_color=None, sprite=None):
        self.x = x
        self.y = y
        self.z = z
        self.height = height
        self.terrain = terrain
        self.cell_type = cell_type
        self.objects = objects
        self.symbol = symbol
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.sprite = sprite
