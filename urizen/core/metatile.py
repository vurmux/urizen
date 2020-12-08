#!/usr/bin/python3


DEFAULT = 'default'


class Metatile(object):
    """
    Metatile class

    Attributes:
    name -- Metatile name
    geometry -- Metatile geometry type. Can be 'default', 'linear' or 'square'
    animated -- Flag: Can the metatile be animated
    tiles -- Structure that stores all metatile tiles in a static format
    """

    def __init__(self, name, geometry=DEFAULT, animated=False, tags=[]):
        self.name = name
        self.geometry = geometry
        self.animated = animated
        self.tags = tags
        self.tiles = {'static': {}}
        if self.animated:
            self.tiles['frames'] = {}
        if self.geometry == DEFAULT:
            self.tiles['static'][DEFAULT] = []

    def add_tile(self, tile, index=None, orientation=None, frame=None):
        """
        Add the tile in a `tiles` structure of the metatile depends on frame/index/orientation of a tile.
        """

        def _insert_into(lst, i, item):
            if i >= len(lst):
                lst += [None] * (i - len(lst) + 1)
            lst[i] = item
            return lst
        
        dst = None
        if not frame:
            if self.animated:
                raise TypeError('Animated metatiles can\'t have non-framed tiles.')
            dst = self.tiles['static']
        else:
            if type(frame) != int:
                raise TypeError('Frame index must be integer: {}'.format(frame))
            elif frame <= 0:
                raise ValueError('Frame index must be positive: {}'.format(frame))
            elif not self.animated:
                raise TypeError('Non-animated metatiles can\'t have framed tiles.')
            if frame not in self.tiles['frames']:
                self.tiles['frames'][frame] = {}
                if self.geometry == DEFAULT:
                    self.tiles['frames'][frame][DEFAULT] = []
            dst = self.tiles['frames'][frame]
        
        if not orientation or orientation == DEFAULT:
            dst[DEFAULT] = _insert_into(dst[DEFAULT], index or 0, tile)
        else:
            if orientation not in dst:
                dst[orientation] = []
            dst[orientation] = _insert_into(dst[orientation], index or 0, tile)

    def get_tiles(self, orientation=None, animated=False, frame=0):
        dst = self.tiles

        if not self.animated:
            dst = dst['static']
        elif type(frame) != int:
            raise TypeError('Frame index must be integer: {}'.format(frame))
        elif frame <= 0:
            raise ValueError('Frame index must be positive: {}'.format(frame))
        elif frame not in dst['frames']:
            raise ValueError('Frame index is not found: {}'.format(frame))
        else:
            dst = dst['frames'][frame]

        if self.geometry == DEFAULT:
            return dst[DEFAULT]
        elif orientation not in dst:
            raise ValueError('Orientation is not found: {}'.format(orientation))
        else:
            return dst[orientation]
