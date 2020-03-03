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

# Furniture

furniture_hearth = type('furniture_hearth', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '#',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#B06000',
    'sprite': None,
    'passable': False,
    'tags': []
})

furniture_table = type('furniture_table', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#905000',
    'sprite': None,
    'passable': False,
    'tags': []
})

furniture_alchemist_table = type('furniture_alchemist_table', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'bg_color': '#000000',
    'fg_color': '#00FF00',
    'pixel_color': '#40B040',
    'sprite': None,
    'passable': False,
    'tags': []
})

furniture_chair = type('furniture_chair', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '\\',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#905000',
    'sprite': None,
    'passable': False,
    'tags': []
})

furniture_bookcase = type('furniture_bookcase', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '[',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#FFEED0',
    'sprite': None,
    'passable': False,
    'tags': []
})
