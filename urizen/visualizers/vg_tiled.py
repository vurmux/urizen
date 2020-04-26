#!/usr/bin/python3

import json
from PIL import Image
from pkg_resources import resource_stream, resource_string
import random


def vg_tiled(M, scale=1, show=True, filepath=None, tileset='default_fantasy'):
    im_tileset = Image.open(resource_stream('urizen', 'data/tilesets/{}/colored.png'.format(tileset)))
    json_tileset = json.loads(resource_string('urizen', 'data/tilesets/{}/colored.json'.format(tileset)))

    tiles_dict = {}
    for tile in json_tileset['tiles']:
        im_tile = _get_tile(im_tileset, tile['id'], json_tileset)
        tile_type = None
        tile_groups = [None, None, None]
        tile_index = None
        for att in tile['properties']:
            if att['name'] == 'type':
                tile_type = att['value']
            if att['name'] == 'supergroup':
                tile_groups[0] = att['value']
            if att['name'] == 'group':
                tile_groups[1] = att['value']
            if att['name'] == 'subgroup' or att['name'] == 'subtype':
                tile_groups[2] = att['value']
            if att['name'] == 'index':
                tile_index = att['value']
        tile_groups = list(filter(lambda x: x != None, tile_groups))
        name = '_'.join([tile_type] + tile_groups)
        if tile_index != None and name not in tiles_dict:
            tiles_dict[name] = [None] * 5
            tiles_dict[name][tile_index] = im_tile
        elif tile_index != None:
            tiles_dict[name][tile_index] = im_tile
        else:
            tiles_dict[name] = [im_tile]
    for name in tiles_dict:
        tiles_dict[name] = list(filter(lambda x: x != None, tiles_dict[name]))

    im_w, im_h = M.get_size()
    im_w *= json_tileset['tilewidth']
    im_h *= json_tileset['tileheight']
    result_im = Image.new('RGB', (im_w, im_h))
    for ypos, line in enumerate(M.cells):
        for xpos, cell in enumerate(line):
            if not len(cell.things):
                name = cell.__class__.__name__
            else:
                name = cell.things[0].__class__.__name__
            im_cell = None
            if name not in tiles_dict:
                im_cell = tiles_dict['unknown'][0]
            elif len(tiles_dict[name]) == 1:
                im_cell = tiles_dict[name][0]
            elif random.random() > 0.5:
                im_cell = tiles_dict[name][0]
            else:
                im_cell = random.choice(tiles_dict[name][1:])
            result_im.paste(im_cell, box=(xpos*json_tileset['tilewidth'], ypos*json_tileset['tileheight']))
    result_im = result_im.resize((im_w*scale, im_h*scale), resample=Image.NEAREST)
    if filepath:
        result_im.save(filepath)
    if show:
        result_im.show()


def _get_tile(im, index, json_tileset):
    x = (index % json_tileset['columns']) * (json_tileset['tilewidth'] + 1) + 1
    y = (index // json_tileset['columns']) * (json_tileset['tileheight'] + 1) + 1
    return im.crop((x, y, x+12, y+12))