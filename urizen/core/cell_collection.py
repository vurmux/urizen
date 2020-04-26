#!/usr/bin/python3

from urizen.core.cell import Cell

# Dungeon cells

cell_void = type('cell_void', (Cell,), {
    'height': 0,
    'terrain': None,
    'cell_type': None,
    'symbol': ' ',
    'pixel_color': '#000000',
    'passable': False,
})

cell_dungeon_floor = type('cell_dungeon_floor', (Cell,), {
    'height': 0,
    'terrain': 'dungeon',
    'cell_type': 'floor',
    'symbol': '.',
    'pixel_color': '#909090',
    'passable': True,
})

cell_dungeon_wall = type('cell_dungeon_wall', (Cell,), {
    'terrain': 'dungeon',
    'cell_type': 'wall',
    'symbol': '#',
    'pixel_color': '#303030',
    'passable': False,
})

cell_dungeon_closed_door = type('cell_dungeon_closed_door', (Cell,), {
    'terrain': 'dungeon',
    'cell_type': 'door',
    'symbol': '+',
    'pixel_color': '#905000',
    'passable': False,
})

cell_dungeon_open_door = type('cell_dungeon_open_door', (Cell,), {
    'terrain': 'dungeon',
    'cell_type': 'door',
    'symbol': '\'',
    'pixel_color': '#905000',
    'passable': True,
})

cell_stairs_down = type('cell_stairs_down', (Cell,), {
    'terrain': 'dungeon',
    'cell_type': 'stairs',
    'symbol': '>',
    'pixel_color': '#257764',
    'passable': True,
})

cell_stairs_up = type('cell_stairs_up', (Cell,), {
    'terrain': 'dungeon',
    'cell_type': 'stairs',
    'symbol': '<',
    'pixel_color': '#257764',
    'passable': True,
})

cell_wall_fence_metal = type('cell_wall_fence_metal', (Cell,), {
    'terrain': 'building',
    'cell_type': 'wall',
    'symbol': '#',
    'pixel_color': '#BBBBBB',
    'passable': False,
})


# World terrain cells

cell_terrain_grassland = type('cell_terrain_grassland', (Cell,), {
    'height': 0,
    'terrain': 'terrain',
    'cell_type': 'terrain',
    'symbol': '"',
    'fg_color': '#00FF00',
    'pixel_color': '#00C000',
    'passable': True,
})

cell_terrain_forest = type('cell_terrain_forest', (Cell,), {
    'terrain': 'terrain',
    'cell_type': 'terrain',
    'symbol': 'T',
    'fg_color': '#00FF00',
    'pixel_color': '#008000',
    'passable': True,
})

cell_terrain_mountain = type('cell_terrain_mountain', (Cell,), {
    'terrain': 'terrain',
    'cell_type': 'terrain',
    'symbol': '^',
    'fg_color': '#FFFFFF',
    'pixel_color': '#909090',
    'passable': True,
})

cell_terrain_pinnacle = type('cell_terrain_pinnacle', (Cell,), {
    'terrain': 'terrain',
    'cell_type': 'terrain',
    'symbol': '^',
    'fg_color': '#FF0000',
    'pixel_color': '#FFFFFF',
    'passable': False,
})

cell_terrain_water = type('cell_terrain_water', (Cell,), {
    'height': 0,
    'terrain': 'terrain',
    'cell_type': 'terrain',
    'symbol': '~',
    'fg_color': '#0000FF',
    'pixel_color': '#0000C0',
    'passable': False,
})

cell_terrain_deep_water = type('cell_terrain_deep_water', (Cell,), {
    'height': 0,
    'terrain': 'terrain',
    'cell_type': 'terrain',
    'symbol': '~',
    'bg_color': '#0000FF',
    'fg_color': '#000000',
    'pixel_color': '#000070',
    'passable': False,
})


# Medieval building cells

cell_floor_plank = type('cell_floor_plank', (Cell,), {
    'height': 0,
    'terrain': 'building',
    'cell_type': 'floor',
    'symbol': '.',
    'pixel_color': '#251000',
    'passable': True
})

cell_floor_flagged = type('cell_floor_flagged', (Cell,), {
    'height': 0,
    'terrain': 'building',
    'cell_type': 'floor',
    'symbol': '.',
    'pixel_color': '#202020',
    'passable': True
})

cell_floor_gravel = type('cell_floor_gravel', (Cell,), {
    'height': 0,
    'terrain': 'building',
    'cell_type': 'floor',
    'symbol': '.',
    'pixel_color': '#202020',
    'passable': True
})

cell_floor_dirt = type('cell_floor_dirt', (Cell,), {
    'height': 0,
    'terrain': 'building',
    'cell_type': 'floor',
    'symbol': '.',
    'pixel_color': '#201005',
    'passable': True
})

cell_wall_plank = type('cell_wall_plank', (Cell,), {
    'terrain': 'building',
    'cell_type': 'wall',
    'symbol': '#',
    'pixel_color': '#703810',
    'passable': False
})

cell_wall_stone = type('cell_wall_stone', (Cell,), {
    'terrain': 'building',
    'cell_type': 'wall',
    'symbol': '#',
    'pixel_color': '#808080',
    'passable': False
})

cell_door_closed = type('cell_door_closed', (Cell,), {
    'terrain': 'building',
    'cell_type': 'door',
    'symbol': '+',
    'pixel_color': '#804500',
    'passable': False
})

cell_door_closed_bars = type('cell_door_closed_bars', (Cell,), {
    'terrain': 'building',
    'cell_type': 'door',
    'symbol': '+',
    'pixel_color': '#804500',
    'passable': False
})

cell_door_open = type('cell_door_open', (Cell,), {
    'terrain': 'building',
    'cell_type': 'door',
    'symbol': '\'',
    'pixel_color': '#804500',
    'passable': True
})

cell_wall_fence_wooden = type('cell_wall_fence_wooden', (Cell,), {
    'terrain': 'building',
    'cell_type': 'wall',
    'symbol': '\"',
    'pixel_color': '#703800',
    'passable': False
})
