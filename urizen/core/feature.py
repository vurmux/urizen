#!/usr/bin/python3


class Feature(object):
    """
    Feature class

    Attributes:
    feature_type -- Feature type
    symbol -- Symbol to print in terminal visualizers
    bg_color -- Background color in terminal visualizers
    fg_color -- Foreground color in terminal visualizers
    pixel_color -- Pixel color for pixel visualizers
    sprite -- Image or image generator in graphical visualizers
    tags -- List of feature tags
    """

    feature_type = None
    symbol = '.'
    bg_color = '#000000'
    fg_color = '#FFFFFF'
    pixel_color = '#000000'
    sprite = None
    tags = []

    def __init__(self, **kwargs):
        for arg, value in kwargs.items():
            if arg in Feature.__dict__ and not arg.startswith('__'):
                self.__dict__[arg] = value