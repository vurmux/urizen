#!/usr/bin/python3

import json
import random
from pkg_resources import resource_stream, resource_string

from PIL import Image

from urizen.core.entity_collection import C


POSITION_TABLE = {
    '0000': 'H',
    '0001': 'L',
    '0010': 'R',
    '0011': 'H',
    '0100': 'U',
    '0101': 'RD',
    '0110': 'DL',
    '0111': 'RDL',
    '1000': 'D',
    '1001': 'UR',
    '1010': 'UL',
    '1011': 'URL',
    '1100': 'V',
    '1101': 'URD',
    '1110': 'UDL',
    '1111': 'C',
}


def vg_tiled(M, scale=1, show=True, filepath=None):

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
            name = im_element.__class__.__name__

            im_cell = None
            if type(im_element.sprite) == dict and element_type == 'cell':
                up = '1' if M.up_to(xpos, ypos).__class__.__name__ == name else '0'
                down = '1' if M.down_to(xpos, ypos).__class__.__name__ == name else '0'
                left = '1' if M.left_to(xpos, ypos).__class__.__name__ == name else '0'
                right = '1' if M.right_to(xpos, ypos).__class__.__name__ == name else '0'
                position = POSITION_TABLE[up+down+left+right]
                im_cell = random.choice(im_element.sprite.get(position, C.unknown().sprite))
            elif type(im_element.sprite) == dict and element_type == 'thing':
                up = (
                    '1'
                    if M.up_to(xpos, ypos) and
                    len(M.up_to(xpos, ypos).things) and
                    M.up_to(xpos, ypos).things[0].__class__.__name__ == name
                    else '0'
                )
                down = (
                    '1'
                    if M.down_to(xpos, ypos) and
                    len(M.down_to(xpos, ypos).things) and
                    M.down_to(xpos, ypos).things[0].__class__.__name__ == name
                    else '0'
                )
                left = (
                    '1'
                    if M.left_to(xpos, ypos) and
                    len(M.left_to(xpos, ypos).things) and
                    M.left_to(xpos, ypos).things[0].__class__.__name__ == name
                    else '0'
                )
                right = (
                    '1' if M.right_to(xpos, ypos) and
                    len(M.right_to(xpos, ypos).things) and
                    M.right_to(xpos, ypos).things[0].__class__.__name__ == name
                    else '0'
                )
                position = POSITION_TABLE[up+down+left+right]
                im_cell = random.choice(im_element.sprite.get(position, C.unknown().sprite))
            elif type(im_element.sprite) == dict and element_type == 'actor':
                up = (
                    '1'
                    if M.up_to(xpos, ypos) and
                    len(M.up_to(xpos, ypos).actors) and
                    M.up_to(xpos, ypos).actors[0].__class__.__name__ == name
                    else '0'
                )
                down = (
                    '1'
                    if M.down_to(xpos, ypos) and
                    len(M.down_to(xpos, ypos).actors) and
                    M.down_to(xpos, ypos).actors[0].__class__.__name__ == name
                    else '0'
                )
                left = (
                    '1'
                    if M.left_to(xpos, ypos) and
                    len(M.left_to(xpos, ypos).actors) and
                    M.left_to(xpos, ypos).actors[0].__class__.__name__ == name
                    else '0'
                )
                right = (
                    '1'
                    if M.right_to(xpos, ypos) and
                    len(M.right_to(xpos, ypos).actors) and
                    M.right_to(xpos, ypos).actors[0].__class__.__name__ == name
                    else '0'
                )
                position = POSITION_TABLE[up+down+left+right]
                im_cell = random.choice(im_element.sprite.get(position, C.unknown().sprite))
            elif type(im_element.sprite) == list:
                im_cell = random.choice(im_element.sprite)

            result_im.paste(im_cell, box=(xpos*12, ypos*12))

    result_im = result_im.resize((im_w*scale, im_h*scale), resample=Image.NEAREST)
    if filepath:
        result_im.save(filepath)
    if show:
        result_im.show()