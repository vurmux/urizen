#!/usr/bin/python3

import json
import random
from pkg_resources import resource_stream, resource_string

from PIL import Image

from urizen.core.cell import Cell
from urizen.core.thing import Thing
from urizen.core.actor import Actor


TILESETS = [
    'urizen-onebit-basic',
    'urizen-onebit-fantasy-medieval'
]


def _get_tile(im_tileset, json_tileset, index):
    x = (index % json_tileset['columns']) * (json_tileset['tilewidth'] + 1) + 1
    y = (index // json_tileset['columns']) * (json_tileset['tileheight'] + 1) + 1
    return im_tileset.crop((x, y, x+json_tileset['tilewidth'], y+json_tileset['tileheight']))


def _get_tileset_tiles(tileset):
    im_tileset = Image.open(resource_stream('urizen', 'data/tilesets/{}/colored.png'.format(tileset)))
    json_tileset = json.loads(resource_string('urizen', 'data/tilesets/{}/colored.json'.format(tileset)))

    cells = {}
    things = {}
    actors = {}

    current_dict = {}
    for tile in json_tileset['tiles']:
        im_tile = _get_tile(im_tileset, json_tileset, tile['id'])
        tile_type = None
        tile_groups = [None, None, None]
        tile_index = None
        tile_orientation = None
        for att in tile['properties']:
            if att['name'] == 'type':
                tile_type = att['value']
            if att['name'] == 'group1':
                tile_groups[0] = att['value']
            if att['name'] == 'group2':
                tile_groups[1] = att['value']
            if att['name'] == 'group3':
                tile_groups[2] = att['value']
            if att['name'] == 'index':
                tile_index = att['value']
            if att['name'] == 'orientation':
                tile_orientation = att['value']
        tile_groups = list(filter(lambda x: x, tile_groups))
        name = '_'.join(tile_groups)
        if not name:
            continue
        if tile_type == 'cell':
            current_dict = cells
        elif tile_type == 'thing':
            current_dict = things
        elif tile_type == 'actor':
            current_dict = actors
        if tile_orientation != None:
            if name not in current_dict:
                current_dict[name] = {}
            if tile_index != None:
                if tile_orientation not in current_dict[name]:
                    current_dict[name][tile_orientation] = [None] * 10
                current_dict[name][tile_orientation][tile_index] = im_tile
            else:
                current_dict[name][tile_orientation] = [im_tile]
        elif tile_index != None:
            if name not in current_dict:
                current_dict[name] = [None] * 10
            current_dict[name][tile_index] = im_tile
        else:
            current_dict[name] = [im_tile]
    for current_dict in [cells, things, actors]:
        for name in current_dict:
            if type(current_dict[name]) == list:
                current_dict[name] = list(filter(lambda x: x != None, current_dict[name]))
            elif type(current_dict[name]) == dict:
                for orientation in current_dict[name]:
                    current_dict[name][orientation] = list(filter(lambda x: x != None, current_dict[name][orientation]))

    return cells, things, actors


def _get_tileblock_color(tileblock):
    tile = None
    if type(tileblock) == list:
        tile = tileblock[0]
    elif type(tileblock) == dict:
        tile = list(tileblock.values())[0][0]
    for _, color_tuple in tile.getcolors():
        r, g, b, a = color_tuple
        if r + g + b > 0:
            return ('#%02x%02x%02x' % (r, g, b)).upper()
    return '#000000'


cell_tiles = {}
thing_tiles = {}
actor_tiles = {}

for tileset in TILESETS:
    cells, things, actors = _get_tileset_tiles(tileset)
    cell_tiles.update(cells)
    thing_tiles.update(things)
    actor_tiles.update(actors)

C = type('C', (object,), {
    name: type(
        name,
        (Cell,),
        {
            'pixel_color': _get_tileblock_color(cell_tiles[name]),
            'sprite': cell_tiles[name]
        }
    ) for name in cell_tiles
})

T = type('T', (object,), {
    name: type(
        name,
        (Thing,),
        {
            'pixel_color': _get_tileblock_color(thing_tiles[name]),
            'sprite': thing_tiles[name]
        }
    ) for name in thing_tiles
})

A = type('A', (object,), {
    name: type(
        name,
        (Actor,),
        {
            'pixel_color': _get_tileblock_color(actor_tiles[name]),
            'sprite': actor_tiles[name]
        }
    ) for name in actor_tiles
})
