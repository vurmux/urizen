#!/usr/bin/python3


class Thing(object):
    """
    Thing class

    Attributes:
    thing_type -- Thing type
    symbol -- Symbol to print in terminal visualizers
    bg_color -- Background color in terminal visualizers
    fg_color -- Foreground color in terminal visualizers
    pixel_color -- Pixel color for pixel visualizers
    sprite -- Image or image generator in graphical visualizers
    passable -- Is the thing passable
    tags -- List of thing tags
    """

    thing_type = None
    symbol = '.'
    bg_color = '#000000'
    fg_color = '#FFFFFF'
    pixel_color = '#000000'
    sprite = None
    passable = True
    tags = []

    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            if arg in Thing.__dict__ and not arg.startswith('__'):
                self.__dict__[arg] = value
    
    @property
    def cname(self):
        return self.__class__.__name__
