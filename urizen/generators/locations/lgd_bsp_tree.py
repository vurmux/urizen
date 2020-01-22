#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.cell_collection import cell_dungeon_wall, cell_dungeon_floor


def lgd_bsp_tree(w, h, min_size=10):
    M = Map(w, h, fill_cell=cell_dungeon_wall)
    root = BSPNode('w', 0, 0, w, h)
    _recursive_split_tree_node(root, min_size)
    print()
    _print_tree(root)
    return M

class BSPNode(object):
    def __init__(self, xy_type, x, y, w, h, children=None):
        self.xy_type = xy_type
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.children = children

def _print_tree(bsp_node, level=0):
    print(' ' * 4 * level, 'BSP node: x:[{}-{}] y:[{}-{}]'.format(
        (bsp_node.x),
        (bsp_node.x + bsp_node.w),
        (bsp_node.y),
        (bsp_node.y + bsp_node.h)
    ))
    level += 1
    if bsp_node.children:
        _print_tree(bsp_node.children[0], level)
        _print_tree(bsp_node.children[1], level)

def _recursive_split_tree_node(bsp_node, min_size):
    if bsp_node.xy_type == 'w':
        if bsp_node.w > int(min_size * 1.5) or bsp_node.w > 2 * bsp_node.h:
            w_child = random.randint(int(bsp_node.w * 0.33), int(bsp_node.w * 0.66))
            child_left = BSPNode(
                'h',
                bsp_node.x,
                bsp_node.y,
                w_child,
                bsp_node.h
            )
            child_right = BSPNode(
                'h',
                bsp_node.x + w_child,
                bsp_node.y,
                bsp_node.w - w_child,
                bsp_node.h
            )
            bsp_node.children = [child_left, child_right]
            print('Current node: {}-{}'.format((bsp_node.x, bsp_node.y), (bsp_node.x + bsp_node.w, bsp_node.y + bsp_node.h)))
            print('    Split left children')
            _recursive_split_tree_node(child_left, min_size)
            print('    Split right children')
            _recursive_split_tree_node(child_right, min_size)
        print('FINAL node: {}-{}'.format((bsp_node.x, bsp_node.y), (bsp_node.x + bsp_node.w, bsp_node.y + bsp_node.h)))
    elif bsp_node.xy_type == 'h':
        if bsp_node.h > int(min_size * 1.5) or bsp_node.h > 2 * bsp_node.w:
            h_child = random.randint(int(bsp_node.h * 0.33), int(bsp_node.h * 0.66))
            child_top = BSPNode(
                'w',
                bsp_node.x,
                bsp_node.y,
                bsp_node.w,
                h_child
            )
            child_bottom = BSPNode(
                'w',
                bsp_node.x,
                bsp_node.y + h_child,
                bsp_node.w,
                bsp_node.h - h_child
            )
            bsp_node.children = [child_top, child_bottom]
            print('Current node: {}-{}'.format((bsp_node.x, bsp_node.y), (bsp_node.x + bsp_node.w, bsp_node.y + bsp_node.h)))
            print('    Split top children')
            _recursive_split_tree_node(child_top, min_size)
            print('    Split bottom children')
            _recursive_split_tree_node(child_bottom, min_size)
        print('FINAL node: {}-{}'.format((bsp_node.x, bsp_node.y), (bsp_node.x + bsp_node.w, bsp_node.y + bsp_node.h)))
