#!/usr/bin/python3


class Tile(object):
    """
    Tile class

    Attributes:
    name -- Metatile name
    index -- Tile index
    orientation -- Tile orientation for non-default metatile geometry
    frame -- Tile frame for animated tiles
    image -- PIL Image of a tile
    tileset_name -- Name of the tileset
    tileset_index -- Tile index in a tileset
    """

    def __init__(self, name, image, tileset_name, tileset_index, index=None, orientation=None, frame=None):
        self.name = name
        self.index = index
        self.orientation = orientation
        self.frame = frame
        self.image = image
        self.tileset_name = tileset_name
        self.tileset_index = tileset_index
