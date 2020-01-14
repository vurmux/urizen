import random
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_dungeon_wall,
    cell_dungeon_floor,
    cell_dungeon_closed_door,
    cell_void
)


def lgd_grid_simple(w, h, room_size=4):
    M = Map(w, h, fill_cell=cell_dungeon_floor)
    _create_room_grid(M, room_size=room_size)
    _create_door(M, room_size=room_size)
    _crush_walls(M, room_size=room_size)
    _delete_walls(M)
    return M


def _create_room_grid(M, room_size):
    w, h = M.get_size()
    x_border_index = ((w - 1) // (room_size + 1)) * (room_size + 1)
    y_border_index = ((h - 1) // (room_size + 1)) * (room_size + 1)
    for y, line in enumerate(M.cells):
        for x, C in enumerate(line):
            if x > x_border_index or y > y_border_index:
                M.cells[y][x] = cell_void(x, y)
            elif x % (room_size + 1) == 0 or y % (room_size + 1) == 0:
                M.cells[y][x] = cell_dungeon_wall(x, y)

def _create_door(M, room_size):
    w, h = M.get_size()
    x_rooms = ((w - 1) // (room_size + 1))
    y_rooms = ((h - 1) // (room_size + 1))
    for i in range(1, y_rooms):
        for j in range(1, x_rooms):
            if i == 1:
                y = i * (room_size + 1) - random.randint(1, room_size)
                x = j * (room_size + 1)
                M.cells[y][x] = cell_dungeon_closed_door(x, y)
            if j == 1:
                y = i * (room_size + 1)
                x = j * (room_size + 1) - random.randint(1, room_size)
                M.cells[y][x] = cell_dungeon_closed_door(x, y)
            y = i * (room_size + 1)
            x = j * (room_size + 1) + random.randint(1, room_size)
            M.cells[y][x] = cell_dungeon_closed_door(x, y)
            y = i * (room_size + 1) + random.randint(1, room_size)
            x = j * (room_size + 1)
            M.cells[y][x] = cell_dungeon_closed_door(x, y)

def _crush_walls(M, room_size):
    w, h = M.get_size()
    x_rooms = ((w - 1) // (room_size + 1))
    y_rooms = ((h - 1) // (room_size + 1))
    delete_chance = 0.33
    for i in range(1, y_rooms):
        for j in range(1, x_rooms):
            y = i * (room_size + 1)
            x = j * (room_size + 1) + 1
            chance = random.random()
            z = 0
            if chance < delete_chance:
                while z < room_size:
                    z += 1
                    M.cells[y][x] = cell_dungeon_floor(x, y)
                    x += 1
    for i in range(1, y_rooms):
        for j in range(1, x_rooms):
            y = i * (room_size + 1) +1
            x = j * (room_size + 1)
            chance = random.random()
            z = 0
            if chance < delete_chance:
                while z < room_size:
                    z += 1
                    M.cells[y][x] = cell_dungeon_floor(x, y)
                    y += 1

def _delete_walls(M):
    for j, line in enumerate(M.cells[1: -1]):
        for i, C in enumerate(line[1: -1]):
            x = i + 1
            y = j + 1
            if (M.cells[y][x].cell_type == "wall" and
                    M.cells[y-1][x].cell_type == "floor" and
                    M.cells[y+1][x].cell_type == "floor" and
                    M.cells[y-1][x+1].cell_type == "floor" and
                    M.cells[y-1][x+1].cell_type == "floor" and
                    M.cells[y][x+1].cell_type == "floor" and
                    M.cells[y+1][x+1].cell_type == "floor" and
                    M.cells[y+1][x-1].cell_type == "floor" and
                    M.cells[y][x-1].cell_type == "floor" and
                    M.cells[y-1][x-1].cell_type == "floor"):
                M.cells[y][x] = cell_dungeon_floor(x, y)
