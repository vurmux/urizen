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
    features -- List of features of the cell
    objects -- List of objects inside the cell
    symbol -- Symbol to print in terminal visualizers
    bg_color -- Background color in terminal visualizers
    fg_color -- Foreground color in terminal visualizers
    pixel_color -- Pixel color for pixel visualizers
    sprite -- Image or image generator in graphical visualizers
    passable -- Is the cell passable
    tags -- List of cell tags
    """

    height = 0
    terrain = None
    cell_type = None
    features = []
    objects = []
    symbol = '.'
    bg_color = '#000000'
    fg_color = '#FFFFFF'
    pixel_color = '#000000'
    sprite = None
    passable = False
    tags = []

    def __init__(self, x, y, z=0, **kwargs):
        self.x = x
        self.y = y
        self.z = z
        for arg, value in kwargs.items():
            if arg in Cell.__dict__ and not arg.startswith('__'):
                self.__dict__[arg] = value
