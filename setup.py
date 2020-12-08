#!/usr/bin/python3

from setuptools import setup, find_packages


LONG_DESCRIPTION = """
Urizen
======

Urizen is the roguelike dungeon generation library written on Python3. It has various algorithms that can be used to generate maps on scale of single rooms to the whole world.

**Note: This project is on early stage of development. It can contain bugs, API breaking changes and lack of documentation.**

Features
--------

- Two main collections - generators and visualizers - that can be used in any variations.
- Easy-to-use map objects with no need of additional libraries.
- Modular architecture that allows simple extension.

Simple example
--------------

.. code:: python

    # Import this library
    import urizen as uz

    # Create a 50x50 size map using BSP algorithm
    M = uz.dungeon_bsp_tree(50, 50)

    # And visualize it using Pillow with Urizen tileset
    uz.vg_tiled(M, scale=3)


The result image will be automatically opened with a default image viewer.
"""

setup(
    name='urizen',
    version='0.2.4',
    description='Roguelike world generation library',
    long_description=LONG_DESCRIPTION,
    url='https://github.com/vurmux/urizen',
    author='Andrey Voronov',
    author_email='vurmux@gmail.com',
    license='Apache',
    classifiers=[
        'Development Status :: 1 - Planning',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3 :: Only',
    ],
    keywords='',
    packages=find_packages(exclude=['doc', 'res', 'build', 'dist']),
    install_requires=[
        'noise',
        'Pillow',
        'pygame>=2.0.0',
        'pygame_gui'
    ],
    extras_require={
        'dev': [],
        'test': [],
    },
    package_data={
        'urizen': [
            'data/tilesets/*/*.json',
            'data/tilesets/*/*.png',
            'data/tilesets/*/*.tsx',
            'data/themes/gui_theme.json',
            'data/themes/images/*.png'
        ]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "urizen = urizen.gui.gui_pygame:main"
        ]
    },
)

