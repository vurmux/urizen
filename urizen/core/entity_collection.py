#!/usr/bin/python3

import json
import random
from pkg_resources import resource_stream, resource_string

from PIL import Image

from urizen.core.cell import Cell
from urizen.core.thing import Thing
from urizen.core.actor import Actor
from urizen.core.tile import Tile
from urizen.core.metatile import Metatile, DEFAULT


TILESETS = [
    'urizen-onebit-basic',
    'urizen-onebit-fantasy-medieval',
    'urizen-onebit-modern',
    'urizen-onebit-fonts',
]


def _get_tile(im_tileset, json_tileset, index):
    x = (index % json_tileset['columns']) * (json_tileset['tilewidth'] + 1) + 1
    y = (index // json_tileset['columns']) * (json_tileset['tileheight'] + 1) + 1
    return im_tileset.crop((x, y, x+json_tileset['tilewidth'], y+json_tileset['tileheight']))


def _get_tileset_tiles(tileset):
    im_tileset = Image.open(resource_stream('urizen', 'data/tilesets/{}/colored.png'.format(tileset)))
    json_tileset = json.loads(resource_string('urizen', 'data/tilesets/{}/colored.json'.format(tileset)).decode('utf-8'))

    cells = {}
    things = {}
    actors = {}

    for tile_object in json_tileset['tiles']:
        im_tile = _get_tile(im_tileset, json_tileset, tile_object['id'])
        tile_type = None
        tile_groups = [None, None, None]
        tile_index = None
        tile_index_in_tileset = tile_object['id']
        tile_frame = None
        tile_orientation = None
        tile_tags = None
        for att in tile_object['properties']:
            if att['name'] == 'type':
                tile_type = att['value']
            elif att['name'] == 'group1':
                tile_groups[0] = att['value']
            elif att['name'] == 'group2':
                tile_groups[1] = att['value']
            elif att['name'] == 'group3':
                tile_groups[2] = att['value']
            elif att['name'] == 'index':
                tile_index = att['value']
            elif att['name'] == 'orientation':
                tile_orientation = att['value']
            elif att['name'] == 'frame':
                tile_frame = att['value']
            elif att['name'] == 'tags':
                tile_tags = att['value'].split(',') if len(att['value']) else []
        tile_groups = list(filter(lambda x: x, tile_groups))
        name = '_'.join(tile_groups)

        tile = Tile(
            name,
            im_tile,
            tileset,
            tile_index_in_tileset,
            index=tile_index,
            orientation=tile_orientation,
            frame=tile_frame
        )

        if not name:
            continue
        dst = {}
        if tile_type == 'cell':
            dst = cells
        elif tile_type == 'thing':
            dst = things
        elif tile_type == 'actor':
            dst = actors
        
        if name not in dst:
            if not tile_orientation:
                geometry = DEFAULT
            elif tile_orientation and tile_orientation.startswith('S'):
                geometry = 'square'
            else:
                geometry = 'linear'
            dst[name] = Metatile(name, geometry=geometry, animated=bool(tile_frame), tags=tile_tags)
            dst[name].add_tile(tile, index=tile_index, orientation=tile_orientation, frame=tile_frame)
        else:
            dst[name].add_tile(tile, index=tile_index, orientation=tile_orientation, frame=tile_frame)

    return cells, things, actors


def _get_tileblock_color(tileblock):
    tile = None
    if type(tileblock) == list:
        tile = tileblock[0]
    elif type(tileblock) == dict:
        tile = list(tileblock.values())[-1][0]
    for _, color_tuple in tile.getcolors():
        r, g, b, a = color_tuple
        if r + g + b > 0:
            return ('#%02x%02x%02x' % (r, g, b)).upper()
    return '#000000'


cell_metatiles = {}
thing_metatiles = {}
actor_metatiles = {}

for tileset in TILESETS:
    cells, things, actors = _get_tileset_tiles(tileset)
    cell_metatiles.update(cells)
    thing_metatiles.update(things)
    actor_metatiles.update(actors)

@classmethod
def filter_by_tags(cls, logic_function, tags_list, instantiate=False):
    result = []
    for name, entity in cls.__dict__.items():
        if type(entity).__name__ != 'type':
            continue
        elif entity.__bases__[0] not in (Cell, Thing, Actor):
            continue
        if logic_function == 'and':
            success = True
            for tag in tags_list:
                if not entity.tags or tag not in entity.tags:
                    success = False
                    break
            if success:
                result.append(entity)
    if instantiate:
        result = [entity() for entity in result]
    return result

C_attributes = {
    name: type(
        name,
        (Cell,),
        {
            #'pixel_color': _get_tileblock_color(cell_metatiles[name]),
            'metatile': cell_metatiles[name],
            'tags': cell_metatiles[name].tags,
        }
    ) for name in cell_metatiles
}
C_attributes['filter_by_tags'] = filter_by_tags

T_attributes = {
    name: type(
        name,
        (Thing,),
        {
            #'pixel_color': _get_tileblock_color(thing_metatiles[name]),
            'metatile': thing_metatiles[name],
            'tags': thing_metatiles[name].tags,
        }
    ) for name in thing_metatiles
}
T_attributes['filter_by_tags'] = filter_by_tags

A_attributes = {
    name: type(
        name,
        (Actor,),
        {
            #'pixel_color': _get_tileblock_color(actor_metatiles[name]),
            'metatile': actor_metatiles[name],
            'tags': actor_metatiles[name].tags,
        }
    ) for name in actor_metatiles
}
A_attributes['filter_by_tags'] = filter_by_tags

C = type('C', (object,), C_attributes)
T = type('T', (object,), T_attributes)
A = type('A', (object,), A_attributes)
