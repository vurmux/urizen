#!/usr/bin/python3

import random
import noise
from urizen.core.map import Map
from urizen.core.cell_collection import (
    cell_terrain_deep_water,
    cell_terrain_water,
    cell_terrain_grassland,
    cell_terrain_forest,
    cell_terrain_mountain,
    cell_terrain_pinnacle
)


def world_perlin_noise(w, h, scale=10.0, octaves=6, persistence=0.5, lacunarity=2.0):
    M = Map(w, h)
    min_value = None
    max_value = None
    startx = random.randint(0, w*100)
    starty = random.randint(0, h*100)
    for y, line in enumerate(M.cells):
        for x, C in enumerate(line):
            n = noise.pnoise2(
                (startx+x)/scale,
                (starty+y)/scale,
                octaves=octaves,
                persistence=persistence,
                lacunarity=lacunarity,
                repeatx=w,
                repeaty=h,
                base=2
            )
            M.cells[y][x].noise = n
            if min_value is None:
                min_value = n
            if max_value is None:
                max_value = n
            if n < min_value:
                min_value = n
            if n > max_value:
                max_value = n

    delta = (max_value - min_value) / 12

    for y, line in enumerate(M.cells):
        for x, C in enumerate(line):
            if M.cells[y][x].noise < min_value + delta:
                M.cells[y][x] = cell_terrain_deep_water(x, y)
            elif M.cells[y][x].noise < min_value + 5*delta:
                M.cells[y][x] = cell_terrain_water(x, y)
            elif M.cells[y][x].noise < min_value + 8*delta:
                M.cells[y][x] = cell_terrain_grassland(x, y)
            elif M.cells[y][x].noise < min_value + 10*delta:
                M.cells[y][x] = cell_terrain_forest(x, y)
            elif M.cells[y][x].noise < min_value + 12*delta:
                M.cells[y][x] = cell_terrain_mountain(x, y)
            else:
                M.cells[y][x] = cell_terrain_pinnacle(x, y)
    
    return M
