#!/usr/bin/python3

import random
from urizen.core.map import Map
from urizen.core.entity_collection import C


def dungeon_grid_simple(w, h, room_size=4, delete_chance=0.33):
    """Dungeon map generator based on square room grid."""

    M = Map(w, h, fill_cell=C.floor_flagged)
    _create_room_grid(M, room_size=room_size)
    _create_doors(M, room_size=room_size)
    _crush_walls(M, room_size=room_size, delete_chance=delete_chance)
    return M


def _create_room_grid(M, room_size):
    """Create room grid and clear all cells that are out of the grid."""

    w, h = M.get_size()
    x_border_index = ((w - 1) // (room_size + 1)) * (room_size + 1)
    y_border_index = ((h - 1) // (room_size + 1)) * (room_size + 1)
    for y, line in enumerate(M.cells):
        for x, cell in enumerate(line):
            if x > x_border_index or y > y_border_index:
                M[x, y] = C.void()
            elif x % (room_size + 1) == 0 or y % (room_size + 1) == 0:
                M[x, y] = C.wall_dungeon_smooth()

def _create_doors(M, room_size):
    """Create door in every wall that connects two rooms."""

    w, h = M.get_size()
    x_rooms = ((w - 1) // (room_size + 1))
    y_rooms = ((h - 1) // (room_size + 1))
    for i in range(1, y_rooms):
        for j in range(1, x_rooms):
            if i == 1:
                y = i * (room_size + 1) - random.randint(1, room_size)
                x = j * (room_size + 1)
                M[x, y] = C.door_closed()
            if j == 1:
                y = i * (room_size + 1)
                x = j * (room_size + 1) - random.randint(1, room_size)
                M[x, y] = C.door_closed()
            y = i * (room_size + 1)
            x = j * (room_size + 1) + random.randint(1, room_size)
            M[x, y] = C.door_closed() 
            y = i * (room_size + 1) + random.randint(1, room_size)
            x = j * (room_size + 1)
            M[x, y] = C.door_closed()

def _crush_walls(M, room_size, delete_chance):
    """Randomly remove walls with delete_chance."""

    w, h = M.get_size()
    x_rooms = ((w - 1) // (room_size + 1))
    y_rooms = ((h - 1) // (room_size + 1))
    for i in range(1, y_rooms):
        for j in range(1, x_rooms):
            y = i * (room_size + 1)
            x = j * (room_size + 1) + 1
            chance = random.random()
            if chance < delete_chance:
                for _ in range(room_size):
                    M[x, y] = C.floor_flagged()
                    x += 1
    for i in range(1, y_rooms):
        for j in range(1, x_rooms):
            y = i * (room_size + 1) +1
            x = j * (room_size + 1)
            chance = random.random()
            if chance < delete_chance:
                for _ in range(room_size):
                    M[x, y] = C.floor_flagged()
                    y += 1
