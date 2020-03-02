#!/usr/bin/python3

from urizen.core.thing import Thing

# Items

# Dungeon

item_skull = type('item_skull', (Thing,), {
    'thing_type': 'item',
    'symbol': ',',
    'bg_color': '#000000',
    'fg_color': '#FFFFFF',
    'pixel_color': '#FFFFF0',
    'sprite': None,
    'passable': True,
    'tags': []
})
