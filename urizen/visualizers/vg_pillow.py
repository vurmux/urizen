#!/usr/bin/python3

from PIL import Image, ImageColor

    
def vg_pillow_pixelated(M, scale=1, show=True, filepath=None):
    w, h = M.get_size()
    pixels = []
    im = Image.new('RGB', (w, h))
    for line in M.cells:
        for cell in line:
            pixels.append(ImageColor.getrgb(cell.pixel_color))
    im.putdata(pixels)
    im = im.resize((w*scale, h*scale), resample=Image.NEAREST)
    if filepath:
        im.save(filepath)
    if show:
        im.show()
