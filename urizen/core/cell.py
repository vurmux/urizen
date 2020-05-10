#!/usr/bin/python3

from urizen.core.thing import Thing
from urizen.core.actor import Actor


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
    things -- List of things inside the cell
    actors -- List of actors inside the cell
    symbol -- Symbol to print in terminal visualizers
    bg_color -- Background color in terminal visualizers
    fg_color -- Foreground color in terminal visualizers
    pixel_color -- Pixel color for pixel visualizers
    sprite -- Image or image generator in graphical visualizers
    passable -- Is the cell passable
    tags -- List of cell tags
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

    def __init__(self, **kwargs):
        self.features = []
        self.things = []
        self.actors = []
        for arg, value in kwargs.items():
            if arg in Cell.__dict__ and not arg.startswith('__'):
                self.__dict__[arg] = value

    def put(self, entity):
        if issubclass(entity.__class__, Actor):
            self.actors.append(entity)
        elif issubclass(entity.__class__, Thing):
            self.things.append(entity)