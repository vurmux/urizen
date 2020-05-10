#!/usr/bin/python3

import random
import noise
from urizen.core.map import Map
from urizen.core.entity_collection import C


def world_perlin_noise(w, h, scale=10.0, octaves=6, persistence=0.5, lacunarity=2.0):
    M = Map(w, h)
    min_value = None
    max_value = None
    startx = random.randint(0, w*100)
    starty = random.randint(0, h*100)
    for y, line in enumerate(M.cells):
        for x, cell in enumerate(line):
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
            M[x, y].noise = n
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
        for x, cell in enumerate(line):
            if M[x, y].noise < min_value + delta:
                M[x, y] = C.overworld_ocean()
            elif M[x, y].noise < min_value + 5*delta:
                M[x, y] = C.overworld_ocean()
            elif M[x, y].noise < min_value + 8*delta:
                M[x, y] = C.overworld_plains()
            elif M[x, y].noise < min_value + 10*delta:
                M[x, y] = C.overworld_forest()
            elif M[x, y].noise < min_value + 12*delta:
                M[x, y] = C.overworld_mountain()
            else:
                M[x, y] = C.overworld_pinnacle()
    
    return M
