#!/usr/bin/python3

from urizen.core.thing import Thing

# Items

# Dungeon

item_bones_skull = type('item_bones_skull', (Thing,), {
    'thing_type': 'item',
    'symbol': ',',
    'pixel_color': '#FFFFF0',
    'passable': True,
})

item_furniture_torch = type('item_furniture_torch', (Thing,), {
    'thing_type': 'item',
    'symbol': 'L',
    'pixel_color': '#FF0000',
    'passable': True,
})

item_bones_human = type('item_bones_human', (Thing,), {
    'thing_type': 'item',
    'symbol': 'I',
    'pixel_color': '#FFFFF0',
    'passable': True,
})

item_bones_remains = type('item_bones_remains', (Thing,), {
    'thing_type': 'item',
    'symbol': 'I',
    'pixel_color': '#FFFFF0',
    'passable': True,
})

item_furniture_bucket = type('item_furniture_bucket', (Thing,), {
    'thing_type': 'item',
    'symbol': 'U',
    'pixel_color': '#191010',
    'passable': True,
})

item_spider_web = type('item_spider_web', (Thing,), {
    'thing_type': 'item',
    'symbol': 'O',
    'pixel_color': '#514949',
    'passable': True,
})

item_tool_tongs = type('item_tool_tongs', (Thing,), {
    'thing_type': 'item',
    'symbol': ':',
    'pixel_color': '#514949',
    'passable': True,
})

# Furniture

item_furniture_hearth = type('item_furniture_hearth', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '#',
    'pixel_color': '#FF0000',
    'passable': False,
})

other_blood = type('other_blood', (Thing,), {
    'thing_type': 'blood',
    'symbol': '.',
    'pixel_color': '#FF0000',
    'passable': True,
})

item_furniture_table = type('item_furniture_table', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'pixel_color': '#905000',
    'passable': False,
})

cell_magic_alchemisttable = type('cell_magic_alchemisttable', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'pixel_color': '#40B040',
    'passable': False,
})

item_furniture_stool = type('item_furniture_stool', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '\\',
    'pixel_color': '#905000',
    'passable': True,
})

item_furniture_torture = type('item_furniture_torture', (Thing,), {
    'thing_type': 'furniture',
    'symbol': 'X',
    'pixel_color': '#905000',
    'passable': True,
})

item_furniture_bookcase = type('item_furniture_bookcase', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '[',
    'pixel_color': '#FFEED0',
    'passable': False,
})

item_furniture_mangler = type('item_furniture_mangler', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'pixel_color': '#C3C300',
    'passable': False,
})

furniture_watertrough = type('furniture_watertrough', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '=',
    'pixel_color': '#0000CF',
    'passable': False,
})

item_furniture_bed_single = type('item_furniture_bed_single', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '_',
    'pixel_color': '#B06000',
    'passable': True,
})

item_furniture_napsack = type('item_furniture_napsack', (Thing,), {
    'thing_type': 'furniture',
    'symbol': '_',
    'pixel_color': '#B06000',
    'passable': True,
})

item_furniture_chest = type('item_furniture_chest', (Thing,), {
    'thing_type': 'furniture',
    'symbol': 'Q',
    'pixel_color': '#300238',
    'passable': False,
})

item_furniture_closet = type('item_furniture_closet', (Thing,), {
    'thing_type': 'furniture',
    'symbol': 'W',
    'pixel_color': '#291010',
    'passable': False,
})

# Other

item_furniture_bonfire = type('item_furniture_bonfire', (Thing,), {
    'thing_type': 'item',
    'symbol': ',',
    'pixel_color': '#761600',
    'passable': True,
})