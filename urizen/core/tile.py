#!/usr/bin/python3


class Tile(object):
    """
    Tile class

    Attributes:
    image -- Image or image generator in graphical visualizers
    """

    height = 1
    terrain = None
    cell_type = None
    symbol = '.'
    bg_color = '#000000'
    fg_color = '#FFFFFF'
    pixel_color = '#000000'
    sprite = None
    passable = False
    tags = []

    def __init__(self, name, image, tileset_name, tileset_index, index=None, orientation=None, frame=None):
        self.name = name
        self.index = index
        self.orientation = orientation
        self.frame = frame
        self.image = image
        self.tileset_name = tileset_name
        self.tileset_index = tileset_index
