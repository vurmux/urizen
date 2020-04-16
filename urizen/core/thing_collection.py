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

item_candle = type('item_candle', (Thing,), {
    'thing_type': 'item',
    'symbol': 'L',
    'bg_color': '#000000',
    'fg_color': '#FFFFFF',
    'pixel_color': '#FF0000',
    'sprite': None,
    'passable': True,
    'tags': []
})

item_bones = type('item_bones', (Thing,), {
    'thing_type': 'item',
    'symbol': 'I',
    'bg_color': '#000000',
    'fg_color': '#FFFFFF',
    'pixel_color': '#FFFFF0',
    'sprite': None,
    'passable': True,
    'tags': []
})

item_bucket = type('item_bucket', (Thing,), {
    'thing_type': 'item',
    'symbol': 'U',
    'bg_color': '#000000',
    'fg_color': '#FFFFFF',
    'pixel_color': '#191010',
    'sprite': None,
    'passable': True,
    'tags': []
})

item_spider_web = type('item_spider_web', (Thing,), {
    'thing_type': 'item',
    'symbol': 'O',
    'bg_color': '#000000',
    'fg_color': '#FFFFFF',
    'pixel_color': '#514949',
    'sprite': None,
    'passable': True,
    'tags': []
})

item_pliers = type('item_pliers', (Thing,), {
    'thing_type': 'item',
    'symbol': ':',
    'bg_color': '#000000',
    'fg_color': '#FFFFFF',
    'pixel_color': '#514949',
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
    'pixel_color': '#FF0000',
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
    'passable': True,
    'tags': []
})

furniture_torture_chair = type('furniture_torture_chair', (Thing,), {
    'thing_type': 'furniture',
    'symbol': 'X',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#905000',
    'sprite': None,
    'passable': True,
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

furniture_manger = type('furniture_manger', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#C3C300',
    'sprite': None,
    'passable': False,
    'tags': []
})

furniture_watertrough = type('furniture_watertrough', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'bg_color': '#000000',
    'fg_color': '#0000FF',
    'pixel_color': '#0000CF',
    'sprite': None,
    'passable': False,
    'tags': []
})

furniture_bed = type('furniture_bed', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '_',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#B06000',
    'sprite': None,
    'passable': True,
    'tags': []
})

furniture_sleeping_bag = type('furniture_sleeping_bag', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '_',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#B06000',
    'sprite': None,
    'passable': True,
    'tags': []
})

furniture_chest = type('furniture_chest', (Thing,), {
    'thing_type': 'furniture',
    'symbol': 'Q',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#300238',
    'sprite': None,
    'passable': False,
    'tags': []
})

furniture_wardrobe = type('furniture_wardrobe', (Thing,), {
    'thing_type': 'furniture',
    'symbol': 'W',
    'bg_color': '#000000',
    'fg_color': '#FF0000',
    'pixel_color': '#291010',
    'sprite': None,
    'passable': False,
    'tags': []
})

# Other

other_bonfire = type('other_bonfire', (Thing,), {
    'thing_type': 'item',
    'symbol': ',',
    'bg_color': '#000000',
    'fg_color': '#FFFFFF',
    'pixel_color': '#761600',
    'sprite': None,
    'passable': True,
    'tags': []
})