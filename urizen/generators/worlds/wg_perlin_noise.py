#!/usr/bin/python3

import random
import noise
from urizen.core.map import Map


class WG_PerlinNoiseFactory(object):

    def generate(self, w, h, scale=10.0, octaves=6, persistence=0.5, lacunarity=2.0):
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
                    # Deep water
                    M.cells[y][x].symbol = '~'
                    M.cells[y][x].fg_color = '#000000'
                    M.cells[y][x].bg_color = '#0000FF'

                elif M.cells[y][x].noise < min_value + 5*delta:
                    # Water
                    M.cells[y][x].symbol = '~'
                    M.cells[y][x].fg_color = '#0000FF'
                elif M.cells[y][x].noise < min_value + 8*delta:
                    # Grass
                    M.cells[y][x].symbol = '"'
                    M.cells[y][x].fg_color = '#00FF00'
                elif M.cells[y][x].noise < min_value + 10*delta:
                    # Forest
                    M.cells[y][x].symbol = 'T'
                    M.cells[y][x].fg_color = '#00FF00'
                elif M.cells[y][x].noise < min_value + 12*delta:
                    # Mountain
                    M.cells[y][x].symbol = '^'
                    M.cells[y][x].fg_color = '#FFFFFF'
                else:
                    # Super mountain
                    M.cells[y][x].symbol = '^'
                    M.cells[y][x].fg_color = '#FF0000'
        
        return M

WG_PerlinNoise = WG_PerlinNoiseFactory()