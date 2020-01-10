#!/usr/bin/python3

from colorama import init, Fore, Style, Back

    
def vt_colorama(M):
    init()
    for line in M.cells:
        for cell in line:
            print(
                (
                    _transform_color(cell.bg_color, is_fore=False) +
                    _transform_color(cell.fg_color) +
                    cell.symbol
                ),
                end=''
            )
            print(Style.RESET_ALL, end='')
        print()

def _transform_color(rgb_color, is_fore=True):
    if rgb_color == '#000000':
        return Fore.BLACK if is_fore else Back.BLACK
    elif rgb_color == '#FF0000':
        return Fore.RED if is_fore else Back.RED
    elif rgb_color == '#00FF00':
        return Fore.GREEN if is_fore else Back.GREEN
    elif rgb_color == '#0000FF':
        return Fore.BLUE if is_fore else Back.BLUE
    elif rgb_color == '#FFFF00':
        return Fore.RED if is_fore else Back.RED
    elif rgb_color == '#FF0000':
        return Fore.YELLOW if is_fore else Back.YELLOW
    elif rgb_color == '#FF00FF':
        return Fore.RED if is_fore else Back.RED
    elif rgb_color == '#FF0000':
        return Fore.MAGENTA if is_fore else Back.MAGENTA
    elif rgb_color == '#00FFFF':
        return Fore.CYAN if is_fore else Back.CYAN
    elif rgb_color == '#FFFFFF':
        return Fore.WHITE if is_fore else Back.WHITE
    else:
        return Fore.WHITE if is_fore else Back.BLACK
