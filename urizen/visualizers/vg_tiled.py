#!/usr/bin/python3

import json
import random
from pkg_resources import resource_stream, resource_string

from PIL import Image

from urizen.core.entity_collection import C


POSITION_TABLE = {
    (0, 0, 0, 0): 'H',
    (0, 0, 0, 1): 'L',
    (0, 0, 1, 0): 'R',
    (0, 0, 1, 1): 'H',
    (0, 1, 0, 0): 'U',
    (0, 1, 0, 1): 'RD',
    (0, 1, 1, 0): 'DL',
    (0, 1, 1, 1): 'RDL',
    (1, 0, 0, 0): 'D',
    (1, 0, 0, 1): 'UR',
    (1, 0, 1, 0): 'UL',
    (1, 0, 1, 1): 'URL',
    (1, 1, 0, 0): 'V',
    (1, 1, 0, 1): 'URD',
    (1, 1, 1, 0): 'UDL',
    (1, 1, 1, 1): 'C',
}


def vg_tiled(M, scale=1, show=True, filepath=None, seed=None):

    random.seed(seed)
    im_w, im_h = M.get_size()
    im_w *= 12
    im_h *= 12
    result_im = Image.new('RGB', (im_w, im_h))
    for ypos, line in enumerate(M.cells):
        for xpos, cell in enumerate(line):
            im_element = None
            element_type = None
            if len(cell.actors):
                im_element = cell.actors[0]
                element_type = 'actor'
            elif len(cell.things):
                im_element = cell.things[0]
                element_type = 'thing'
            else:
                im_element = cell
                element_type = 'cell'
            name = im_element.cname

            im_cell = None
            if type(im_element.sprite) == dict and element_type == 'cell':
                up = int(M.up_to(xpos, ypos).cname == name)
                down = int(M.down_to(xpos, ypos).cname == name)
                left = int(M.left_to(xpos, ypos).cname == name)
                right = int(M.right_to(xpos, ypos).cname == name)
                position = POSITION_TABLE[(up, down, left, right)]
                im_cell = random.choice(im_element.sprite.get(position, C.unknown().sprite))
            elif type(im_element.sprite) == dict and element_type == 'thing':
                up = int(
                    M.up_to(xpos, ypos) and
                    len(M.up_to(xpos, ypos).things) and
                    M.up_to(xpos, ypos).things[0].cname == name
                )
                down = int(
                    M.down_to(xpos, ypos) and
                    len(M.down_to(xpos, ypos).things) and
                    M.down_to(xpos, ypos).things[0].cname == name
                )
                left = int(
                    M.left_to(xpos, ypos) and
                    len(M.left_to(xpos, ypos).things) and
                    M.left_to(xpos, ypos).things[0].cname == name
                )
                right = int(
                    M.right_to(xpos, ypos) and
                    len(M.right_to(xpos, ypos).things) and
                    M.right_to(xpos, ypos).things[0].cname == name
                )
                position = POSITION_TABLE[(up, down, left, right)]
                im_cell = random.choice(im_element.sprite.get(position, C.unknown().sprite))
            elif type(im_element.sprite) == dict and element_type == 'actor':
                up = int(
                    M.up_to(xpos, ypos) and
                    len(M.up_to(xpos, ypos).actors) and
                    M.up_to(xpos, ypos).actors[0].cname == name
                )
                down = int(
                    M.down_to(xpos, ypos) and
                    len(M.down_to(xpos, ypos).actors) and
                    M.down_to(xpos, ypos).actors[0].cname == name
                )
                left = int(
                    M.left_to(xpos, ypos) and
                    len(M.left_to(xpos, ypos).actors) and
                    M.left_to(xpos, ypos).actors[0].cname == name
                )
                right = int(
                    M.right_to(xpos, ypos) and
                    len(M.right_to(xpos, ypos).actors) and
                    M.right_to(xpos, ypos).actors[0].cname == name
                )
                position = POSITION_TABLE[(up, down, left, right)]
                im_cell = random.choice(im_element.sprite.get(position, C.unknown().sprite))
            elif type(im_element.sprite) == list:
                im_cell = random.choice(im_element.sprite)

            result_im.paste(im_cell, box=(xpos*12, ypos*12))

    result_im = result_im.resize((im_w*scale, im_h*scale), resample=Image.NEAREST)
    if filepath:
        result_im.save(filepath)
    if show:
        result_im.show()