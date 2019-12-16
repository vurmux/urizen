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
    symbol -- Symbol to print in terminal visualizers
    bg_color -- Background color in terminal visualizers
    fg_color -- Foreground color in terminal visualizers
    sprite -- Image or image generator in graphical visualizers
    passable -- Is the cell passable
    tags -- List of cell tags
    """

    def __init__(self, x, y, z=0, height=0, terrain=None, cell_type=None, objects=[], symbol='.',
            bg_color='#000000', fg_color='#FFFFFF', sprite=None, passable=False, tags=[]):
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
        self.passable = passable
        self.tags = tags
